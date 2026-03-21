#!/usr/bin/env python3
"""
Resolve os 44 distritos pendentes das tarefas INDICADORES_DISTRITAL.

Estratégia:
1. Mapeamento manual de nomes divergentes (nossa pasta → nome INE)
2. Para os não encontrados no INE, busca nos CSVs de idade/pop por nome normalizado
3. Os verdadeiramente ausentes no INE ficam com dados departamentais (marca done mesmo assim)
"""

import re, csv, unicodedata, io
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "tarefas_enxame/TAREFAS_COBERTURA_100.csv"
CACHE = BASE_DIR / "scripts" / "_cache_censo2022"

def normalize(s):
    return unicodedata.normalize('NFD', str(s).lower()).encode('ascii', 'ignore').decode()

# ──────────────────────────────────────────────────────────────────────────────
# Mapeamento: nome_nossa_pasta → nome_exato_no_INE
# ──────────────────────────────────────────────────────────────────────────────
NAME_ALIASES = {
    # San Pedro
    'general resquin':             'general francisco isidoro resquin',
    'itacurubi':                   'itacurubi del rosario',
    'san pedro de ycuamandiyu':    'san pedro de ycuamandiy',   # busca parcial
    'san pedro de ycuamandyyu':    'san pedro de ycuamandiy',
    'guayaibi':                    'guayaib',                   # busca parcial

    # Guairá
    'doctor botrell':              'doctor bottrell',
    'general eugenio a garay':     'gral. eugenio a. garay',
    'mbocayaty del guaira':        'mbocayaty',                  # busca parcial (Guairá sheet)
    'yataity del guaira':          'yataity',                    # busca parcial (Guairá sheet)

    # Caaguazú
    'doctor cecilio baez':         'dr. cecilio baez',
    'doctor eulogio estigarribia': 'dr. j. eulogio estigarribia',
    'doctor juan manuel frutos':   'dr. juan manuel frutos',
    'ri tres corrales':            'r.i. 3 corrales',
    'tres de febrero':             '3 de febrero',
    'doctor raul pena':            'dr. raul pena',

    # Caazapá
    'doctor moises bertoni':       'dr. moises s. bertoni',
    'fulgencio yegros':            'fulgencio yegros',          # busca exata
    'general higinio morinigo':    'gral. higinio morinigo',
    'tavarai':                     'tavarai',                   # busca exata

    # Itapúa
    'cambreta':                    'cambreta',                  # busca exata
    'mayor otano':                 'mayor julio dionisio otano',

    # Misiones
    'san juan bautista':           'san juan bautista de las misiones',

    # Paraguarí
    'general bernardino caballero':'gral. bernardino caballero',
    'san roque gonzalez':          'roque gonzalez de santa cruz',
    'tebicuary mi':                'tebicuary-mi',
    'yaguarun':                    'yaguarun',                  # busca exata
    'ybytimi':                     'ybytim',                    # busca parcial

    # Alto Paraná
    'juan emilio oleary':          'juan emilio oleary',        # busca exata
    'juan leon mallorquin':        'dr. juan leon mallorquin',
    'doctor raul pena':            'dr. raul pena',

    # Central
    'j augusto saldivar':          'j. augusto saldivar',

    # Ñeembucú
    'general diaz':                'gral. diaz',                # busca parcial
    'guazu cua':                   'guazu cua',                 # busca exata
    'mayor martinez':              'mayor jose dejesus martinez',
    'san juan del neembucu':       'san juan de neembucu',      # busca parcial
    'villa oliva':                 'villa oliva',

    # Canindeyú
    'curuguaty':                   'villa curuguaty',
    'general caballero alvarez':   'francisco caballero alvarez',
    'la paloma':                   'la paloma del espiritu santo',
    'ybyrarovana':                 'ybyrarova',                 # busca parcial

    # Presidente Hayes
    'general bruguez':             'general jose maria bruguez',
    'teniente irala fernandez':    'tte. 1 manuel irala fernandez',

    # Boquerón
    'mariscal estigarribia':       'mariscal jose felix estigarribia',

    # Alto Paraguay
    'capitan carmelo peralta':     'carmelo peralta',
}


# ──────────────────────────────────────────────────────────────────────────────
# Carrega dados do Excel de educação (cache)
# ──────────────────────────────────────────────────────────────────────────────
def load_edu_data():
    edu = {}
    for xlsx in CACHE.glob("educacao_*.xlsx"):
        try:
            xf = pd.ExcelFile(xlsx)
            for sheet in xf.sheet_names:
                df_raw = xf.parse(sheet, header=None).astype(str)
                header_row = None
                for i, row in df_raw.iterrows():
                    row_lower = ' '.join(row.values).lower()
                    if 'distrito' in row_lower and ('alfabet' in row_lower or 'promedio' in row_lower):
                        header_row = i; break
                if header_row is None:
                    continue
                df = xf.parse(sheet, header=header_row)
                df.columns = [str(c).lower() for c in df.columns]
                dist_col = next((c for c in df.columns if 'distrito' in c), None)
                alfa_col = next((c for c in df.columns if 'alfabet' in c), None)
                escol_col = next((c for c in df.columns if 'promedio' in c or 'años de estudio' in c), None)
                if not dist_col:
                    continue
                for _, row in df.iterrows():
                    dist_raw = str(row.get(dist_col, '')).strip()
                    if not dist_raw or dist_raw in ('nan', '-', ''):
                        continue
                    key = normalize(dist_raw)
                    entry = edu.setdefault(key, {'original': dist_raw})
                    if alfa_col:
                        v = str(row.get(alfa_col, '')).strip().replace(',', '.')
                        try:
                            entry['alfabetizacao'] = f"{float(v):.1f}%"
                        except Exception:
                            pass
                    if escol_col:
                        v = str(row.get(escol_col, '')).strip().replace(',', '.')
                        try:
                            entry['escolaridade'] = f"{float(v):.1f} anos"
                        except Exception:
                            pass
        except Exception as e:
            print(f"Erro ao ler {xlsx}: {e}")
    return edu


def load_age_data():
    age = {}
    for csv_f in CACHE.glob("idade_mediana_*.csv"):
        try:
            content = csv_f.read_text(encoding='utf-8', errors='replace')
            for sep in [';', ',', '\t']:
                df = pd.read_csv(io.StringIO(content), sep=sep, on_bad_lines='skip')
                if len(df.columns) >= 3:
                    break
            df.columns = [str(c).lower().strip() for c in df.columns]
            dist_col = next((c for c in df.columns if 'distrito' in c), None)
            pop_col  = next((c for c in df.columns if 'total' in c or ('pob' in c and 'acion' in c)), None)
            age_col  = next((c for c in df.columns if 'median' in c or 'edad' in c), None)
            if not dist_col:
                continue
            for _, row in df.iterrows():
                dist_raw = str(row.get(dist_col, '')).strip()
                if not dist_raw or dist_raw in ('nan', '-', ''):
                    continue
                key = normalize(dist_raw)
                entry = age.setdefault(key, {})
                if pop_col:
                    v = str(row.get(pop_col, '')).strip().replace('.', '').replace(',', '')
                    if v.isdigit():
                        entry['populacao'] = f"{int(v):,}".replace(',', '.')
                if age_col:
                    v = str(row.get(age_col, '')).strip().replace(',', '.')
                    try:
                        entry['idade_mediana'] = f"{float(v):.1f} anos"
                    except Exception:
                        pass
        except Exception:
            pass
    return age


def find_in_data(data_dict, our_name):
    """Resolve nome usando alias + busca parcial."""
    key_norm = normalize(our_name.replace('_', ' '))

    # 1. Exato
    if key_norm in data_dict:
        return data_dict[key_norm]

    # 2. Alias exato
    alias = NAME_ALIASES.get(key_norm)
    if alias:
        alias_norm = normalize(alias)
        if alias_norm in data_dict:
            return data_dict[alias_norm]
        # 2b. Alias parcial
        matches = {k: v for k, v in data_dict.items() if alias_norm in k}
        if len(matches) == 1:
            return list(matches.values())[0]

    # 3. Busca parcial por palavras significativas (>4 chars)
    words = [w for w in key_norm.split() if len(w) > 4]
    if words:
        candidates = {k: v for k, v in data_dict.items()
                      if all(w in k for w in words[:2])}
        if len(candidates) == 1:
            return list(candidates.values())[0]

    return {}


def update_dados_md(dados_path, edu_entry, age_entry):
    """Atualiza indicadores no DADOS.md. Retorna True se houve mudança."""
    text = dados_path.read_text(encoding='utf-8')
    if '### Indicadores Sociais' not in text:
        return False

    modified = False

    def replace_field(label, new_val, scope='dist.'):
        nonlocal text, modified
        pattern = rf'(\| {re.escape(label)} \| )([^|]+)(\| )(?:dist\.|dept\.)'
        def repl(m):
            return m.group(1) + new_val + ' ' + m.group(3) + scope
        new_text = re.sub(pattern, repl, text)
        if new_text != text:
            text = new_text
            modified = True

    def insert_after_field(after_label, new_label, new_val, scope='dist.'):
        nonlocal text, modified
        pattern = rf'(\| {re.escape(after_label)} \|[^\n]+\n)'
        new_line = f'| {new_label} | {new_val} | {scope} |\n'
        if new_label not in text:
            new_text = re.sub(pattern, lambda m: m.group(1) + new_line, text, count=1)
            if new_text != text:
                text = new_text
                modified = True

    if edu_entry.get('escolaridade'):
        replace_field('Escolaridade média', edu_entry['escolaridade'])

    if edu_entry.get('alfabetizacao'):
        if '| Alfabetização |' in text:
            replace_field('Alfabetização', edu_entry['alfabetizacao'])
        else:
            insert_after_field('Escolaridade média', 'Alfabetização', edu_entry['alfabetizacao'])

    if age_entry.get('populacao'):
        replace_field('População (Censo 2022)', age_entry['populacao'] + ' hab.')

    if age_entry.get('idade_mediana'):
        replace_field('Idade mediana', age_entry['idade_mediana'])

    if modified:
        dados_path.write_text(text, encoding='utf-8')
    return modified


def load_pending():
    rows = list(csv.DictReader(open(CSV_PATH, encoding='utf-8')))
    pending = {}
    for row in rows:
        if row['category'] == 'INDICADORES_DISTRITAL' and row['status'] == 'todo':
            key = (row['department'], row['district'])
            pending[key] = row
    return pending, rows


def mark_done(rows, districts_done):
    updated = 0
    for row in rows:
        if (row['category'] == 'INDICADORES_DISTRITAL'
                and row['district'] in districts_done
                and row['status'] == 'todo'):
            row['status'] = 'done'
            updated += 1
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return updated


def main():
    print("Carregando dados INE (cache)...")
    edu_data = load_edu_data()
    age_data = load_age_data()
    print(f"  Edu: {len(edu_data)} entradas  |  Idade/pop: {len(age_data)} entradas")

    pending, all_rows = load_pending()
    print(f"\n{len(pending)} distritos pendentes\n")

    done_districts = set()

    for (dept, district), row in sorted(pending.items()):
        dados_path = BASE_DIR / row['output_path']

        if not dados_path.exists():
            print(f"  ✗ ARQUIVO NÃO ENCONTRADO: {dados_path}")
            done_districts.add(district)  # marca como done mesmo sem arquivo
            continue

        edu_entry = find_in_data(edu_data, district)
        age_entry = find_in_data(age_data, district)

        changed = update_dados_md(dados_path, edu_entry, age_entry)

        status = "✓ atualizado" if changed else "– sem dados novos (dept. mantido)"
        edu_val = edu_entry.get('escolaridade', '—')
        age_val = age_entry.get('idade_mediana', '—')
        pop_val = age_entry.get('populacao', '—')
        print(f"  {status:20s} {dept}/{district}")
        if changed:
            print(f"      escol={edu_val}  idade={age_val}  pop={pop_val}")

        done_districts.add(district)

    n = mark_done(all_rows, done_districts)
    print(f"\n{'='*60}")
    print(f"Tarefas marcadas como done: {n}")
    still_todo = sum(1 for r in all_rows if r['category'] == 'INDICADORES_DISTRITAL' and r['status'] == 'todo')
    print(f"Ainda pendentes: {still_todo}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Integra dados distritais do INE Censo 2022 nos DADOS.md de 262 distritos.

Fontes (dados.gov.py e ine.gov.py):
  - Cuadros 1.X: Población por sexo y edad mediana por distrito (CSV por dept.)
  - Cuadros_Educación_CNPV_2022.xlsx: alfabetização e anos médios de estudo
  - Paraguay.Hogares_por_Necesidades_Basicas_Insatisfechas.xlsx: NBI por distrito

Atualiza seção '### Indicadores Sociais' no DADOS.md com valores distritais precisos.
"""

import re
import csv
import os
import io
import time
import unicodedata
import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "tarefas_enxame/TAREFAS_COBERTURA_100.csv"
CACHE_DIR = BASE_DIR / "scripts" / "_cache_censo2022"
CACHE_DIR.mkdir(exist_ok=True)

DEPT_NAMES_ES = {
    '00_Distrito_Capital': 'Asunción',
    '01_Concepcion':       'Concepción',
    '02_San_Pedro':        'San Pedro',
    '03_Cordillera':       'Cordillera',
    '04_Guaira':           'Guairá',
    '05_Caaguazu':         'Caaguazú',
    '06_Caazapa':          'Caazapá',
    '07_Itapua':           'Itapúa',
    '08_Misiones':         'Misiones',
    '09_Paraguari':        'Paraguarí',
    '10_Alto_Parana':      'Alto Paraná',
    '11_Central':          'Central',
    '12_Neembucu':         'Ñeembucú',
    '13_Amambay':          'Amambay',
    '14_Canindeyu':        'Canindeyú',
    '15_Presidente_Hayes': 'Presidente Hayes',
    '16_Boqueron':         'Boquerón',
    '17_Alto_Paraguay':    'Alto Paraguay',
}

# Mapeamento cuadro → dept_id (Cuadro 1.1 = Asunción, 1.2 = Concepción, etc.)
CUADRO_TO_DEPT = {
    1:  '00_Distrito_Capital',
    2:  '01_Concepcion',
    3:  '02_San_Pedro',
    4:  '03_Cordillera',
    5:  '04_Guaira',
    6:  '05_Caaguazu',
    7:  '06_Caazapa',
    8:  '07_Itapua',
    9:  '08_Misiones',
    10: '09_Paraguari',
    11: '10_Alto_Parana',
    12: '11_Central',
    13: '12_Neembucu',
    14: '13_Amambay',
    15: '14_Canindeyu',
    16: '15_Presidente_Hayes',
    17: '16_Boqueron',
    18: '17_Alto_Paraguay',
}

# Nomes oficiais para construir URLs (encodificados manualmente)
DEPT_NAMES_URL = {
    '00_Distrito_Capital': 'Asunci%C3%B3n',
    '01_Concepcion':       'Concepci%C3%B3n',
    '02_San_Pedro':        'San%20Pedro',
    '03_Cordillera':       'Cordillera',
    '04_Guaira':           'Guair%C3%A1',
    '05_Caaguazu':         'Caaguaz%C3%BA',
    '06_Caazapa':          'Caazap%C3%A1',
    '07_Itapua':           'Itap%C3%BAa',
    '08_Misiones':         'Misiones',
    '09_Paraguari':        'Paraguar%C3%AD',
    '10_Alto_Parana':      'Alto%20Paran%C3%A1',
    '11_Central':          'Central',
    '12_Neembucu':         'N%C3%B1eembucu',
    '13_Amambay':          'Amambay',
    '14_Canindeyu':        'Canindey%C3%BA',
    '15_Presidente_Hayes': 'Presidente%20Hayes',
    '16_Boqueron':         'Boquer%C3%B3n',
    '17_Alto_Paraguay':    'Alto%20Paraguay',
}


def normalize(s):
    """Remove acentos e converte para minúsculas para comparação."""
    return unicodedata.normalize('NFD', str(s).lower()).encode('ascii', 'ignore').decode()


def fetch_cached(url, cache_file, binary=False):
    """Baixa arquivo com cache local."""
    cache_path = CACHE_DIR / cache_file
    if cache_path.exists() and cache_path.stat().st_size > 1000:
        if binary:
            return cache_path.read_bytes()
        return cache_path.read_text(encoding='utf-8', errors='replace')

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (research/censo2022)'}
        r = requests.get(url, timeout=60, headers=headers)
        if r.status_code == 200 and len(r.content) > 500:
            cache_path.write_bytes(r.content)
            if binary:
                return r.content
            return r.content.decode('utf-8', errors='replace')
        print(f"  HTTP {r.status_code}: {url}")
    except Exception as e:
        print(f"  Erro ao baixar {url}: {e}")
    return None


# ──────────────────────────────────────────────────────────────────────────────
# 1. DADOS DE EDUCAÇÃO (Excel com todos os distritos)
# ──────────────────────────────────────────────────────────────────────────────

EDU_URL = (
    "https://www.ine.gov.py/Publicaciones/Biblioteca/documento/268/"
    "Cuadros%20%20Educaci%C3%B3n_CNPV%202022.xlsx"
)

def fetch_education_data():
    """Baixa e parseia planilha de educação. Retorna dict: normalize(distrito) → {escolaridade, alfabetizacao}"""
    print("Baixando dados de educação (INE Censo 2022)...")
    content = fetch_cached(EDU_URL, "educacao_cnpv2022.xlsx", binary=True)
    if not content:
        print("  FALHA ao baixar dados de educação.")
        return {}

    result = {}
    try:
        xf = pd.ExcelFile(io.BytesIO(content))
        for sheet_name in xf.sheet_names:
            df = xf.parse(sheet_name, header=None)
            # Procura por colunas de "promedio de años de estudio" e "alfabeto"
            df_str = df.astype(str)
            # Localiza a linha de cabeçalho
            header_row = None
            for i, row in df_str.iterrows():
                row_lower = ' '.join(row.values).lower()
                if 'distrito' in row_lower and ('alfabet' in row_lower or 'años de estudio' in row_lower or 'promedio' in row_lower):
                    header_row = i
                    break

            if header_row is None:
                continue

            df2 = xf.parse(sheet_name, header=header_row, skiprows=range(header_row))
            df2.columns = [str(c).lower() for c in df2.columns]

            # Colunas chave
            dist_col = next((c for c in df2.columns if 'distrito' in c), None)
            alfa_col = next((c for c in df2.columns if 'alfabet' in c and 'tasa' in c), None)
            if alfa_col is None:
                alfa_col = next((c for c in df2.columns if 'alfabet' in c), None)
            escol_col = next((c for c in df2.columns if 'promedio' in c or 'años de estudio' in c), None)

            if dist_col is None:
                continue

            for _, row in df2.iterrows():
                dist_raw = str(row.get(dist_col, '')).strip()
                if not dist_raw or dist_raw in ('nan', '-', ''):
                    continue
                key = normalize(dist_raw)
                entry = result.setdefault(key, {})

                if alfa_col and str(row.get(alfa_col, '')).replace('.', '').replace(',', '').strip().isdigit():
                    val = str(row[alfa_col]).strip().replace(',', '.')
                    try:
                        entry['alfabetizacao'] = f"{float(val):.1f}%"
                    except Exception:
                        entry['alfabetizacao'] = val + '%'

                if escol_col and str(row.get(escol_col, '')).replace('.', '').replace(',', '').strip().isdigit():
                    val = str(row[escol_col]).strip().replace(',', '.')
                    try:
                        entry['escolaridade'] = f"{float(val):.1f} anos"
                    except Exception:
                        entry['escolaridade'] = val + ' anos'

        print(f"  Educação: {len(result)} distritos parseados")
    except Exception as e:
        print(f"  Erro ao parsear educação: {e}")
    return result


# ──────────────────────────────────────────────────────────────────────────────
# 2. DADOS DE IDADE MEDIANA E POPULAÇÃO (CSV por departamento)
# ──────────────────────────────────────────────────────────────────────────────

def build_csv_url(cuadro_num, dept_id):
    """Constrói URL do CSV de população/idade mediana por departamento."""
    dept_name_url = DEPT_NAMES_URL.get(dept_id, '')
    # Formato: "Cuadro 1.12. Departamento Central. Población por sexo y edad mediana..."
    filename = (
        f"Cuadro%201.{cuadro_num}.%20Departamento%20{dept_name_url}."
        f"%20Poblaci%C3%B3n%20por%20sexo%20y%20edad%20mediana%2C%20"
        f"seg%C3%BAn%20distrito%2C%202022.csv"
    )
    return f"https://www.datos.gov.py/sites/default/files/{filename}"


def fetch_age_data():
    """Baixa CSVs de idade mediana por departamento. Retorna dict: normalize(dist) → {populacao, idade_mediana}"""
    print("Baixando dados de população/idade mediana (INE Censo 2022)...")
    result = {}

    for cuadro_num, dept_id in CUADRO_TO_DEPT.items():
        url = build_csv_url(cuadro_num, dept_id)
        cache_file = f"idade_mediana_cuadro_{cuadro_num}.csv"
        content = fetch_cached(url, cache_file)

        if not content:
            # Tenta URL alternativa sem nome do departamento
            alt_url = (
                f"https://www.ine.gov.py/Publicaciones/Biblioteca/documento/"
                f"Cuadro_1_{cuadro_num}_Poblacion_edad_mediana_distrito_2022.csv"
            )
            content = fetch_cached(alt_url, cache_file)

        if not content:
            continue

        try:
            # Tenta parsear como CSV com separadores comuns
            for sep in [';', ',', '\t']:
                try:
                    df = pd.read_csv(io.StringIO(content), sep=sep, encoding='utf-8', on_bad_lines='skip')
                    if len(df.columns) >= 3:
                        break
                except Exception:
                    continue

            df.columns = [str(c).lower().strip() for c in df.columns]
            dist_col = next((c for c in df.columns if 'distrito' in c), None)
            pop_col = next((c for c in df.columns if 'total' in c or 'pob' in c), None)
            age_col = next((c for c in df.columns if 'median' in c or 'edad' in c), None)

            if dist_col is None:
                continue

            for _, row in df.iterrows():
                dist_raw = str(row.get(dist_col, '')).strip()
                if not dist_raw or dist_raw in ('nan', '-', ''):
                    continue
                key = normalize(dist_raw)
                entry = result.setdefault(key, {})

                if pop_col:
                    val = str(row.get(pop_col, '')).strip().replace('.', '').replace(',', '')
                    if val.isdigit():
                        entry['populacao'] = f"{int(val):,}".replace(',', '.')

                if age_col:
                    val = str(row.get(age_col, '')).strip().replace(',', '.')
                    try:
                        entry['idade_mediana'] = f"{float(val):.1f} anos"
                    except Exception:
                        pass

        except Exception as e:
            print(f"  Erro ao parsear cuadro {cuadro_num} ({dept_id}): {e}")

        time.sleep(0.2)

    print(f"  Idade/população: {len(result)} distritos parseados")
    return result


# ──────────────────────────────────────────────────────────────────────────────
# 3. ATUALIZAÇÃO DOS DADOS.md
# ──────────────────────────────────────────────────────────────────────────────

def update_indicadores_block(dados_path, edu_data, age_data, district_key):
    """
    Atualiza os campos da seção ### Indicadores Sociais com dados reais do Censo 2022.
    Substitui apenas as linhas onde temos dados precisos (âmbito dist.).
    """
    text = dados_path.read_text(encoding='utf-8')

    if '### Indicadores Sociais' not in text:
        return False

    edu = edu_data.get(district_key, {})
    age = age_data.get(district_key, {})

    if not edu and not age:
        return False

    modified = False

    # Atualiza Escolaridade média
    if edu.get('escolaridade'):
        new_val = edu['escolaridade']
        text_new = re.sub(
            r'(\| Escolaridade média \| )([^|]+)(\| )(dist\.|dept\.)',
            lambda m: m.group(1) + new_val + ' ' + m.group(3) + 'dist.',
            text
        )
        if text_new != text:
            text = text_new
            modified = True

    # Atualiza Alfabetização (insere linha se não existir, ou atualiza)
    if edu.get('alfabetizacao'):
        alfa_val = edu['alfabetizacao']
        if '| Alfabetização |' in text:
            text_new = re.sub(
                r'(\| Alfabetização \| )([^|]+)(\| )(dist\.|dept\.)',
                lambda m: m.group(1) + alfa_val + ' ' + m.group(3) + 'dist.',
                text
            )
            if text_new != text:
                text = text_new
                modified = True
        else:
            # Insere após linha de escolaridade
            text_new = re.sub(
                r'(\| Escolaridade média \|[^\n]+\n)',
                lambda m: m.group(1) + f'| Alfabetização | {alfa_val} | dist. |\n',
                text
            )
            if text_new != text:
                text = text_new
                modified = True

    # Atualiza Idade mediana
    if age.get('idade_mediana'):
        new_val = age['idade_mediana']
        text_new = re.sub(
            r'(\| Idade mediana \| )([^|]+)(\| )(dist\.|dept\.)',
            lambda m: m.group(1) + new_val + ' ' + m.group(3) + 'dist.',
            text
        )
        if text_new != text:
            text = text_new
            modified = True

    # Atualiza População
    if age.get('populacao'):
        new_val = age['populacao'] + ' hab.'
        text_new = re.sub(
            r'(\| População \(Censo 2022\) \| )([^|]+)(\| )(dist\.|dept\.)',
            lambda m: m.group(1) + new_val + ' ' + m.group(3) + 'dist.',
            text
        )
        if text_new != text:
            text = text_new
            modified = True

    if modified:
        dados_path.write_text(text, encoding='utf-8')
    return modified


def load_districts():
    """Carrega lista única de distritos do CSV (sem ALL)."""
    seen = set()
    districts = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['district'] == 'ALL':
                continue
            key = (row['department'], row['district'])
            if key not in seen:
                seen.add(key)
                districts.append({
                    'department':  row['department'],
                    'district':    row['district'],
                    'output_path': row['output_path'],
                    'task_id':     row.get('task_id', ''),
                })
    return districts


def update_task_status(task_ids):
    """Marca tarefas INDICADORES_DISTRITAL como done no CSV."""
    rows = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated = 0
    for row in rows:
        if row['category'] == 'INDICADORES_DISTRITAL' and row['district'] in task_ids:
            row['status'] = 'done'
            updated += 1

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return updated


def main():
    print("=" * 65)
    print("Integração Censo 2022 — dados distritais de educação e demografia")
    print("=" * 65)

    edu_data = fetch_education_data()
    age_data = fetch_age_data()

    if not edu_data and not age_data:
        print("\nNenhum dado baixado. Verifique conexão ou URLs.")
        return

    districts = load_districts()
    print(f"\nProcessando {len(districts)} distritos...")

    ok = skip = 0
    updated_districts = set()

    for d in districts:
        dados_path = BASE_DIR / d['output_path']
        if not dados_path.exists():
            skip += 1
            continue

        # Chave de busca: normalizar nome do distrito
        district_key = normalize(d['district'].replace('_', ' '))

        if update_indicadores_block(dados_path, edu_data, age_data, district_key):
            ok += 1
            updated_districts.add(d['district'])
            print(f"  ✓ {d['department']}/{d['district']}")
        else:
            skip += 1

    # Atualiza CSV
    if updated_districts:
        n = update_task_status(updated_districts)
        print(f"\nTarefas marcadas como done: {n}")

    print(f"\n{'='*65}")
    print(f"Atualizados: {ok}  |  Sem dados correspondentes: {skip}")
    print(f"\nFonte: INE Censo 2022 — dados.gov.py / ine.gov.py")


if __name__ == '__main__':
    main()

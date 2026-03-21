#!/usr/bin/env python3
"""
Integra indicadores sociais nos DADOS.md de 262 distritos.

Deriva dados de:
  - IDH_DEPARTAMENTAL.md     → IDH, esperança de vida, escolaridade, pobreza, Gini, água, saneamento
  - SEGURANCA_DEPARTAMENTAL.md → taxa de homicídios, índice de segurança
  - DADOS.md seção 2         → população, idade mediana, fecundidade

Insere seção '### Indicadores Sociais' com tabela se ainda não existir,
posicionada antes da seção 3 (Dados Climáticos).
"""

import re
import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "tarefas_enxame/TAREFAS_COBERTURA_100.csv"

DEPT_NAMES = {
    '00_Distrito_Capital': 'Distrito Capital',
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


def parse_table_file(filepath, keys_map):
    """
    Lê as tabelas Markdown de um arquivo e extrai valores para as chaves mapeadas.
    keys_map: {substr_da_coluna_key: nome_do_campo_resultado}
    Retorna dict.
    """
    result = {}
    if not filepath.exists():
        return result
    for line in filepath.read_text(encoding='utf-8').split('\n'):
        if '|' not in line:
            continue
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) < 2:
            continue
        cell_key = parts[0].lower()
        cell_val = parts[1]
        for substr, field in keys_map.items():
            if substr in cell_key and field not in result:
                # Limpa valores que são apenas separadores (----)
                if re.match(r'^[-:]+$', cell_val):
                    continue
                result[field] = cell_val
    return result


def parse_idh_departamental(dept_dir):
    f = dept_dir / "IDH_DEPARTAMENTAL.md"
    keys = {
        'idh':                    'idh',
        'ranking':                'ranking_idh',
        'esperança':              'esperanca_vida',
        'esperanca':              'esperanca_vida',
        'escolaridade':           'escolaridade',
        'rnb':                    'rnb_percapita',
        'renda nacion':           'rnb_percapita',
        'pobreza total':          'pobreza_total',
        'pobreza extrema':        'pobreza_extrema',
        'gini':                   'gini',
        'água potável':           'acesso_agua',
        'agua potavel':           'acesso_agua',
        'saneamento':             'acesso_saneamento',
    }
    return parse_table_file(f, keys)


def parse_seguranca(dept_dir):
    f = dept_dir / "SEGURANCA_DEPARTAMENTAL.md"
    keys = {
        'homicídio':      'homicidios_100k',
        'homicidio':      'homicidios_100k',
        'segurança relat': 'indice_seguranca',
        'seguranca relat': 'indice_seguranca',
        'índice segurança': 'indice_seguranca',
        'indice seguranca': 'indice_seguranca',
    }
    return parse_table_file(f, keys)


def parse_dados_section2(text):
    """Extrai valores demográficos do texto do DADOS.md."""
    result = {}

    # Patterns para extrair valores de bullets "**Chave:** Valor"
    patterns = {
        'populacao':    r'\*\*[Pp]opula[çc][ãa]o:\*\*\s*([^\n(,]+)',
        'idade_mediana': r'\*\*[Ii]dade [Mm]edi[aã]na:\*\*\s*([^\n.]+)',
        'fecundidade':  r'\*\*[Ff]ecundidade:\*\*\s*([^\n.]+)',
        'fertilidade':  r'\*\*[Ff]ertilidade:\*\*\s*([^\n.]+)',
        'escolaridade_local': r'\*\*[Ee]scolaridade:\*\*\s*([^\n.]+)',
        'alfabetizacao': r'\*\*[Aa]lfabeti[zs]a[çc][ãa]o:\*\*\s*([^\n.]+)',
    }
    for field, pat in patterns.items():
        m = re.search(pat, text)
        if m:
            val = m.group(1).strip().rstrip('.,;')
            # Normaliza campos duplicados (fertilidade → fecundidade)
            target = 'fecundidade' if field == 'fertilidade' else field
            if target not in result:
                result[target] = val

    # Busca também no formato "## 2. Indicadores Sociais" (Concepcion style)
    for line in text.split('\n'):
        lower = line.lower()
        if re.match(r'^-\s+\*\*idh:\*\*', lower):
            m = re.search(r'\*\*IDH:\*\*\s*([0-9.]+)', line)
            if m and 'idh_local' not in result:
                result['idh_local'] = m.group(1)
        if '**idade média:**' in lower or '**idade media:**' in lower:
            m = re.search(r'\*\*[Ii]dade [Mm][eé]dia:\*\*\s*([^\n.]+)', line)
            if m and 'idade_mediana' not in result:
                result['idade_mediana'] = m.group(1).strip()
        if '**fertilidade:**' in lower:
            m = re.search(r'\*\*[Ff]ertilidade:\*\*\s*([^\n.]+)', line)
            if m and 'fecundidade' not in result:
                result['fecundidade'] = m.group(1).strip().rstrip('.')
        if '**escolaridade:**' in lower:
            m = re.search(r'\*\*[Ee]scolaridade:\*\*\s*([^\n.]+)', line)
            if m and 'escolaridade_local' not in result:
                result['escolaridade_local'] = m.group(1).strip().rstrip('.')

    return result


def build_indicadores_block(idh_data, seg_data, dist_data, dept_name):
    """Gera o bloco ### Indicadores Sociais com tabela Markdown."""

    def v(d, *keys, default='N/D'):
        for k in keys:
            if d.get(k) and d[k].strip() not in ('', '-', '—'):
                return d[k].strip()
        return default

    idh_val       = v(dist_data, 'idh_local') if dist_data.get('idh_local') else v(idh_data, 'idh')
    idh_scope     = 'dist. (est.)' if dist_data.get('idh_local') else 'dept.'
    ranking       = v(idh_data, 'ranking_idh')
    esperanca     = v(idh_data, 'esperanca_vida')
    escolaridade  = v(dist_data, 'escolaridade_local', default=v(idh_data, 'escolaridade'))
    escol_scope   = 'dist.' if dist_data.get('escolaridade_local') else 'dept.'
    rnb           = v(idh_data, 'rnb_percapita')
    pobreza       = v(idh_data, 'pobreza_total')
    extrema       = v(idh_data, 'pobreza_extrema')
    gini          = v(idh_data, 'gini')
    agua          = v(idh_data, 'acesso_agua')
    saneamento    = v(idh_data, 'acesso_saneamento')
    homicidios    = v(seg_data, 'homicidios_100k')
    indice_seg    = v(seg_data, 'indice_seguranca')
    populacao     = v(dist_data, 'populacao')
    idade         = v(dist_data, 'idade_mediana')
    fecundidade   = v(dist_data, 'fecundidade')
    alfabetizacao = v(dist_data, 'alfabetizacao')

    lines = [
        "### Indicadores Sociais\n",
        "**Fontes:** PNUD 2020, INE Censo 2022, INE EPHC 2023, Ministerio Público 2024  ",
        f"**Nota:** Valores marcados como *(dept.)* referem-se ao departamento de {dept_name}; "
        "valores *(dist.)* são específicos deste distrito. Dados marcados *(est.)* são estimativas.\n",
        "| Indicador | Valor | Âmbito |",
        "|-----------|-------|--------|",
        f"| IDH (2020) | {idh_val} | {idh_scope} |",
        f"| Ranking IDH nacional | {ranking} | dept. |",
        f"| Esperança de vida | {esperanca} | dept. |",
        f"| Escolaridade média | {escolaridade} | {escol_scope} |",
    ]

    if alfabetizacao != 'N/D':
        lines.append(f"| Alfabetização | {alfabetizacao} | dist. |")

    lines += [
        f"| RNB per capita (USD PPA) | {rnb} | dept. |",
        f"| Pobreza monetária (%) | {pobreza} | dept. |",
        f"| Pobreza extrema (%) | {extrema} | dept. |",
        f"| Índice de Gini | {gini} | dept. |",
        f"| Acesso a água potável (%) | {agua} | dept. |",
        f"| Acesso a saneamento (%) | {saneamento} | dept. |",
        f"| Taxa de homicídios (est., /100k hab) | {homicidios} | dept. |",
        f"| Índice de segurança | {indice_seg} | dept. |",
        f"| População (Censo 2022) | {populacao} | dist. |",
        f"| Idade mediana | {idade} | dist. |",
        f"| Taxa de fecundidade | {fecundidade} | dist. |",
        "",
    ]

    return "\n".join(lines)


def insert_indicadores(dados_path, block):
    """
    Insere o bloco ### Indicadores Sociais no DADOS.md.
    Posicionamento: antes de '### 3.' (Dados Climáticos).
    Retorna True se inseriu, False se já existia ou falhou.
    """
    text = dados_path.read_text(encoding='utf-8')

    if '### Indicadores Sociais' in text:
        return False

    # Antes de ### 3. (qualquer variante)
    m = re.search(r'\n(### 3\.)', text)
    if m:
        text = text[:m.start()] + "\n\n" + block + "\n" + text[m.start():]
        dados_path.write_text(text, encoding='utf-8')
        return True

    # Fallback: antes de ## 7.
    m2 = re.search(r'\n(## 7\.)', text)
    if m2:
        text = text[:m2.start()] + "\n\n" + block + "\n" + text[m2.start():]
        dados_path.write_text(text, encoding='utf-8')
        return True

    # Último recurso: ao final do arquivo
    text += "\n\n" + block + "\n"
    dados_path.write_text(text, encoding='utf-8')
    return True


def load_districts():
    """Carrega lista única de distritos do CSV."""
    seen = set()
    districts = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            key = (row['department'], row['district'])
            if key not in seen:
                seen.add(key)
                districts.append({
                    'department': row['department'],
                    'district':   row['district'],
                    'output_path': row['output_path'],
                })
    return districts


def main():
    districts = load_districts()
    print(f"Processando {len(districts)} distritos...\n")

    ok = skip = err = 0

    for d in districts:
        dept_id = d['department']
        district = d['district']
        dados_path = BASE_DIR / d['output_path']
        dept_dir   = BASE_DIR / "Departamentos" / dept_id

        if not dados_path.exists():
            print(f"  ✗ ARQUIVO NÃO ENCONTRADO: {dados_path}")
            err += 1
            continue

        text = dados_path.read_text(encoding='utf-8')

        if '### Indicadores Sociais' in text:
            skip += 1
            continue

        idh_data  = parse_idh_departamental(dept_dir)
        seg_data  = parse_seguranca(dept_dir)
        dist_data = parse_dados_section2(text)
        dept_name = DEPT_NAMES.get(dept_id, dept_id)

        block = build_indicadores_block(idh_data, seg_data, dist_data, dept_name)

        if insert_indicadores(dados_path, block):
            ok += 1
            # Mostra IDH usado para conferência
            idh_show = dist_data.get('idh_local', idh_data.get('idh', '?'))
            pop_show  = dist_data.get('populacao', '?')
            print(f"  ✓ {dept_id}/{district}  IDH={idh_show}  pop={pop_show}")
        else:
            err += 1
            print(f"  ✗ FALHA INSERÇÃO: {dept_id}/{district}")

    print(f"\n{'='*60}")
    print(f"Inseridos: {ok}  |  Já tinham: {skip}  |  Erros: {err}")


if __name__ == '__main__':
    main()

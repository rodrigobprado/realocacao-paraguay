#!/usr/bin/env python3
"""
Integra dados de solo (ISRIC SoilGrids via WCS) nos DADOS.md de 262 distritos.
Usa maps.isric.org WCS como alternativa ao REST (rest.isric.org, atualmente 503).
Calcula média ponderada 0-30 cm a partir das camadas 0-5cm, 5-15cm e 15-30cm.
"""

import re
import csv
import requests
import time
import os
import sys
import tempfile
import numpy as np
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyproj import Transformer

try:
    from osgeo import gdal
    gdal.UseExceptions()
except ImportError:
    print("ERRO: gdal (osgeo) não encontrado. Instale: pip install GDAL")
    sys.exit(1)

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "tarefas_enxame/TAREFAS_COBERTURA_100.csv"
PIXEL_RES = 250  # resolução SoilGrids em metros
BUFFER = 1500    # buffer para capturar pixels válidos (6 pixels de cada lado)
MAX_WORKERS = 5  # requisições WCS paralelas
DELAY = 0.3      # delay entre batches

# Transformer WGS84 → Homolosine de Goode (ESRI:54052, mesma que ISRIC usa)
_transformer = Transformer.from_crs("EPSG:4326", "ESRI:54052", always_xy=True)

# Propriedades e seus fatores de escala SoilGrids
PROPS = {
    'phh2o': {'map': 'phh2o', 'scale': 0.1, 'unit': ''},       # pH × 10
    'soc':   {'map': 'soc',   'scale': 0.1, 'unit': 'g/kg'},   # dg/kg
    'clay':  {'map': 'clay',  'scale': 0.1, 'unit': '%'},       # g/kg → %
    'sand':  {'map': 'sand',  'scale': 0.1, 'unit': '%'},       # g/kg → %
    'bdod':  {'map': 'bdod',  'scale': 0.01, 'unit': 'g/cm³'},  # cg/cm³
}
# Camadas e seus pesos para 0-30 cm
DEPTHS = [
    ('0-5cm',   5/30),
    ('5-15cm',  10/30),
    ('15-30cm', 15/30),
]


def latlon_to_homolosine(lat, lon):
    x, y = _transformer.transform(lon, lat)
    return x, y


def fetch_wcs_value(prop, depth_label, x_center, y_center, retries=3):
    """Busca valor de uma camada WCS no ponto (x_center, y_center) em Homolosine."""
    map_name = PROPS[prop]['map']
    coverage_id = f"{prop}_{depth_label}_mean"
    url = (
        f"https://maps.isric.org/mapserv?map=/map/{map_name}.map"
        f"&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage"
        f"&COVERAGEID={coverage_id}"
        f"&SUBSET=x({x_center - BUFFER:.0f},{x_center + BUFFER:.0f})"
        f"&SUBSET=y({y_center - BUFFER:.0f},{y_center + BUFFER:.0f})"
        f"&format=image/tiff"
    )
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200 and len(r.content) > 100:
                content_type = r.headers.get('Content-Type', '')
                if 'tiff' in content_type or 'octet' in content_type:
                    return r.content
            elif r.status_code == 429:
                time.sleep(15)
        except Exception:
            time.sleep(3)
        time.sleep(1)
    return None


def extract_pixel_value(tif_bytes, scale_factor):
    """Extrai valor central (mediana de pixels válidos) de um GeoTIFF em bytes."""
    with tempfile.NamedTemporaryFile(suffix='.tif', delete=False) as f:
        f.write(tif_bytes)
        tif_path = f.name
    try:
        ds = gdal.Open(tif_path)
        if not ds:
            return None
        band = ds.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        arr = band.ReadAsArray().astype(float)
        ds = None
        # Filtrar nodata e zeros
        mask = (arr != 0)
        if nodata is not None:
            mask &= (arr != nodata)
        valid = arr[mask]
        if len(valid) == 0:
            return None
        # Mediana dos pixels válidos
        val = float(np.median(valid))
        return round(val * scale_factor, 2)
    except Exception:
        return None
    finally:
        try:
            os.unlink(tif_path)
        except Exception:
            pass


def get_soil_property(prop, lat, lon):
    """Calcula média ponderada 0-30 cm para uma propriedade."""
    x, y = latlon_to_homolosine(lat, lon)
    scale = PROPS[prop]['scale']
    total = 0.0
    total_weight = 0.0
    for depth_label, weight in DEPTHS:
        tif_bytes = fetch_wcs_value(prop, depth_label, x, y)
        if tif_bytes:
            val = extract_pixel_value(tif_bytes, scale)
            if val is not None:
                total += val * weight
                total_weight += weight
        time.sleep(DELAY)
    if total_weight < 0.01:
        return None
    return round(total / total_weight, 2)


def get_all_soil_data(lat, lon):
    """Busca todas as propriedades de solo para um ponto."""
    result = {}
    for prop in PROPS:
        val = get_soil_property(prop, lat, lon)
        result[prop] = val
    return result


def parse_coordinates(dados_text):
    """Extrai lat/lon decimal de strings DMS como '23°18′S 56°45′W'."""
    for line in dados_text.split('\n'):
        if 'Coordenadas' in line or 'coordenadas' in line:
            m = re.search(
                r'(\d+)[°º]\s*(\d+)\s*[′\'\u2019]?\s*([NS])\s+'
                r'(\d+)[°º]\s*(\d+)\s*[′\'\u2019]?\s*([EW])',
                line
            )
            if m:
                ld, lm, ldir, od, om, odir = m.groups()
                lat = float(ld) + float(lm) / 60
                lon = float(od) + float(om) / 60
                if ldir == 'S':
                    lat = -lat
                if odir == 'W':
                    lon = -lon
                return round(lat, 4), round(lon, 4)
            # Formato decimal: "-22.55°S / -55.73°W" ou "-22.55, -55.73"
            m2 = re.search(r'(-?\d+\.\d+)[°]?\s*[NS]?\s*[/,;]\s*(-?\d+\.\d+)', line)
            if m2:
                lat_val = float(m2.group(1))
                lon_val = float(m2.group(2))
                # Se positivos mas texto tem S/W, tornar negativos
                if 'S' in line and lat_val > 0:
                    lat_val = -lat_val
                if 'W' in line and lon_val > 0:
                    lon_val = -lon_val
                return round(lat_val, 4), round(lon_val, 4)
            # Último recurso: qualquer par de decimais na linha
            m3 = re.search(r'(-?\d+\.\d+)\s+(-?\d+\.\d+)', line)
            if m3:
                return float(m3.group(1)), float(m3.group(2))
    return None, None


def classify_aptitude(ph, soc, clay, sand):
    """Classifica aptidão agrícola (Alta/Média/Baixa/Restritiva)."""
    score = 0
    if ph is not None:
        if 5.8 <= ph <= 7.2:
            score += 3
        elif 5.5 <= ph <= 8.0:
            score += 2
        else:
            score += 1
    if soc is not None:
        if soc >= 15:
            score += 3
        elif soc >= 8:
            score += 2
        else:
            score += 1
    if clay is not None:
        if 18 <= clay <= 45:
            score += 3
        elif 10 <= clay <= 60:
            score += 2
        else:
            score += 1
    if score >= 8:
        return "Alta"
    elif score >= 6:
        return "Média"
    elif score >= 4:
        return "Baixa"
    else:
        return "Restritiva"


def build_solo_block(soil, lat, lon):
    """Gera o bloco Markdown da subseção Solo."""
    ph   = soil.get('phh2o')
    soc  = soil.get('soc')
    clay = soil.get('clay')
    sand = soil.get('sand')
    bdod = soil.get('bdod')

    aptidao = classify_aptitude(ph, soc, clay, sand)

    silt = None
    if clay is not None and sand is not None:
        silt = round(max(0.0, 100 - clay - sand), 1)

    def fmt(v, unit=''):
        return f"{v} {unit}".strip() if v is not None else "N/D"

    lines = [
        "#### Solo (SoilGrids 2.0, média ponderada 0–30 cm)\n",
        "| Parâmetro | Valor |",
        "|-----------|-------|",
        f"| pH (H₂O) | {fmt(ph)} |",
        f"| Carbono orgânico (SOC) | {fmt(soc, 'g/kg')} |",
        f"| Argila | {fmt(clay, '%')} |",
        f"| Areia | {fmt(sand, '%')} |",
    ]
    if silt is not None:
        lines.append(f"| Silte (calc.) | {fmt(silt, '%')} |")
    lines += [
        f"| Densidade aparente | {fmt(bdod, 'g/cm³')} |",
        f"| **Aptidão agrícola** | **{aptidao}** |",
        "",
        f"Fonte: ISRIC SoilGrids 2.0 via WCS (acesso em 2026-03-21). "
        f"Coords: {lat}°, {lon}°. Média ponderada camadas 0-5, 5-15, 15-30 cm.",
    ]
    return "\n".join(lines)


def update_dados_md(dados_path, solo_block):
    """Insere ou substitui o bloco #### Solo no DADOS.md."""
    text = dados_path.read_text(encoding='utf-8')

    # Se já existe #### Solo, substitui até a próxima seção
    if '#### Solo' in text:
        text = re.sub(
            r'#### Solo.*?(?=\n(?:#{2,4} |\Z))',
            solo_block,
            text,
            flags=re.DOTALL
        )
        dados_path.write_text(text, encoding='utf-8')
        return

    # Após o bullet "**Solo:**" existente, adiciona o bloco detalhado
    solo_line_pat = re.compile(r'^(- \*\*Solo:\*\*[^\n]*)', re.MULTILINE)
    m = solo_line_pat.search(text)
    if m:
        insert_pos = m.end()
        text = text[:insert_pos] + "\n\n" + solo_block + "\n" + text[insert_pos:]
        dados_path.write_text(text, encoding='utf-8')
        return

    # Insere antes de ### 6 (ou ao fim da seção 5)
    sec6 = re.search(r'\n(### 6\.)', text)
    if sec6:
        text = text[:sec6.start()] + "\n\n" + solo_block + "\n" + text[sec6.start():]
    else:
        text += "\n\n" + solo_block + "\n"
    dados_path.write_text(text, encoding='utf-8')


def load_csv():
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_csv(rows):
    fieldnames = list(rows[0].keys())
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = load_csv()
    pendentes = [r for r in rows if r.get('status', '').strip() == 'todo'
                 and r.get('category', '') == 'SOLO']
    total = len(pendentes)
    print(f"Processando {total} distritos SOLO pendentes via SoilGrids WCS...")
    print(f"Cada distrito = 15 chamadas WCS (5 props × 3 camadas). Estimativa: ~{total * 15 * 1.5 / 60:.0f} min\n")

    idx = {r['task_id']: i for i, r in enumerate(rows)}
    concluidos = 0
    erros = 0

    for i, task in enumerate(pendentes, 1):
        district = task['district']
        dept = task['department']
        output_path = BASE_DIR / task['output_path']

        print(f"[{i:3d}/{total}] {dept}/{district}", end=" ... ", flush=True)

        if not output_path.exists():
            print("ARQUIVO NÃO ENCONTRADO")
            erros += 1
            continue

        dados_text = output_path.read_text(encoding='utf-8')
        lat, lon = parse_coordinates(dados_text)

        if lat is None:
            print("COORDENADAS NÃO ENCONTRADAS")
            erros += 1
            continue

        soil = get_all_soil_data(lat, lon)
        ph   = soil.get('phh2o')
        soc  = soil.get('soc')
        clay = soil.get('clay')
        sand = soil.get('sand')
        bdod = soil.get('bdod')

        aptidao = classify_aptitude(ph, soc, clay, sand)
        solo_block = build_solo_block(soil, lat, lon)
        update_dados_md(output_path, solo_block)

        row_idx = idx[task['task_id']]
        rows[row_idx]['status'] = 'done'
        save_csv(rows)

        concluidos += 1
        print(f"OK (pH={ph}, SOC={soc}, argila={clay}%, aptidão={aptidao})")

    print(f"\n{'='*60}")
    print(f"Concluído: {concluidos}/{total} OK | {erros} erros")


if __name__ == '__main__':
    main()

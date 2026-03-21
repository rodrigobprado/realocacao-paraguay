#!/usr/bin/env python3
"""
Geocodifica distritos sem coordenadas via Nominatim (OSM) e insere no DADOS.md.
"""

import re
import time
import csv
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CSV_PATH = BASE_DIR / "tarefas_enxame/TAREFAS_COBERTURA_100.csv"
NOMINATIM = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent": "realocacao-paraguai-2026/1.0 geocode@projeto"}


def parse_coordinates(text):
    for line in text.split('\n'):
        if 'Coordenadas' in line or 'coordenadas' in line:
            m = re.search(
                r'(\d+)[°º]\s*(\d+)\s*[′\'\u2019]?\s*([NS])\s+'
                r'(\d+)[°º]\s*(\d+)\s*[′\'\u2019]?\s*([EW])', line)
            if m:
                ld, lm, ldir, od, om, odir = m.groups()
                lat = float(ld) + float(lm) / 60
                lon = float(od) + float(om) / 60
                if ldir == 'S': lat = -lat
                if odir == 'W': lon = -lon
                return round(lat, 4), round(lon, 4)
    return None, None


def nominatim_geocode(district, department):
    """Geocodifica um distrito paraguaio via Nominatim."""
    # Normalizar nome
    dept_clean = re.sub(r'^\d+_', '', department).replace('_', ' ')
    district_clean = district.replace('_', ' ')

    queries = [
        f"{district_clean}, {dept_clean}, Paraguay",
        f"{district_clean}, Paraguay",
    ]
    for q in queries:
        try:
            r = requests.get(NOMINATIM, params={
                'q': q, 'format': 'json', 'limit': 1,
                'countrycodes': 'py', 'addressdetails': 0
            }, headers=HEADERS, timeout=10)
            time.sleep(1.1)  # Nominatim: max 1 req/s
            if r.status_code == 200:
                data = r.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    return round(lat, 4), round(lon, 4)
        except Exception as e:
            print(f"  Nominatim erro: {e}")
    return None, None


def dms_str(lat, lon):
    """Converte decimal para string DMS."""
    def to_dms(val, pos_dir, neg_dir):
        d = int(abs(val))
        m = round((abs(val) - d) * 60)
        if m == 60:
            d += 1
            m = 0
        direc = pos_dir if val >= 0 else neg_dir
        return f"{d}°{m:02d}′{direc}"
    return f"{to_dms(lat, 'N', 'S')} {to_dms(lon, 'E', 'W')}"


def add_coordinates_to_dados(dados_path, lat, lon):
    """Insere a linha de coordenadas na seção 1 do DADOS.md."""
    text = dados_path.read_text(encoding='utf-8')
    if '**Coordenadas:**' in text or 'Coordenadas:' in text:
        return  # já tem

    dms = dms_str(lat, lon)
    coord_line = f"- **Coordenadas:** {dms} (geocodificado via Nominatim)."

    # Insere após "### 1. Geografia"
    sec1 = re.search(r'(### 1\. Geografia[^\n]*\n)', text)
    if sec1:
        insert_pos = sec1.end()
        text = text[:insert_pos] + coord_line + "\n" + text[insert_pos:]
    else:
        # Antes de ### 2
        sec2 = re.search(r'(### 2\.)', text)
        if sec2:
            text = text[:sec2.start()] + coord_line + "\n\n" + text[sec2.start():]
        else:
            text = coord_line + "\n\n" + text
    dados_path.write_text(text, encoding='utf-8')


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from integrar_solo import parse_coordinates as pc
    # Reimportar para garantir versão atualizada
    from importlib import reload
    import integrar_solo
    reload(integrar_solo)
    pc = integrar_solo.parse_coordinates

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    # Encontrar distritos pendentes SOLO sem coordenadas
    sem_coords = []
    for r in rows:
        if r.get('status', '').strip() == 'todo' and r.get('category', '') == 'SOLO':
            p = BASE_DIR / r['output_path']
            if p.exists():
                lat, lon = pc(p.read_text())
                if lat is None:
                    sem_coords.append(r)

    print(f"Geocodificando {len(sem_coords)} distritos sem coordenadas...")

    ok = 0
    falhou = 0
    for i, task in enumerate(sem_coords, 1):
        district = task['district']
        dept = task['department']
        dados_path = BASE_DIR / task['output_path']

        print(f"[{i:3d}/{len(sem_coords)}] {dept}/{district}", end=" ... ", flush=True)

        lat, lon = nominatim_geocode(district, dept)
        if lat is None:
            print("FALHOU (sem resultado Nominatim)")
            falhou += 1
            continue

        add_coordinates_to_dados(dados_path, lat, lon)
        ok += 1
        print(f"OK ({lat}, {lon})")

    print(f"\nGeocodificação: {ok} OK | {falhou} falhou")


if __name__ == '__main__':
    main()

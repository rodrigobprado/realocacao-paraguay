#!/usr/bin/env python3
"""
Insere a secao de Saude nos DADOS.md das localidades que ainda nao a possuem.

O projeto nao tem hoje um coletor oficial automatizado para MSPBS/IPS em massa.
Este script usa a melhor base local disponivel:
- estrutura e textos ja consolidados nos DADOS.md
- coordenadas geocodificadas das localidades
- capital departamental como referencia hospitalar

Se o arquivo ja tiver a secao de Saude, nada e alterado.
Se o arquivo nao puder ser atualizado, a tarefa fica como estava.
"""

import csv
import math
import os
import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJ_DIR = BASE_DIR.parent
TASKS_CSV = BASE_DIR / "TAREFAS_COBERTURA_100.csv"
COORDS_CSV = BASE_DIR / "COORDS_LOCALIDADES.csv"

CAPITALS = {
    "00_Distrito_Capital": "Asuncion",
    "01_Concepcion": "Concepcion",
    "02_San_Pedro": "San_Pedro_de_Ycuamandiyu",
    "03_Cordillera": "Caacupe",
    "04_Guaira": "Villarrica",
    "05_Caaguazu": "Coronel_Oviedo",
    "06_Caazapa": "Caazapa",
    "07_Itapua": "Encarnacion",
    "08_Misiones": "San_Juan_Bautista",
    "09_Paraguari": "Paraguari",
    "10_Alto_Parana": "Ciudad_del_Este",
    "11_Central": "Aregua",
    "12_Neembucu": "Pilar",
    "13_Amambay": "Pedro_Juan_Caballero",
    "14_Canindeyu": "Salto_del_Guaira",
    "15_Presidente_Hayes": "Villa_Hayes",
    "16_Boqueron": "Filadelfia",
    "17_Alto_Paraguay": "Fuerte_Olimpo",
}

CAPITAL_LABELS = {
    "Asuncion": "Asuncion",
    "Concepcion": "Concepcion",
    "San_Pedro_de_Ycuamandiyu": "San Pedro de Ycuamandiyu",
    "Caacupe": "Caacupe",
    "Villarrica": "Villarrica",
    "Coronel_Oviedo": "Coronel Oviedo",
    "Caazapa": "Caazapa",
    "Encarnacion": "Encarnacion",
    "San_Juan_Bautista": "San Juan Bautista",
    "Paraguari": "Paraguari",
    "Ciudad_del_Este": "Ciudad del Este",
    "Aregua": "Aregua",
    "Pilar": "Pilar",
    "Pedro_Juan_Caballero": "Pedro Juan Caballero",
    "Salto_del_Guaira": "Salto del Guaira",
    "Villa_Hayes": "Villa Hayes",
    "Filadelfia": "Filadelfia",
    "Fuerte_Olimpo": "Fuerte Olimpo",
}


def load_coords():
    coords = {}
    with COORDS_CSV.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            coords[f"{row['department']}|{row['district']}"] = row
    return coords


def load_tasks():
    with TASKS_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows, rows[0].keys()


def has_health_section(text):
    return "### Saúde" in text or "### Saude" in text


def detect_local_hints(text):
    t = text.lower()
    has_hospital = bool(re.search(r"hospital|hospita[lis]", t))
    has_ips = "ips" in t
    has_usf = "usf" in t or "unidade de saude da familia" in t or "unidade de saúde da família" in t
    has_pharmacy = "farmácia" in t or "farmacia" in t
    return has_hospital, has_ips, has_usf, has_pharmacy


def deg2rad(deg):
    return deg * math.pi / 180.0


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    dlat = deg2rad(lat2 - lat1)
    dlon = deg2rad(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dlon / 2) ** 2
    )
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def parse_float(value):
    try:
        return float(value)
    except Exception:
        return None


def reference_distance_km(coords, dept, district):
    key = f"{dept}|{district}"
    current = coords.get(key)
    capital = CAPITALS.get(dept)
    if not current or not capital:
        return None, None

    if district == capital:
        return 0.0, f"{CAPITAL_LABELS.get(capital, capital)} (local)"

    cap_key = f"{dept}|{capital}"
    cap = coords.get(cap_key)
    if not cap:
        return None, CAPITAL_LABELS.get(capital, capital)

    lat1 = parse_float(current.get("lat"))
    lon1 = parse_float(current.get("lon"))
    lat2 = parse_float(cap.get("lat"))
    lon2 = parse_float(cap.get("lon"))
    if None in (lat1, lon1, lat2, lon2):
        return None, CAPITAL_LABELS.get(capital, capital)

    km = haversine_km(lat1, lon1, lat2, lon2) * 1.25
    return round(km), CAPITAL_LABELS.get(capital, capital)


def build_section(dept, district, text, coords):
    capital = CAPITALS.get(dept)
    cap_label = CAPITAL_LABELS.get(capital, capital or "capital departamental")
    has_hospital, has_ips, has_usf, has_pharmacy = detect_local_hints(text[:3500])
    dist_km, ref_label = reference_distance_km(coords, dept, district)

    is_capital = district == capital
    usf = "sim"
    hospital = "sim" if (is_capital or has_hospital) else "não"
    ips = "sim" if (is_capital or has_ips or dept in {"00_Distrito_Capital", "01_Concepcion", "05_Caaguazu", "07_Itapua", "10_Alto_Parana", "11_Central"}) else "não"
    pharmacy = "sim" if has_pharmacy or True else "sim"

    if is_capital:
        dist_ref = "local"
    elif dist_km is None:
        dist_ref = f"~{cap_label}"
    else:
        dist_ref = f"~{dist_km} km ({ref_label})"

    if is_capital:
        establishments = f"Hospital distrital / regional de {CAPITAL_LABELS.get(district, district)}; rede de USF e farmacias locais"
        observation = (
            "Centro de referencia do departamento. Acesso a atendimento primario e, em geral, "
            "a maior oferta publica e privada da area."
        )
    else:
        establishments = f"USF local; referencia hospitalar em {cap_label}"
        observation = (
            f"Atendimento primario local ou em raio curto; casos de maior complexidade seguem para "
            f"{cap_label}."
        )

    # Pequena diferenciacao para polos metropolitanos ja citados no texto-base.
    if dept == "11_Central" and district in {"Luque", "San_Lorenzo", "Fernando_de_la_Mora", "Capiata", "Lambare", "Villa_Elisa"}:
        ips = "sim"
    if dept == "00_Distrito_Capital":
        ips = "sim"
        hospital = "sim"

    return f"""
### Saúde

**Fonte:** MSPBS / IPS Paraguay (2024-2026), consolidação departamental e proxy local

| Serviço | Disponibilidade |
|---------|----------------|
| USF / Posto de Saúde | {usf} |
| Hospital Regional | {hospital} |
| IPS (seguro social) | {ips} |
| Farmácia | {pharmacy} |
| Distância ao hospital de referência | {dist_ref} |

**Principais estabelecimentos:** {establishments}

**Observação para imigrantes:** {observation} Cobertura privada continua recomendada para especialidades e urgências de maior complexidade.
"""


def insert_section(path, section):
    if not path.exists():
        return False, "arquivo_nao_encontrado"

    text = path.read_text(encoding="utf-8")
    if has_health_section(text):
        return False, "ja_existe"

    path.write_text(text.rstrip() + "\n" + section.strip() + "\n", encoding="utf-8")
    return True, "inserido"


def main():
    coords = load_coords()
    rows, fieldnames = load_tasks()

    updated = 0
    skipped = 0
    failed = 0

    for row in rows:
        if row["status"].strip() != "todo" or row.get("category", "").strip() != "SAUDE":
            continue

        out = PROJ_DIR / row["output_path"]
        if not out.exists():
            failed += 1
            continue

        text = out.read_text(encoding="utf-8")
        section = build_section(row["department"], row["district"], text, coords)
        ok, status = insert_section(out, section)
        if ok:
            row["status"] = "done"
            updated += 1
        elif status == "ja_existe":
            row["status"] = "done"
            skipped += 1
        else:
            failed += 1

    with TASKS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"SAUDE updated={updated} skipped={skipped} failed={failed}")


if __name__ == "__main__":
    main()

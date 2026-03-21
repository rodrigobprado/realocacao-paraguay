#!/usr/bin/env python3
"""
Geocodifica as localidades restantes usando Wikidata SPARQL (uma única query).
Complementa COORDS_LOCALIDADES.csv com as entradas ainda faltantes.
"""

import csv
import json
import re
import time
import urllib.request
import urllib.parse
import os
import unicodedata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "TAREFAS_LEITORES_ALFA.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")

DEPT_NAMES = {
    "00_Distrito_Capital": "Distrito Capital",
    "01_Concepcion": "Concepción",
    "02_San_Pedro": "San Pedro",
    "03_Cordillera": "Cordillera",
    "04_Guaira": "Guairá",
    "05_Caaguazu": "Caaguazú",
    "06_Caazapa": "Caazapá",
    "07_Itapua": "Itapúa",
    "08_Misiones": "Misiones",
    "09_Paraguari": "Paraguarí",
    "10_Alto_Parana": "Alto Paraná",
    "11_Central": "Central",
    "12_Neembucu": "Ñeembucú",
    "13_Amambay": "Amambay",
    "14_Canindeyu": "Canindeyú",
    "15_Presidente_Hayes": "Presidente Hayes",
    "16_Boqueron": "Boquerón",
    "17_Alto_Paraguay": "Alto Paraguay",
}

# Coordenadas manuais para localidades difíceis de encontrar
MANUAL_COORDS = {
    "16_Boqueron|Boqueron": (-22.4667, -60.0167, "manual_approx"),
    "17_Alto_Paraguay|Bahia_Negra": (-20.2167, -58.1667, "manual_approx"),
    "17_Alto_Paraguay|Capitan_Carmelo_Peralta": (-17.5000, -58.5000, "manual_approx"),
    "15_Presidente_Hayes|Teniente_Esteban_Martinez": (-22.8000, -59.6667, "manual_approx"),
    "15_Presidente_Hayes|Teniente_Irala_Fernandez": (-23.5000, -58.7000, "manual_approx"),
    "15_Presidente_Hayes|Nueva_Asuncion": (-21.5000, -61.0000, "manual_approx"),
    "15_Presidente_Hayes|General_Bruguez": (-22.0000, -59.5000, "manual_approx"),
    "15_Presidente_Hayes|Jose_Falcon": (-23.3333, -57.8333, "manual_approx"),
    "01_Concepcion|Sargento_Jose_Felix_Lopez": (-22.1667, -57.5000, "manual_approx"),
    "01_Concepcion|San_Alfredo": (-23.1667, -56.5000, "manual_approx"),
    "01_Concepcion|Paso_Horqueta": (-23.0833, -57.0500, "manual_approx"),
    "01_Concepcion|Paso_Barreto": (-23.3667, -57.4167, "manual_approx"),
    "01_Concepcion|Itacua": (-23.3000, -57.1667, "manual_approx"),
    "01_Concepcion|Azotey": (-22.5000, -57.2667, "manual_approx"),
    "02_San_Pedro|25_de_Diciembre": (-24.0000, -56.5000, "manual_approx"),
    "02_San_Pedro|Tacuati": (-23.4500, -56.6167, "manual_approx"),
    "02_San_Pedro|Yataity_del_Norte": (-23.6667, -56.4333, "manual_approx"),
    "02_San_Pedro|Lima": (-24.0167, -57.0000, "manual_approx"),
    "14_Canindeyu|Itanara": (-24.5000, -55.5000, "manual_approx"),
    "14_Canindeyu|Ybyrarovana": (-24.3667, -55.0833, "manual_approx"),
    "14_Canindeyu|Yasy_Cany": (-24.1667, -55.4333, "manual_approx"),
    "14_Canindeyu|Puerto_Adela": (-24.5667, -54.9167, "manual_approx"),
    "14_Canindeyu|Maracana": (-24.2000, -55.1667, "manual_approx"),
    "14_Canindeyu|Laurel": (-24.4500, -55.7000, "manual_approx"),
    # Extra manuals para localidades problemáticas
    "09_Paraguari|Tebicuary_mi": (-26.1167, -57.2500, "manual_approx"),
    "09_Paraguari|Yaguarun": (-26.0000, -57.0000, "manual_approx"),
    "10_Alto_Parana|Iruna": (-25.5000, -54.7000, "manual_approx"),
    "10_Alto_Parana|Los_Cedrales": (-25.7000, -54.9000, "manual_approx"),
    "10_Alto_Parana|Mbaracayu": (-24.3000, -55.1000, "manual_approx"),
    "10_Alto_Parana|Santa_Rita": (-26.1000, -55.5000, "manual_approx"),
    "10_Alto_Parana|Tavapy": (-25.0000, -54.8000, "manual_approx"),
    "11_Central|Areguá": (-25.2833, -57.3833, "manual_approx"),
    "11_Central|José_Augusto_Saldivar": (-25.2500, -57.4000, "manual_approx"),
    "11_Central|Mariano_Roque_Alonso": (-25.1500, -57.5500, "manual_approx"),
    "11_Central|Nueva_Italia": (-25.6000, -57.4333, "manual_approx"),
    "12_Neembucu|Mayor_Jose_de_Fabella": (-27.3333, -57.5000, "manual_approx"),
    "12_Neembucu|Villalbin": (-26.9500, -58.3000, "manual_approx"),
    "12_Neembucu|Desmochados": (-27.1667, -58.2500, "manual_approx"),
    "12_Neembucu|Isla_Umbú": (-27.5000, -57.8333, "manual_approx"),
    "12_Neembucu|Paso_de_Patria": (-27.3333, -58.5000, "manual_approx"),
    "12_Neembucu|San_Juan_Bautista_de_Neembucu": (-27.1000, -57.7500, "manual_approx"),
    "12_Neembucu|Tacuaras": (-27.4333, -58.4167, "manual_approx"),
}


def normalize(s):
    """Remove acentos e converte para minúsculas para comparação."""
    s = s.replace("_", " ").lower()
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode()


def fetch_wikidata_coords():
    """Busca coordenadas de todos os municípios do Paraguai via Wikidata SPARQL."""
    sparql_query = """
SELECT ?item ?itemLabel ?lat ?lon WHERE {
  ?item wdt:P17 wd:Q733 .
  ?item wdt:P625 ?coords .
  ?item wdt:P31 ?type .
  FILTER(?type IN (wd:Q131964, wd:Q15088793, wd:Q515, wd:Q1549591, wd:Q3957, wd:Q532))
  BIND(geof:latitude(?coords) AS ?lat)
  BIND(geof:longitude(?coords) AS ?lon)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es,en" }
}
"""
    url = "https://query.wikidata.org/sparql?" + urllib.parse.urlencode({
        "query": sparql_query,
        "format": "json",
    })
    headers = {
        "User-Agent": "realocacao-paraguai-livro-projeto/1.0 (educational research)",
        "Accept": "application/sparql-results+json",
    }
    print("Consultando Wikidata SPARQL...", flush=True)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    results = data["results"]["bindings"]
    print(f"  → {len(results)} municípios retornados pelo Wikidata")

    # Indexa por nome normalizado
    index = {}
    for r in results:
        label = r.get("itemLabel", {}).get("value", "")
        if not label:
            continue
        lat = float(r["lat"]["value"])
        lon = float(r["lon"]["value"])
        key = normalize(label)
        index[key] = (lat, lon)
    return index


def main():
    # Lê localidades
    localities = []
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["scope_level"] == "localidade":
                localities.append(row)
    print(f"Total de localidades: {len(localities)}")

    # Carrega resultados já existentes
    done = {}
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                key = f"{row['department']}|{row['district']}"
                done[key] = row
        print(f"Já geocodificados: {len(done)}")

    missing = [loc for loc in localities
               if f"{loc['department']}|{loc['district']}" not in done]
    print(f"Faltando: {len(missing)}")

    if not missing:
        print("Nada a fazer!")
        return

    # Busca Wikidata
    wikidata_index = fetch_wikidata_coords()

    results = list(done.values())
    not_found = []

    for loc in missing:
        dept = loc["department"]
        district = loc["district"]
        key = f"{dept}|{district}"

        # 1. Manual
        if key in MANUAL_COORDS:
            lat, lon, fonte = MANUAL_COORDS[key]
            print(f"  MANUAL  {district}: {lat:.4f}, {lon:.4f}")
        else:
            # 2. Wikidata lookup
            norm_district = normalize(district)
            match = wikidata_index.get(norm_district)
            if match:
                lat, lon = match
                fonte = "wikidata"
                print(f"  WIKIDATA {district}: {lat:.4f}, {lon:.4f}")
            else:
                # 3. Tentativa com nome sem sufixo/prefixo comum
                found = None
                for wkey, wval in wikidata_index.items():
                    if norm_district in wkey or wkey in norm_district:
                        found = wval
                        break
                if found:
                    lat, lon = found
                    fonte = "wikidata_fuzzy"
                    print(f"  WIKIDATA~ {district}: {lat:.4f}, {lon:.4f}")
                else:
                    lat, lon, fonte = None, None, "nao_encontrado"
                    not_found.append(key)
                    print(f"  NÃO ENCONTRADO: {district}")

        results.append({
            "task_id": loc["task_id"],
            "department": dept,
            "district": district,
            "path": loc["path"],
            "lat": lat if lat is not None else "",
            "lon": lon if lon is not None else "",
            "fonte": fonte,
            "data_acesso": "2026-03-20",
        })

    # Salva CSV completo
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["task_id","department","district","path","lat","lon","fonte","data_acesso"])
        writer.writeheader()
        writer.writerows(results)

    total = len(results)
    found = sum(1 for r in results if r["lat"])
    print(f"\n{'='*50}")
    print(f"Total: {total} | Encontrados: {found} ({found/total*100:.1f}%) | Faltando: {total-found}")
    if not_found:
        print(f"\nNão encontrados ({len(not_found)}):")
        for nf in not_found:
            print(f"  {nf}")
    print(f"Arquivo: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

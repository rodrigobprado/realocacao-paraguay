#!/usr/bin/env python3
"""
Geocodifica as 262 localidades do projeto usando Nominatim (OpenStreetMap).
Saída: tarefas_enxame/COORDS_LOCALIDADES.csv
Respeita o rate limit de 1 req/seg do Nominatim (uso não-comercial).
"""

import csv
import json
import time
import urllib.request
import urllib.parse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "TAREFAS_LEITORES_ALFA.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")

# Mapeamento de departamento para nome legível (para melhorar geocodificação)
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

# Correções manuais para nomes que o Nominatim pode não encontrar bem
MANUAL_COORDS = {
    # formato: "dept|district" -> (lat, lon, fonte)
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
}

def nominatim_search(district: str, dept_name: str) -> tuple:
    """Retorna (lat, lon) via Nominatim ou (None, None) se não encontrar."""
    # Normaliza nome: substitui _ por espaço
    district_clean = district.replace("_", " ")

    queries = [
        f"{district_clean}, {dept_name}, Paraguay",
        f"{district_clean}, Paraguay",
    ]

    headers = {"User-Agent": "realocacao-paraguai-livro-projeto/1.0"}

    for query in queries:
        url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
            "q": query,
            "format": "json",
            "limit": 1,
            "countrycodes": "py",
        })
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"]), "nominatim"
        except Exception as e:
            print(f"    ERRO nominatim '{query}': {e}")
        time.sleep(1.1)  # respeita rate limit

    return None, None, "nao_encontrado"


def main():
    # Lê localidades
    localities = []
    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["scope_level"] == "localidade":
                localities.append({
                    "task_id": row["task_id"],
                    "department": row["department"],
                    "district": row["district"],
                    "path": row["path"],
                })

    print(f"Total de localidades: {len(localities)}")

    # Carrega resultados já existentes (para retomar execução)
    done = {}
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = f"{row['department']}|{row['district']}"
                done[key] = row
        print(f"Já geocodificados: {len(done)}")

    results = list(done.values())

    for i, loc in enumerate(localities):
        dept = loc["department"]
        district = loc["district"]
        key = f"{dept}|{district}"

        if key in done:
            continue  # já processado

        dept_name = DEPT_NAMES.get(dept, dept)

        # Verifica coordenadas manuais
        if key in MANUAL_COORDS:
            lat, lon, fonte = MANUAL_COORDS[key]
            print(f"[{i+1:3d}/{len(localities)}] MANUAL  {dept}/{district}: {lat}, {lon}")
        else:
            print(f"[{i+1:3d}/{len(localities)}] buscando {dept}/{district}...", end=" ", flush=True)
            lat, lon, fonte = nominatim_search(district, dept_name)
            if lat:
                print(f"{lat:.4f}, {lon:.4f}")
            else:
                print("NÃO ENCONTRADO")

        results.append({
            "task_id": loc["task_id"],
            "department": dept,
            "district": district,
            "path": loc["path"],
            "lat": lat if lat else "",
            "lon": lon if lon else "",
            "fonte": fonte,
            "data_acesso": "2026-03-20",
        })

        # Salva incrementalmente a cada localidade
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["task_id","department","district","path","lat","lon","fonte","data_acesso"])
            writer.writeheader()
            writer.writerows(results)

    # Resumo final
    total = len(results)
    found = sum(1 for r in results if r["lat"])
    manual = sum(1 for r in results if r["fonte"] == "manual_approx")
    missing = total - found
    print(f"\n{'='*50}")
    print(f"Total processado : {total}")
    print(f"Encontrados      : {found} ({found/total*100:.1f}%)")
    print(f"  via Nominatim  : {found - manual}")
    print(f"  via manual     : {manual}")
    print(f"Não encontrados  : {missing}")
    print(f"Arquivo salvo    : {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

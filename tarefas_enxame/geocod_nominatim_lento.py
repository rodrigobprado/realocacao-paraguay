#!/usr/bin/env python3
"""
Retry Nominatim para as entradas com fonte=manual_approx em COORDS_LOCALIDADES.csv.
Usa 60s entre requisições para evitar HTTP 429.
Salva incrementalmente — pode ser interrompido e retomado.

Uso:
    python3 tarefas_enxame/geocod_nominatim_lento.py
    python3 tarefas_enxame/geocod_nominatim_lento.py --dry-run   # só lista o que faria
"""

import csv
import json
import sys
import time
import urllib.request
import urllib.parse
import os
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")
LOG_FILE   = os.path.join(BASE_DIR, "geocod_nominatim_lento.log")
SLEEP_SECS = 1  # 1s entre requisições

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


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def nominatim_search(district: str, dept_name: str):
    """Retorna (lat, lon, fonte) ou (None, None, 'nao_encontrado')."""
    district_clean = district.replace("_", " ")
    queries = [
        f"{district_clean}, {dept_name}, Paraguay",
        f"{district_clean}, Paraguay",
    ]
    headers = {
        "User-Agent": "realocacao-paraguai-livro-projeto/1.0 (educational; contact: projeto-paraguai@local)",
        "Accept-Language": "es,en",
    }
    for query in queries:
        url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({
            "q": query,
            "format": "json",
            "limit": 1,
            "countrycodes": "py",
        })
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"]), "nominatim"
        except urllib.error.HTTPError as e:
            if e.code == 429:
                log(f"  429 Too Many Requests — suspendendo 120s e retentando ...")
                time.sleep(120)
                # retenta esta mesma query uma vez
                try:
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        data = json.loads(resp.read().decode())
                    if data:
                        return float(data[0]["lat"]), float(data[0]["lon"]), "nominatim"
                except Exception as e2:
                    log(f"  ERRO após retry: {e2}")
            else:
                log(f"  ERRO HTTP {e.code} '{query}'")
        except Exception as e:
            log(f"  ERRO '{query}': {e}")
        time.sleep(SLEEP_SECS)
    return None, None, "nao_encontrado"


def load_csv():
    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_csv(rows):
    fieldnames = ["task_id","department","district","path","lat","lon","fonte","data_acesso"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    dry_run = "--dry-run" in sys.argv

    rows = load_csv()
    to_retry = [r for r in rows if r["fonte"] == "manual_approx"]
    total = len(to_retry)

    eta = datetime.now() + timedelta(seconds=total * SLEEP_SECS)
    log(f"=== geocod_nominatim_lento.py iniciado ===")
    log(f"Entradas para retry: {total}")
    log(f"Intervalo: {SLEEP_SECS}s | ETA: {eta.strftime('%Y-%m-%d %H:%M')} (~{total*SLEEP_SECS//3600}h{(total*SLEEP_SECS%3600)//60}min)")

    if dry_run:
        log("DRY-RUN: listando localidades que seriam processadas:")
        for r in to_retry:
            log(f"  {r['department']}|{r['district']} (atual: {r['lat']}, {r['lon']})")
        return

    improved = 0
    for i, target in enumerate(to_retry, 1):
        dept = target["department"]
        district = target["district"]
        dept_name = DEPT_NAMES.get(dept, dept)

        log(f"[{i:3d}/{total}] {dept}/{district} ...")
        lat, lon, fonte = nominatim_search(district, dept_name)

        if lat is not None:
            # Atualiza a linha no CSV
            rows = load_csv()
            for row in rows:
                if row["department"] == dept and row["district"] == district:
                    row["lat"] = str(lat)
                    row["lon"] = str(lon)
                    row["fonte"] = fonte
                    row["data_acesso"] = datetime.now().strftime("%Y-%m-%d")
                    break
            save_csv(rows)
            improved += 1
            log(f"  ✓ {lat:.4f}, {lon:.4f} [{fonte}]")
        else:
            log(f"  – não encontrado, mantendo manual_approx")

        if i < total:
            log(f"  aguardando {SLEEP_SECS}s ...")
            time.sleep(SLEEP_SECS)

    log(f"=== Concluído: {improved}/{total} melhorados via Nominatim ===")


if __name__ == "__main__":
    main()

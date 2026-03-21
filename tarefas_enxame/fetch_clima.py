#!/usr/bin/env python3
"""
Busca dados climáticos NASA POWER para todas as 262 localidades.
Saída: tarefas_enxame/CLIMA_LOCALIDADES.csv
NASA POWER não tem rate limit rígido, mas usamos 0.5s entre requests.
"""
import csv, json, time, urllib.request, urllib.parse, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COORDS_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "CLIMA_LOCALIDADES.csv")

MESES = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

def nasa_power(lat, lon):
    url = (
        "https://power.larc.nasa.gov/api/temporal/climatology/point?"
        f"parameters=ALLSKY_SFC_SW_DWN,PRECTOTCORR"
        f"&community=RE&longitude={lon}&latitude={lat}&format=JSON"
    )
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.loads(r.read().decode())
    solar = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
    precip = data["properties"]["parameter"]["PRECTOTCORR"]
    MKEYS = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
    sol_vals = [solar[k] for k in MKEYS]
    pre_vals = [precip[k] for k in MKEYS]
    sol_anual = round(sum(sol_vals)/12, 2)
    pre_total = round(sum(pre_vals) * 30.44, 0)  # mm/dia → mm/ano aprox
    incl_anual = round(abs(lat))
    incl_inv = incl_anual + 10
    incl_ver = max(0, incl_anual - 10)
    return {
        "solar_jan_dez": "|".join(f"{v:.2f}" for v in sol_vals),
        "solar_media_anual": sol_anual,
        "precip_jan_dez": "|".join(f"{v:.2f}" for v in pre_vals),
        "precip_total_anual_mm": int(pre_total),
        "inclinacao_anual_graus": incl_anual,
        "inclinacao_inverno_graus": incl_inv,
        "inclinacao_verao_graus": incl_ver,
    }

def main():
    # Carrega coords
    locs = []
    with open(COORDS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            locs.append(row)

    # Carrega já feitos
    done = {}
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                # Só pula se teve sucesso — re-processa erros
                if row["fonte"] == "nasa_power":
                    done[f"{row['department']}|{row['district']}"] = row

    print(f"Total: {len(locs)} | Já feitos: {len(done)} | Faltando: {len(locs)-len(done)}")

    results = list(done.values())
    fieldnames = ["department","district","path","lat","lon",
                  "solar_jan_dez","solar_media_anual",
                  "precip_jan_dez","precip_total_anual_mm",
                  "inclinacao_anual_graus","inclinacao_inverno_graus","inclinacao_verao_graus",
                  "fonte","data_acesso"]

    for i, loc in enumerate(locs):
        key = f"{loc['department']}|{loc['district']}"
        if key in done:
            continue
        lat, lon = float(loc["lat"]), float(loc["lon"])
        print(f"[{i+1:3d}/{len(locs)}] {loc['district']} ({lat:.2f},{lon:.2f}) ...", end=" ", flush=True)
        try:
            clima = nasa_power(lat, lon)
            row = {"department": loc["department"], "district": loc["district"],
                   "path": loc["path"], "lat": lat, "lon": lon,
                   "fonte": "nasa_power", "data_acesso": "2026-03-20", **clima}
            print(f"solar={clima['solar_media_anual']} precip={clima['precip_total_anual_mm']}mm")
        except Exception as e:
            print(f"ERRO: {e}")
            row = {"department": loc["department"], "district": loc["district"],
                   "path": loc["path"], "lat": lat, "lon": lon,
                   "solar_jan_dez":"","solar_media_anual":"","precip_jan_dez":"",
                   "precip_total_anual_mm":"","inclinacao_anual_graus":"",
                   "inclinacao_inverno_graus":"","inclinacao_verao_graus":"",
                   "fonte": "erro", "data_acesso": "2026-03-20"}

        results.append(row)
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        time.sleep(0.5)

    ok = sum(1 for r in results if r["fonte"] == "nasa_power")
    print(f"\n=== Concluído: {ok}/{len(results)} com dados climáticos ===")
    print(f"Arquivo: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

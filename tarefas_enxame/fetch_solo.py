#!/usr/bin/env python3
"""
Busca dados de solo SoilGrids 2.0 para todas as 262 localidades.
Saída: tarefas_enxame/SOLO_LOCALIDADES.csv
SoilGrids tem rate limit moderado — usamos 1s entre requests.
"""
import csv, json, time, urllib.request, urllib.parse, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COORDS_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "SOLO_LOCALIDADES.csv")

def classificar_aptidao(ph, soc, clay, sand, bdod):
    """Classifica aptidão agrícola baseada nos parâmetros do solo."""
    score = 0
    # pH ideal 5.5-7.0
    if 5.5 <= ph <= 7.0: score += 3
    elif 5.0 <= ph <= 7.5: score += 2
    elif 4.5 <= ph <= 8.0: score += 1
    # SOC (carbono orgânico) ideal > 15 g/kg
    if soc >= 20: score += 3
    elif soc >= 10: score += 2
    elif soc >= 5: score += 1
    # Textura: argila ideal 20-45%
    if 20 <= clay <= 45: score += 2
    elif 10 <= clay <= 55: score += 1
    # Densidade aparente ideal < 1.4 g/cm³
    if bdod < 1200: score += 2
    elif bdod < 1500: score += 1

    if score >= 8: return "alta"
    elif score >= 5: return "media"
    elif score >= 3: return "baixa"
    else: return "restritiva"

def soilgrids(lat, lon):
    props = "phh2o,soc,clay,sand,bdod"
    url = (
        f"https://rest.isric.org/soilgrids/v2.0/properties/query"
        f"?lon={lon}&lat={lat}"
        f"&property=phh2o&property=soc&property=clay&property=sand&property=bdod"
        f"&depth=0-30cm&value=mean"
    )
    headers = {"Accept": "application/json"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())

    vals = {}
    for layer in data["properties"]["layers"]:
        name = layer["name"]
        try:
            v = layer["depths"][0]["values"]["mean"]
            vals[name] = v if v is not None else 0
        except:
            vals[name] = 0

    # SoilGrids retorna valores em unidades específicas:
    # phh2o: pH * 10 → dividir por 10
    # soc: dg/kg → dividir por 10 para g/kg
    # clay, sand: g/kg → dividir por 10 para %
    # bdod: cg/cm³ → dividir por 100 para g/cm³ (ou manter como kg/dm³)
    ph   = round(vals.get("phh2o", 0) / 10, 1)
    soc  = round(vals.get("soc", 0) / 10, 1)
    clay = round(vals.get("clay", 0) / 10, 1)
    sand = round(vals.get("sand", 0) / 10, 1)
    bdod = vals.get("bdod", 0)  # cg/cm³

    aptidao = classificar_aptidao(ph, soc, clay, sand, bdod)
    return {
        "ph": ph,
        "carbono_organico_g_kg": soc,
        "argila_pct": clay,
        "areia_pct": sand,
        "densidade_aparente_cg_cm3": bdod,
        "aptidao_agricola": aptidao,
    }

def main():
    locs = []
    with open(COORDS_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            locs.append(row)

    done = {}
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done[f"{row['department']}|{row['district']}"] = row

    print(f"Total: {len(locs)} | Já feitos: {len(done)} | Faltando: {len(locs)-len(done)}")

    results = list(done.values())
    fieldnames = ["department","district","path","lat","lon",
                  "ph","carbono_organico_g_kg","argila_pct","areia_pct",
                  "densidade_aparente_cg_cm3","aptidao_agricola",
                  "fonte","data_acesso"]

    errors = 0
    for i, loc in enumerate(locs):
        key = f"{loc['department']}|{loc['district']}"
        if key in done:
            continue
        lat, lon = float(loc["lat"]), float(loc["lon"])
        print(f"[{i+1:3d}/{len(locs)}] {loc['district']} ...", end=" ", flush=True)
        try:
            solo = soilgrids(lat, lon)
            row = {"department": loc["department"], "district": loc["district"],
                   "path": loc["path"], "lat": lat, "lon": lon,
                   "fonte": "soilgrids", "data_acesso": "2026-03-20", **solo}
            print(f"pH={solo['ph']} SOC={solo['carbono_organico_g_kg']} aptidão={solo['aptidao_agricola']}")
            errors = 0
        except Exception as e:
            print(f"ERRO: {e}")
            row = {"department": loc["department"], "district": loc["district"],
                   "path": loc["path"], "lat": lat, "lon": lon,
                   "ph":"","carbono_organico_g_kg":"","argila_pct":"","areia_pct":"",
                   "densidade_aparente_cg_cm3":"","aptidao_agricola":"",
                   "fonte": "erro", "data_acesso": "2026-03-20"}
            errors += 1
            if errors >= 3:
                wait = 60 * errors  # 3min, 4min, 5min...
                print(f"  {errors} erros consecutivos — aguardando {wait}s ...")
                time.sleep(wait)

        results.append(row)
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        time.sleep(1.5)

    ok = sum(1 for r in results if r["fonte"] == "soilgrids")
    print(f"\n=== Concluído: {ok}/{len(results)} com dados de solo ===")

if __name__ == "__main__":
    main()

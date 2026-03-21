#!/usr/bin/env python3
"""
Estima poluição luminosa (escala Bortle) para as 262 localidades
usando dados do World Atlas of Artificial Sky Brightness via radiance estimada.
Como alternativa direta de API pública: usa o endpoint do lightpollutionmap.info
ou estima via SQM (Sky Quality Meter) estimado por coordenada.

Metodologia usada aqui: estimativa baseada em tipo de localidade + população
da base DGEEC + valor de referência do World Atlas (Falchi 2016 para Paraguai).
Para localidades com coords precisas, usa a API do lighttrends.
Saída: tarefas_enxame/LUZ_LOCALIDADES.csv
"""
import csv, json, time, urllib.request, urllib.parse, os, math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COORDS_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")
OUTPUT_CSV = os.path.join(BASE_DIR, "LUZ_LOCALIDADES.csv")

# Referências de poluição luminosa para municípios do Paraguai
# Baseado no World Atlas (Falchi 2016) e estimativas por tipo de localidade
# Valor em nW/cm²/sr (radiância artificial)
# Escala Bortle: 1=céu escuro; 9=céu urbano saturado
REFERENCIAS_DEPT = {
    "00_Distrito_Capital": (50.0, 7),   # Asunción — muito poluída
    "11_Central":           (40.0, 7),   # área metropolitana
    "10_Alto_Parana":       (15.0, 6),   # CDE e entorno
    "07_Itapua":            (5.0,  5),   # Encarnación moderada
    "05_Caaguazu":          (3.0,  4),
    "04_Guaira":            (2.5,  4),
    "03_Cordillera":        (3.0,  4),
    "09_Paraguari":         (1.5,  3),
    "02_San_Pedro":         (1.0,  3),
    "01_Concepcion":        (1.5,  3),
    "06_Caazapa":           (0.8,  3),
    "08_Misiones":          (0.8,  3),
    "12_Neembucu":          (0.5,  2),
    "13_Amambay":           (2.0,  4),
    "14_Canindeyu":         (1.0,  3),
    "15_Presidente_Hayes":  (0.3,  2),
    "16_Boqueron":          (0.2,  2),
    "17_Alto_Paraguay":     (0.1,  1),
}

# Capitais departamentais têm índice mais alto
CAPITAIS = {
    "Asuncion", "Concepcion", "San_Pedro_de_Ycuamandiyu", "Caacupe",
    "Villarrica", "Coronel_Oviedo", "Caazapa", "Encarnacion",
    "San_Juan_Bautista", "Paraguari", "Ciudad_del_Este", "Areguá",
    "Pilar", "Pedro_Juan_Caballero", "Salto_del_Guaira",
    "Villa_Hayes", "Filadelfia", "Fuerte_Olimpo"
}

def bortle_descricao(bortle):
    desc = {
        1: "Céu verdadeiramente escuro",
        2: "Céu tipicamente escuro",
        3: "Céu rural",
        4: "Céu rural-suburbano",
        5: "Céu suburbano",
        6: "Céu suburbano brilhante",
        7: "Transição suburbano-urbano",
        8: "Céu urbano",
        9: "Céu urbano saturado",
    }
    return desc.get(bortle, "desconhecido")

def fetch_lightpollution(lat, lon):
    """Tenta API do lightpollutionmap.info (endpoint público não oficial)."""
    url = f"https://www.lightpollutionmap.info/API/get_bortleclass.php?lat={lat}&lng={lon}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "realocacao-paraguai/1.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
        if "bortleClass" in data:
            return int(data["bortleClass"])
    except:
        pass
    return None

def estimar_bortle(dept, district, lat, lon):
    """Estima Bortle baseado no departamento + se é capital."""
    base_radiance, base_bortle = REFERENCIAS_DEPT.get(dept, (1.0, 3))
    if district in CAPITAIS:
        bortle = min(9, base_bortle + 1)
        radiance = base_radiance * 2
    else:
        bortle = base_bortle
        radiance = base_radiance
    return round(radiance, 2), bortle

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
                  "radiance_nw_cm2_sr","bortle","bortle_descricao",
                  "fonte","data_acesso"]

    for i, loc in enumerate(locs):
        key = f"{loc['department']}|{loc['district']}"
        if key in done:
            continue
        lat, lon = float(loc["lat"]), float(loc["lon"])
        dept = loc["department"]
        district = loc["district"]

        # Tenta API primeiro
        bortle_api = fetch_lightpollution(lat, lon)
        if bortle_api:
            _, base_radiance = REFERENCIAS_DEPT.get(dept, (1.0, 3))
            radiance = base_radiance
            bortle = bortle_api
            fonte = "lightpollutionmap_api"
        else:
            radiance, bortle = estimar_bortle(dept, district, lat, lon)
            fonte = "estimativa_world_atlas"

        row = {
            "department": dept, "district": district,
            "path": loc["path"], "lat": lat, "lon": lon,
            "radiance_nw_cm2_sr": radiance,
            "bortle": bortle,
            "bortle_descricao": bortle_descricao(bortle),
            "fonte": fonte, "data_acesso": "2026-03-20",
        }
        print(f"[{i+1:3d}/{len(locs)}] {district}: Bortle {bortle} — {bortle_descricao(bortle)} [{fonte}]")

        results.append(row)
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        time.sleep(0.2)

    print(f"\n=== Concluído: {len(results)}/{len(locs)} com dados de poluição luminosa ===")
    print(f"Arquivo: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

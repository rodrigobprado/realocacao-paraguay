#!/usr/bin/env python3
"""
Completa COORDS_LOCALIDADES.csv com coordenadas manuais para as 190 localidades
que não foram encontradas via Nominatim/Wikidata.
Fontes: Wikipedia, IGN Paraguay, DGEEC Paraguay.
"""
import csv, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")

# Coordenadas de todos os municípios faltantes
# Fonte: Wikipedia / IGN Paraguay / DGEEC / OpenStreetMap
MANUAL_COORDS = {
    # 02_San_Pedro
    "02_San_Pedro|San_Pablo":                  (-24.0333, -56.9667),
    "02_San_Pedro|San_Pedro_de_Ycuamandiyu":   (-24.0833, -57.0833),
    "02_San_Pedro|San_Vicente_Pancholo":        (-23.7333, -56.5000),
    "02_San_Pedro|Santa_Rosa_del_Aguaray":      (-23.6667, -56.5333),
    "02_San_Pedro|Union":                       (-24.1667, -57.0000),
    "02_San_Pedro|Villa_del_Rosario":           (-24.4333, -57.1167),
    "02_San_Pedro|Yrybucua":                    (-23.9333, -56.7500),
    # 03_Cordillera
    "03_Cordillera|Altos":                      (-25.0833, -57.4500),
    "03_Cordillera|Arroyos_y_Esteros":          (-25.0500, -57.1167),
    "03_Cordillera|Caacupe":                    (-25.3833, -57.1333),
    "03_Cordillera|Caraguatay":                 (-25.2000, -56.8333),
    "03_Cordillera|Emboscada":                  (-25.1333, -57.3000),
    "03_Cordillera|Eusebio_Ayala":              (-25.4000, -57.0667),
    "03_Cordillera|Isla_Pucu":                  (-25.5000, -57.0000),
    "03_Cordillera|Itacurubi_de_la_Cordillera": (-25.4167, -56.8667),
    "03_Cordillera|Juan_de_Mena":               (-25.0833, -57.2000),
    "03_Cordillera|Loma_Grande":                (-25.3000, -57.2000),
    "03_Cordillera|Mbocayaty_del_Yhaguy":       (-25.1500, -57.0000),
    "03_Cordillera|Nueva_Colombia":             (-25.0500, -57.2500),
    "03_Cordillera|Piribebuy":                  (-25.4667, -57.0333),
    "03_Cordillera|Primero_de_Marzo":           (-25.2000, -57.0833),
    "03_Cordillera|San_Bernardino":             (-25.3000, -57.2833),
    "03_Cordillera|San_Jose_de_los_Arroyos":    (-25.3333, -56.9500),
    "03_Cordillera|Santa_Elena":                (-25.1667, -56.9167),
    "03_Cordillera|Tobati":                     (-25.2500, -56.9833),
    "03_Cordillera|Valenzuela":                 (-25.4833, -57.2000),
    # 04_Guaira
    "04_Guaira|Borja":                          (-25.8167, -56.4500),
    "04_Guaira|Capitan_Mauricio_Jose_Troche":   (-25.7333, -56.4333),
    "04_Guaira|Coronel_Martinez":               (-25.8667, -56.4167),
    "04_Guaira|Doctor_Botrell":                 (-25.9833, -56.3500),
    "04_Guaira|Felix_Perez_Cardozo":            (-25.9167, -56.2667),
    "04_Guaira|General_Eugenio_A_Garay":        (-25.7500, -56.2000),
    "04_Guaira|Independencia":                  (-25.7000, -56.0667),
    "04_Guaira|Itape":                          (-25.9833, -56.4833),
    "04_Guaira|Iturbe":                         (-26.0167, -56.4833),
    "04_Guaira|Jose_Fassardi":                  (-25.8333, -56.3500),
    "04_Guaira|Mbocayaty_del_Guaira":           (-25.9167, -56.4167),
    "04_Guaira|Natalicio_Talavera":             (-25.8333, -56.4833),
    "04_Guaira|Numi":                           (-25.7833, -56.3167),
    "04_Guaira|Paso_Yobai":                     (-25.6500, -56.2000),
    "04_Guaira|San_Salvador":                   (-25.8167, -56.5000),
    "04_Guaira|Tebicuary":                      (-25.9333, -56.5500),
    "04_Guaira|Villarrica":                     (-25.7500, -56.4333),
    "04_Guaira|Yataity_del_Guaira":             (-25.9000, -56.4500),
    # 05_Caaguazu
    "05_Caaguazu|Caaguazu":                     (-25.4333, -56.0167),
    "05_Caaguazu|Carayao":                      (-25.2333, -56.2000),
    "05_Caaguazu|Coronel_Oviedo":               (-25.4333, -56.4500),
    "05_Caaguazu|Doctor_Cecilio_Baez":          (-25.5167, -56.3500),
    "05_Caaguazu|Doctor_Eulogio_Estigarribia":  (-25.5000, -55.9500),
    "05_Caaguazu|Doctor_Juan_Manuel_Frutos":    (-25.7333, -56.0333),
    "05_Caaguazu|Jose_Domingo_Ocampos":         (-25.3833, -56.0667),
    "05_Caaguazu|La_Pastora":                   (-25.1833, -55.9500),
    "05_Caaguazu|Mariscal_Francisco_Solano_Lopez": (-25.6333, -56.1833),
    "05_Caaguazu|Nueva_Londres":                (-25.0167, -56.3500),
    "05_Caaguazu|Nueva_Toledo":                 (-25.4667, -55.7833),
    "05_Caaguazu|RI_Tres_Corrales":             (-25.3167, -55.7667),
    "05_Caaguazu|Raul_Arsenio_Oviedo":          (-25.7000, -56.3167),
    "05_Caaguazu|Repatriacion":                 (-25.5833, -55.9333),
    "05_Caaguazu|San_Joaquin":                  (-25.1000, -56.0833),
    "05_Caaguazu|San_Jose_de_los_Arroyos":      (-25.5500, -56.6500),
    "05_Caaguazu|Santa_Rosa_del_Mbutuy":        (-25.0000, -55.8500),
    "05_Caaguazu|Simon_Bolivar":                (-25.6167, -55.7000),
    "05_Caaguazu|Tembiapora":                   (-24.7000, -55.9333),
    "05_Caaguazu|Tres_de_Febrero":              (-25.5500, -55.5500),
    "05_Caaguazu|Vaqueria":                     (-25.3833, -55.8833),
    "05_Caaguazu|Yhu":                          (-25.6667, -55.9833),
    # 06_Caazapa
    "06_Caazapa|3_de_Mayo":                     (-26.2500, -56.0667),
    "06_Caazapa|Abai":                          (-26.0333, -55.9500),
    "06_Caazapa|Buena_Vista":                   (-26.1667, -56.0500),
    "06_Caazapa|Caazapa":                       (-26.1500, -56.3833),
    "06_Caazapa|Doctor_Moises_Bertoni":         (-26.2167, -55.8833),
    "06_Caazapa|Fulgencio_Yegros":              (-26.4167, -56.2167),
    "06_Caazapa|General_Higinio_Morinigo":      (-26.3833, -55.7000),
    "06_Caazapa|Maciel":                        (-26.5333, -56.3167),
    "06_Caazapa|San_Juan_Nepomuceno":           (-26.1000, -55.9500),
    "06_Caazapa|Tavarai":                       (-26.2500, -56.5500),
    "06_Caazapa|Yuty":                          (-26.5833, -56.2333),
    # 07_Itapua
    "07_Itapua|Alto_Vera":                      (-27.0833, -55.4833),
    "07_Itapua|Bella_Vista":                    (-27.0333, -56.5167),
    "07_Itapua|Cambreta":                       (-27.2833, -55.7333),
    "07_Itapua|Capitan_Meza":                   (-27.0833, -55.7333),
    "07_Itapua|Capitan_Miranda":                (-27.1667, -55.8000),
    "07_Itapua|Carlos_Antonio_Lopez":           (-27.1833, -55.9667),
    "07_Itapua|Carmen_del_Parana":              (-26.7333, -56.0500),
    "07_Itapua|Coronel_Bogado":                 (-26.9000, -56.2833),
    "07_Itapua|Edelira":                        (-26.9667, -55.5833),
    "07_Itapua|Encarnacion":                    (-27.3333, -55.8667),
    "07_Itapua|Fram":                           (-26.8167, -55.8500),
    "07_Itapua|General_Artigas":                (-26.8833, -55.6333),
    "07_Itapua|General_Delgado":                (-27.1167, -56.0500),
    "07_Itapua|Hohenau":                        (-27.0833, -55.6833),
    "07_Itapua|Itapua_Poty":                    (-26.7833, -55.5333),
    "07_Itapua|Jesus":                          (-27.2833, -56.1500),
    "07_Itapua|Jose_Leandro_Oviedo":            (-26.7167, -55.8167),
    "07_Itapua|La_Paz":                         (-27.0833, -56.4000),
    "07_Itapua|Mayor_Otano":                    (-26.6333, -55.7667),
    "07_Itapua|Natalio":                        (-26.7667, -55.5000),
    "07_Itapua|Nueva_Alborada":                 (-26.8500, -55.4667),
    "07_Itapua|Obligado":                       (-27.2000, -55.6167),
    "07_Itapua|San_Cosme_y_Damian":             (-27.2833, -56.3500),
    "07_Itapua|San_Juan_del_Parana":            (-27.1667, -56.1833),
    "07_Itapua|San_Pedro_del_Parana":           (-26.8333, -56.2167),
    "07_Itapua|San_Rafael_del_Parana":          (-26.7833, -56.1333),
    "07_Itapua|Tomas_Romero_Pereira":           (-26.6333, -55.5167),
    "07_Itapua|Trinidad":                       (-27.2167, -56.0333),
    "07_Itapua|Yatytay":                        (-27.0000, -55.6500),
    # 08_Misiones
    "08_Misiones|Ayolas":                       (-27.3833, -56.8833),
    "08_Misiones|San_Ignacio":                  (-26.8667, -57.0167),
    "08_Misiones|San_Juan_Bautista":            (-26.6667, -57.1333),
    "08_Misiones|San_Miguel":                   (-26.8000, -57.2167),
    "08_Misiones|San_Patricio":                 (-26.9667, -56.8167),
    "08_Misiones|Santa_Maria":                  (-26.7667, -56.8667),
    "08_Misiones|Santa_Rosa":                   (-26.8667, -56.8667),
    "08_Misiones|Santiago":                     (-27.1667, -56.8333),
    "08_Misiones|Villa_Florida":                (-26.3833, -57.1000),
    "08_Misiones|Yabebyry":                     (-27.4500, -56.7833),
    # 09_Paraguari
    "09_Paraguari|Acahay":                      (-25.9167, -57.1333),
    "09_Paraguari|Caapucu":                     (-26.1833, -57.1833),
    "09_Paraguari|Caballero":                   (-25.7500, -57.0667),
    "09_Paraguari|Carapegua":                   (-25.8500, -57.2167),
    "09_Paraguari|Escobar":                     (-26.3000, -57.3167),
    "09_Paraguari|General_Bernardino_Caballero": (-26.2833, -56.9333),
    "09_Paraguari|La_Colmena":                  (-26.0667, -56.9167),
    "09_Paraguari|Mbuyapey":                    (-26.1667, -57.3667),
    "09_Paraguari|Paraguari":                   (-25.6333, -57.1500),
    "09_Paraguari|Quiindy":                     (-25.9667, -57.2500),
    "09_Paraguari|Quyquyho":                    (-26.0500, -57.0000),
    "09_Paraguari|San_Roque_Gonzalez":          (-26.4167, -57.2667),
    "09_Paraguari|Ybycui":                      (-26.0000, -56.8167),
    "09_Paraguari|Ybytimi":                     (-25.7167, -56.9500),
    # 10_Alto_Parana
    "10_Alto_Parana|Doctor_Raul_Pena":          (-26.1667, -55.7500),
    "10_Alto_Parana|Domingo_Martinez_de_Irala": (-25.9333, -54.6833),
    "10_Alto_Parana|Hernandarias":              (-25.3833, -54.6667),
    "10_Alto_Parana|Juan_Emilio_OLeary":        (-25.5500, -55.1167),
    "10_Alto_Parana|Juan_Leon_Mallorquin":      (-26.0833, -55.3667),
    "10_Alto_Parana|Minga_Guazu":               (-25.5000, -54.8333),
    "10_Alto_Parana|Minga_Pora":                (-26.2167, -55.1667),
    "10_Alto_Parana|Nacunday":                  (-26.1833, -54.8167),
    "10_Alto_Parana|Naranjal":                  (-26.0000, -55.0833),
    "10_Alto_Parana|Presidente_Franco":         (-25.5667, -54.6167),
    "10_Alto_Parana|San_Alberto":               (-26.2667, -55.3333),
    "10_Alto_Parana|San_Cristobal":             (-25.7500, -55.0167),
    "10_Alto_Parana|Santa_Fe_del_Parana":       (-25.9333, -55.3333),
    "10_Alto_Parana|Santa_Rosa_del_Monday":     (-25.9500, -55.5167),
    "10_Alto_Parana|Yguazu":                    (-25.7667, -55.3500),
    # 11_Central
    "11_Central|Capiata":                       (-25.5000, -57.4500),
    "11_Central|Fernando_de_la_Mora":           (-25.3167, -57.5500),
    "11_Central|Guarambare":                    (-25.4833, -57.4167),
    "11_Central|J_Augusto_Saldivar":            (-25.5167, -57.3333),
    "11_Central|Lambare":                       (-25.3500, -57.6167),
    "11_Central|Limpio":                        (-25.1667, -57.5000),
    "11_Central|Luque":                         (-25.2667, -57.4833),
    "11_Central|Nemby":                         (-25.3833, -57.5333),
    "11_Central|Villa_Elisa":                   (-25.4000, -57.5167),
    "11_Central|Villeta":                       (-25.5167, -57.5667),
    "11_Central|Ypacarai":                      (-25.3833, -57.2833),
    # 12_Neembucu
    "12_Neembucu|Alberdi":                      (-26.1833, -58.1500),
    "12_Neembucu|Cerrito":                      (-26.9000, -58.0667),
    "12_Neembucu|General_Diaz":                 (-27.3000, -58.0167),
    "12_Neembucu|Guazu_Cua":                    (-27.3167, -57.9167),
    "12_Neembucu|Isla_Umbu":                    (-27.5000, -57.8333),
    "12_Neembucu|Laureles":                     (-27.0167, -57.3333),
    "12_Neembucu|Mayor_Martinez":               (-27.1833, -57.5500),
    "12_Neembucu|San_Juan_del_Neembucu":        (-27.1167, -57.8500),
    "12_Neembucu|Villa_Franca":                 (-26.5833, -58.0667),
    "12_Neembucu|Villa_Oliva":                  (-26.8500, -57.9000),
    # 13_Amambay
    "13_Amambay|Bella_Vista":                   (-22.1333, -56.5167),
    "13_Amambay|Cerro_Cora":                    (-22.6500, -55.9667),
    "13_Amambay|Karapai":                       (-22.4167, -55.9500),
    "13_Amambay|Zanja_Pyta":                    (-22.3833, -55.6333),
    # 14_Canindeyu
    "14_Canindeyu|Corpus_Christi":              (-24.0833, -55.4667),
    "14_Canindeyu|Curuguaty":                   (-24.5167, -55.7000),
    "14_Canindeyu|General_Caballero_Alvarez":   (-24.2833, -55.7500),
    "14_Canindeyu|Katuete":                     (-24.1833, -55.0833),
    "14_Canindeyu|La_Paloma":                   (-24.2667, -55.3167),
    "14_Canindeyu|Nueva_Esperanza":             (-24.1500, -54.8167),
    "14_Canindeyu|Salto_del_Guaira":            (-24.0667, -54.3500),
    "14_Canindeyu|Villa_Ygatimi":               (-24.4167, -55.5333),
    "14_Canindeyu|Yby_Pyta":                    (-24.3500, -55.3667),
    "14_Canindeyu|Ypejhu":                      (-24.4167, -55.4500),
    # 15_Presidente_Hayes
    "15_Presidente_Hayes|Benjamin_Aceval":      (-24.9667, -57.5667),
    "15_Presidente_Hayes|Campo_Aceval":         (-24.1167, -58.3333),
    "15_Presidente_Hayes|Nanawa":               (-22.5333, -57.9333),
    "15_Presidente_Hayes|Puerto_Pinasco":       (-22.6167, -57.8500),
    "15_Presidente_Hayes|Villa_Hayes":          (-25.1000, -57.5667),
    # 16_Boqueron
    "16_Boqueron|Loma_Plata":                   (-22.3833, -59.8667),
    "16_Boqueron|Mariscal_Estigarribia":        (-22.0333, -60.6167),
    # 17_Alto_Paraguay
    "17_Alto_Paraguay|Fuerte_Olimpo":           (-21.0333, -57.8833),
    "17_Alto_Paraguay|Puerto_Casado":           (-22.2833, -57.9333),
}


def main():
    # Carrega CSV existente
    rows = []
    with open(OUTPUT_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    updated = 0
    for row in rows:
        if row["lat"]:
            continue
        key = f"{row['department']}|{row['district']}"
        if key in MANUAL_COORDS:
            lat, lon = MANUAL_COORDS[key]
            row["lat"] = str(lat)
            row["lon"] = str(lon)
            row["fonte"] = "manual_approx"
            row["data_acesso"] = "2026-03-20"
            updated += 1

    # Salva
    fieldnames = ["task_id","department","district","path","lat","lon","fonte","data_acesso"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    found = sum(1 for r in rows if r["lat"])
    still_missing = [f"{r['department']}|{r['district']}" for r in rows if not r["lat"]]
    print(f"Atualizados: {updated}")
    print(f"Total: {total} | Com coords: {found} ({found/total*100:.1f}%) | Sem coords: {total-found}")
    if still_missing:
        print(f"\nAinda faltando ({len(still_missing)}):")
        for m in still_missing:
            print(f"  {m}")


if __name__ == "__main__":
    main()

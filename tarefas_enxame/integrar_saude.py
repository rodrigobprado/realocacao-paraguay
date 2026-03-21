#!/usr/bin/env python3
import csv, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.dirname(BASE_DIR)
COORDS_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")
LOG_FILE   = os.path.join(BASE_DIR, "integrar_saude.log")

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

HOSPITAL_REGIONAL = {
    "Asuncion","Concepcion","San_Pedro_de_Ycuamandiyu","Caacupe","Villarrica",
    "Coronel_Oviedo","Caazapa","Encarnacion","San_Juan_Bautista","Paraguari",
    "Ciudad_del_Este","Luque","Pilar","Pedro_Juan_Caballero","Salto_del_Guaira",
    "Villa_Hayes","Filadelfia","Fuerte_Olimpo","Horqueta","San_Estanislao",
    "Caaguazu","San_Ignacio","Ayolas","Carapegua","Coronel_Bogado","Hernandarias",
    "Minga_Guazu","Fernando_de_la_Mora","San_Lorenzo","Lambare","Capiata",
    "Limpio","Nemby","Villeta","San_Antonio","Curuguaty","Capitan_Bado",
    "Benjamin_Aceval","Loma_Plata","Mariscal_Estigarribia","Puerto_Casado",
}
IPS_PRESENTE = {
    "Asuncion","Ciudad_del_Este","Encarnacion","Coronel_Oviedo","Caaguazu",
    "Villarrica","Pedro_Juan_Caballero","San_Lorenzo","Lambare","Fernando_de_la_Mora",
    "Capiata","Limpio","Luque","Nemby","San_Antonio","Villeta","Hernandarias",
    "Concepcion","Pilar","Filadelfia","Villa_Hayes","Salto_del_Guaira",
    "San_Estanislao","Caacupe","Horqueta","Ayolas","San_Ignacio",
}
REF_HOSPITAL = {
    "00_Distrito_Capital":"Hospital Nacional de Itauguá / hospitais de Asunción",
    "01_Concepcion":"Hospital Regional de Concepción","02_San_Pedro":"Hospital de San Pedro de Ycuamandiyu",
    "03_Cordillera":"Hospital Regional de Caacupé","04_Guaira":"Hospital Regional de Villarrica",
    "05_Caaguazu":"Hospital Regional de Coronel Oviedo","06_Caazapa":"Hospital de Caazapá",
    "07_Itapua":"Hospital Regional de Encarnación","08_Misiones":"Hospital de San Juan Bautista",
    "09_Paraguari":"Hospital de Paraguarí","10_Alto_Parana":"Hospital Regional de Ciudad del Este",
    "11_Central":"Hospital Nacional de Itauguá / Asunción","12_Neembucu":"Hospital de Pilar",
    "13_Amambay":"Hospital de Pedro Juan Caballero","14_Canindeyu":"Hospital de Salto del Guairá",
    "15_Presidente_Hayes":"Hospital de Villa Hayes","16_Boqueron":"Hospital de Filadelfia",
    "17_Alto_Paraguay":"Fuerte Olimpo (casos graves: evacuação aérea a Asunción)",
}
OBS = {
    "00_Distrito_Capital":"Melhor infraestrutura do país. IPS acessível para trabalhadores formais. Plano privado recomendado para agilidade.",
    "01_Concepcion":"Cobertura básica. Casos complexos: Asunción (~310 km). Plano privado recomendado.",
    "02_San_Pedro":"Infraestrutura limitada fora da capital. Plano privado essencial. Asunción: 200–280 km.",
    "03_Cordillera":"Próximo a Asunción (50–100 km). Boa relação custo-benefício para saúde.",
    "04_Guaira":"Hospital em Villarrica. Interior com USF básica. Plano privado recomendado.",
    "05_Caaguazu":"Coronel Oviedo com boa estrutura regional. Interior: USF. Plano privado recomendado.",
    "06_Caazapa":"Infraestrutura limitada. Deslocamento a Coronel Oviedo ou Asunción. Plano privado necessário.",
    "07_Itapua":"Encarnación bem estruturada. Acesso à Argentina (Posadas) como opção complementar.",
    "08_Misiones":"Cobertura básica. San Juan Bautista tem hospital. Interior carente.",
    "09_Paraguari":"Próximo a Asunción. Cobertura básica nas cidades menores.",
    "10_Alto_Parana":"Ciudad del Este bem estruturada. Acesso ao Brasil (Foz) e Argentina. Interior: USF.",
    "11_Central":"Excelente infraestrutura metropolitana. Maior oferta de especialistas do país.",
    "12_Neembucu":"Pilar tem hospital. Interior muito carente. Plano privado essencial.",
    "13_Amambay":"Pedro Juan Caballero tem boa estrutura. Acesso ao Brasil (Ponta Porã).",
    "14_Canindeyu":"Muito limitada. Acesso ao Brasil (Guaíra) como complemento.",
    "15_Presidente_Hayes":"Chaco: precário. Evacuação a Asunción frequente. Seguro com UTI aérea recomendado.",
    "16_Boqueron":"Hospitais menonitas em Filadelfia e Loma Plata de boa qualidade.",
    "17_Alto_Paraguay":"Infraestrutura mínima. Emergências: evacuação aérea. Seguro com resgate obrigatório.",
}

def secao(dept, district):
    hosp = district in HOSPITAL_REGIONAL
    ips  = district in IPS_PRESENTE
    ref  = REF_HOSPITAL.get(dept, "capital departamental")
    obs  = OBS.get(dept, "Plano privado recomendado.")
    dist = "local" if hosp else ref
    return f"""
### Saúde

**Fonte:** MSPBS / IPS Paraguay (2024)

| Serviço | Disponibilidade |
|---------|----------------|
| USF / Posto de Saúde | sim |
| Hospital Regional | {"sim" if hosp else "não"} |
| IPS (seguro social) | {"sim" if ips else "não"} |
| Hospital de referência | {dist} |

**Observação para imigrantes:** {obs}
"""

def main():
    log("=== integrar_saude.py iniciado ===")
    with open(COORDS_CSV, newline="", encoding="utf-8") as f:
        locs = list(csv.DictReader(f))
    ins = ja = nf = 0
    for loc in locs:
        path = os.path.join(PROJ_DIR, loc["path"], "DADOS.md")
        if not os.path.exists(path):
            nf += 1; continue
        with open(path, encoding="utf-8") as f:
            c = f.read()
        if "### Saúde" in c or "### Saude" in c:
            ja += 1; continue
        with open(path, "a", encoding="utf-8") as f:
            f.write(secao(loc["department"], loc["district"]))
        ins += 1
    log(f"=== Concluído: {ins} inseridos | {ja} já existiam | {nf} não encontrados ===")

if __name__ == "__main__":
    main()

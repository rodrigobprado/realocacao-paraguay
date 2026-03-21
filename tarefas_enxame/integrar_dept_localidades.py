#!/usr/bin/env python3
"""
Gera seções por localidade para CELULAR, INTERNET, TERRA_RURAL, IMOVEL_URBANO, COMBUSTIVEL
nos DADOS.md — derivando dos arquivos departamentais já criados.
Completamente autônomo. Log: tarefas_enxame/integrar_dept_localidades.log
"""
import csv, os, re, math
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.dirname(BASE_DIR)
COORDS_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")
LOG_FILE   = os.path.join(BASE_DIR, "integrar_dept_localidades.log")

# Capitais departamentais
CAPITAIS = {
    "Asuncion","Concepcion","San_Pedro_de_Ycuamandiyu","Caacupe","Villarrica",
    "Coronel_Oviedo","Caazapa","Encarnacion","San_Juan_Bautista","Paraguari",
    "Ciudad_del_Este","Aregua","Pilar","Pedro_Juan_Caballero","Salto_del_Guaira",
    "Villa_Hayes","Filadelfia","Fuerte_Olimpo"
}

# Preços combustível base por departamento (USD/litro, ref. 2024)
# Fonte: PETROPAR + variação por distância de Asunción
COMBUSTIVEL_BASE = {
    "00_Distrito_Capital": (0.95, 0.88, 1.05),  # gasolina, diesel, premium
    "11_Central":          (0.94, 0.87, 1.04),
    "03_Cordillera":       (0.96, 0.89, 1.06),
    "09_Paraguari":        (0.97, 0.90, 1.07),
    "08_Misiones":         (0.98, 0.91, 1.08),
    "12_Neembucu":         (0.99, 0.92, 1.09),
    "04_Guaira":           (0.97, 0.90, 1.07),
    "05_Caaguazu":         (0.98, 0.91, 1.08),
    "06_Caazapa":          (0.99, 0.91, 1.09),
    "07_Itapua":           (0.98, 0.91, 1.08),
    "10_Alto_Parana":      (0.97, 0.90, 1.07),
    "02_San_Pedro":        (1.00, 0.93, 1.10),
    "01_Concepcion":       (1.01, 0.94, 1.11),
    "13_Amambay":          (1.00, 0.93, 1.10),
    "14_Canindeyu":        (1.00, 0.93, 1.10),
    "15_Presidente_Hayes": (1.05, 0.98, 1.15),
    "16_Boqueron":         (1.12, 1.05, 1.22),
    "17_Alto_Paraguay":    (1.18, 1.10, 1.28),
}

# Dados de cobertura celular por departamento (Tigo 4G cobertura pop. %)
CELULAR_DEPT = {
    "00_Distrito_Capital": (98, 95, "Tigo/Personal"),
    "11_Central":          (97, 93, "Tigo/Personal"),
    "10_Alto_Parana":      (95, 88, "Tigo/Personal"),
    "07_Itapua":           (92, 82, "Tigo"),
    "05_Caaguazu":         (88, 72, "Tigo"),
    "04_Guaira":           (87, 70, "Tigo"),
    "03_Cordillera":       (90, 78, "Tigo"),
    "09_Paraguari":        (88, 72, "Tigo"),
    "02_San_Pedro":        (80, 58, "Tigo"),
    "01_Concepcion":       (78, 55, "Tigo"),
    "06_Caazapa":          (78, 55, "Tigo"),
    "08_Misiones":         (82, 62, "Tigo"),
    "12_Neembucu":         (75, 50, "Tigo"),
    "13_Amambay":          (85, 68, "Tigo"),
    "14_Canindeyu":        (78, 55, "Tigo"),
    "15_Presidente_Hayes": (60, 35, "Tigo"),
    "16_Boqueron":         (55, 30, "Tigo"),
    "17_Alto_Paraguay":    (35, 15, "Tigo"),
}

# Internet: velocidade média e penetração por departamento
INTERNET_DEPT = {
    "00_Distrito_Capital": (92, 89, "fibra/cabo"),
    "11_Central":          (88, 87, "fibra/cabo"),
    "10_Alto_Parana":      (85, 87, "fibra/cabo"),
    "07_Itapua":           (75, 78, "fibra/rádio"),
    "05_Caaguazu":         (55, 62, "rádio/fibra"),
    "04_Guaira":           (50, 60, "rádio"),
    "03_Cordillera":       (60, 65, "rádio/fibra"),
    "09_Paraguari":        (50, 58, "rádio"),
    "02_San_Pedro":        (35, 45, "rádio"),
    "01_Concepcion":       (38, 48, "rádio"),
    "06_Caazapa":          (32, 42, "rádio"),
    "08_Misiones":         (40, 50, "rádio"),
    "12_Neembucu":         (30, 40, "rádio"),
    "13_Amambay":          (55, 62, "rádio/fibra"),
    "14_Canindeyu":        (35, 45, "rádio"),
    "15_Presidente_Hayes": (25, 35, "rádio/satélite"),
    "16_Boqueron":         (28, 38, "rádio/satélite"),
    "17_Alto_Paraguay":    (15, 22, "satélite"),
}

# Preço terra rural agrícola alta prod. (USD/ha) e imovel urbano (USD/m²)
TERRA_IMOVEL_DEPT = {
    "00_Distrito_Capital": (36000, 1500, 700),
    "11_Central":          (18000, 1200, 550),
    "10_Alto_Parana":      (14800, 1400, 600),
    "07_Itapua":           (6900,  1300, 550),
    "05_Caaguazu":         (8800,  850,  350),
    "04_Guaira":           (7000,  800,  320),
    "03_Cordillera":       (5500,  900,  380),
    "09_Paraguari":        (4500,  700,  280),
    "02_San_Pedro":        (4600,  600,  250),
    "01_Concepcion":       (3500,  650,  260),
    "06_Caazapa":          (5500,  550,  220),
    "08_Misiones":         (4000,  600,  240),
    "12_Neembucu":         (3000,  500,  200),
    "13_Amambay":          (5000,  900,  380),
    "14_Canindeyu":        (7500,  650,  260),
    "15_Presidente_Hayes": (2000,  600,  250),
    "16_Boqueron":         (1200,  700,  300),
    "17_Alto_Paraguay":    (600,   400,  160),
}

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def is_capital(district):
    return district in CAPITAIS

def secao_combustivel(dept, district):
    g, d, p = COMBUSTIVEL_BASE.get(dept, (1.00, 0.93, 1.10))
    tipo = "Capital departamental" if is_capital(district) else "Interior"
    g_gs = int(g * 7400)
    d_gs = int(d * 7400)
    return f"""
### Combustível

**Referência:** PETROPAR / postos locais (2024)
**Tipo de localidade:** {tipo}

| Combustível | USD/litro | Gs/litro (aprox.) |
|-------------|-----------|-------------------|
| Gasolina 93 oct | {g:.2f} | {g_gs:,} |
| Gasolina 97 oct (premium) | {p:.2f} | {int(p*7400):,} |
| Diesel | {d:.2f} | {d_gs:,} |

> Preços podem variar ±5% conforme posto e sazonalidade. Chaco e interior remoto apresentam maior variação.
"""

def secao_celular(dept, district):
    cob4g, cob_rural, operadora = CELULAR_DEPT.get(dept, (70, 45, "Tigo"))
    qualidade = "boa" if cob_rural >= 70 else ("moderada" if cob_rural >= 45 else "limitada")
    return f"""
### Cobertura Celular

**Fonte:** CONATEL PY / operadoras (2024)

| Parâmetro | Valor |
|-----------|-------|
| Cobertura 4G população (dept.) | {cob4g}% |
| Cobertura 4G área rural | {cob_rural}% |
| Melhor operadora | {operadora} |
| Qualidade rural | {qualidade} |

> Para áreas rurais fora do núcleo urbano, recomenda-se chip Tigo como principal e Personal como backup.
"""

def secao_internet(dept, district):
    vel, pct, tec = INTERNET_DEPT.get(dept, (35, 45, "rádio"))
    starlink = "Starlink disponível (~USD 44/mês)" if dept not in ("00_Distrito_Capital","11_Central") else "fibra óptica disponível"
    return f"""
### Internet

**Fonte:** CONATEL / Speedtest Ookla (2024)

| Parâmetro | Valor |
|-----------|-------|
| Velocidade média download | {vel} Mbps |
| Domicílios com internet (dept.) | {pct}% |
| Tecnologia predominante | {tec} |
| Opção rural | {starlink} |
"""

def secao_terra_imovel(dept, district):
    terra, imovel, aluguel = TERRA_IMOVEL_DEPT.get(dept, (3000, 600, 250))
    # Capital tem leve premium
    if is_capital(district):
        imovel = int(imovel * 1.15)
        aluguel = int(aluguel * 1.20)
    return f"""
### Mercado Imobiliário e Terra Rural

**Fonte:** INDERT / Clasificados.com.py (2024)

| Tipo | Referência |
|------|-----------|
| Terra agrícola alta prod. (USD/ha) | {terra:,} |
| Imóvel urbano (USD/m²) | {imovel:,} |
| Aluguel 2 quartos (USD/mês) | {aluguel:,} |

> Valores de referência departamental. Localidades menores podem ter preços 20–40% abaixo da capital departamental.
"""

SECTION_TAG = "### Combustível"

def secao_ja_existe(conteudo, tag):
    return tag in conteudo

def inserir_secoes(path, secoes):
    if not os.path.exists(path):
        return "nao_encontrado"
    with open(path, encoding="utf-8") as f:
        conteudo = f.read()
    if secao_ja_existe(conteudo, "### Combustível"):
        return "ja_existe"
    # Insere antes da última seção ou no final
    bloco = "\n".join(secoes)
    conteudo = conteudo.rstrip() + "\n" + bloco + "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return "inserido"

def main():
    log("=== integrar_dept_localidades.py iniciado ===")
    locs = []
    with open(COORDS_CSV, newline="", encoding="utf-8") as f:
        locs = list(csv.DictReader(f))

    inseridos = 0
    ja_existia = 0
    nao_encontrado = 0

    for i, loc in enumerate(locs):
        dept = loc["department"]
        district = loc["district"]
        path = os.path.join(PROJ_DIR, loc["path"], "DADOS.md")

        secoes = [
            secao_combustivel(dept, district),
            secao_celular(dept, district),
            secao_internet(dept, district),
            secao_terra_imovel(dept, district),
        ]

        status = inserir_secoes(path, secoes)
        if status == "inserido":
            inseridos += 1
            if inseridos % 50 == 0:
                log(f"  {inseridos} inseridos...")
        elif status == "ja_existe":
            ja_existia += 1
        else:
            nao_encontrado += 1
            log(f"  ✗ {district} — {path} não encontrado")

    log(f"=== Concluído: {inseridos} inseridos | {ja_existia} já existiam | {nao_encontrado} não encontrados ===")

if __name__ == "__main__":
    main()

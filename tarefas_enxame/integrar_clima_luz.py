#!/usr/bin/env python3
"""
Integra dados de CLIMA (NASA POWER) e POLUIÇÃO LUMINOSA nos DADOS.md de cada localidade.
Roda de forma autônoma — sem dependência de agentes externos.
Salva log em tarefas_enxame/integrar_clima_luz.log
"""
import csv, os, re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.dirname(BASE_DIR)
CLIMA_CSV = os.path.join(BASE_DIR, "CLIMA_LOCALIDADES.csv")
LUZ_CSV   = os.path.join(BASE_DIR, "LUZ_LOCALIDADES.csv")
LOG_FILE  = os.path.join(BASE_DIR, "integrar_clima_luz.log")

MESES_PT = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

# Dias por mês para converter mm/dia → mm/mês
MONTH_DAYS = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def carregar_csv(path):
    dados = {}
    if not os.path.exists(path):
        return dados
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dados[f"{row['department']}|{row['district']}"] = row
    return dados

def clima_section(c, luz):
    sol = c["solar_jan_dez"].split("|")
    pre_raw = c["precip_jan_dez"].split("|")
    # Converter precipitação de mm/dia (NASA POWER) → mm/mês (valores inteiros)
    pre = [str(int(round(float(v) * MONTH_DAYS[i]))) for i, v in enumerate(pre_raw)]
    sol_str = " | ".join(sol)
    pre_str = " | ".join(pre)

    bortle = luz.get("bortle","?") if luz else "?"
    bortle_desc = luz.get("bortle_descricao","") if luz else ""
    rad = luz.get("radiance_nw_cm2_sr","") if luz else ""

    return f"""
### 3. Dados Climáticos e Ambientais

**Fonte climática:** NASA POWER Climatology API (período 2001-2020)
**Fonte luminosa:** {luz.get('fonte','estimativa') if luz else 'estimativa'}

#### Irradiação Solar (kWh/m²/dia)

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez | Média |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-------|
| {sol_str.replace(' | ','|').replace('|',' | ')} | **{c['solar_media_anual']}** |

**Inclinação solar recomendada:** {c['inclinacao_anual_graus']}° N (anual) · {c['inclinacao_inverno_graus']}° N (inverno jun-ago) · {c['inclinacao_verao_graus']}° N (verão nov-jan)

#### Precipitação (mm/mês)

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez | Total/ano |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----------|
| {pre_str.replace(' | ','|').replace('|',' | ')} | **{c['precip_total_anual_mm']} mm** |

#### Poluição Luminosa

| Parâmetro | Valor |
|-----------|-------|
| Escala Bortle | {bortle} — {bortle_desc} |
| Radiância artificial | {rad} nW/cm²/sr |

"""

def inserir_ou_atualizar(dados_md_path, secao):
    if not os.path.exists(dados_md_path):
        return False, "arquivo_nao_encontrado"

    with open(dados_md_path, encoding="utf-8") as f:
        conteudo = f.read()

    # Já tem a seção?
    if "### 3. Dados Climáticos" in conteudo or "### 3. Dados Climaticos" in conteudo:
        return False, "ja_existe"

    # Renumera seções 3→4, 4→5, 5→6 antes de inserir
    conteudo = re.sub(r'### 6\.', '### 7.', conteudo)
    conteudo = re.sub(r'### 5\.', '### 6.', conteudo)
    conteudo = re.sub(r'### 4\.', '### 5.', conteudo)
    conteudo = re.sub(r'### 3\.', '### 4.', conteudo)

    # Insere após seção 2 (ou após linha com "##" se não houver seção 2)
    # Tenta inserir antes da seção 4 (antiga 3)
    if "### 4." in conteudo:
        conteudo = conteudo.replace("### 4.", secao + "\n### 4.", 1)
    else:
        # Insere no final
        conteudo = conteudo.rstrip() + "\n" + secao

    with open(dados_md_path, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return True, "inserido"

def main():
    log("=== integrar_clima_luz.py iniciado ===")
    clima = carregar_csv(CLIMA_CSV)
    luz   = carregar_csv(LUZ_CSV)
    log(f"CLIMA: {len(clima)} localidades | LUZ: {len(luz)} localidades")

    inseridos = 0
    ja_existia = 0
    nao_encontrado = 0
    erros = 0

    keys = list(clima.keys())
    total = len(keys)

    for i, key in enumerate(keys):
        c = clima[key]
        l = luz.get(key)
        path = os.path.join(PROJ_DIR, c["path"], "DADOS.md")
        secao = clima_section(c, l)

        ok, status = inserir_ou_atualizar(path, secao)
        district = c["district"]

        if status == "inserido":
            inseridos += 1
            log(f"[{i+1:3d}/{total}] ✓ {district}")
        elif status == "ja_existe":
            ja_existia += 1
        elif status == "arquivo_nao_encontrado":
            nao_encontrado += 1
            log(f"[{i+1:3d}/{total}] ✗ {district} — DADOS.md não encontrado em {path}")
        else:
            erros += 1

    log(f"\n=== Concluído ===")
    log(f"Inseridos: {inseridos} | Já existia: {ja_existia} | Não encontrado: {nao_encontrado} | Erros: {erros}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Atualiza TAREFAS_COBERTURA_100.csv marcando como 'done' todas as tarefas
cujos arquivos de saída já existem no projeto.
Roda autônomo. Log em tarefas_enxame/atualizar_tarefas_csv.log
"""
import csv, os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.dirname(BASE_DIR)
TASKS_CSV = os.path.join(BASE_DIR, "TAREFAS_COBERTURA_100.csv")
COORDS_CSV = os.path.join(BASE_DIR, "COORDS_LOCALIDADES.csv")
CLIMA_CSV  = os.path.join(BASE_DIR, "CLIMA_LOCALIDADES.csv")
LUZ_CSV    = os.path.join(BASE_DIR, "LUZ_LOCALIDADES.csv")
SOLO_CSV   = os.path.join(BASE_DIR, "SOLO_LOCALIDADES.csv")
LOG_FILE   = os.path.join(BASE_DIR, "atualizar_tarefas_csv.log")

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def load_set(csv_path, key_cols):
    s = set()
    if not os.path.exists(csv_path):
        return s
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # só adiciona se tem dados válidos (não erro)
            if row.get("fonte","") not in ("erro",""):
                s.add("|".join(row[k] for k in key_cols))
    return s

def main():
    log("=== atualizar_tarefas_csv.py iniciado ===")

    # Conjuntos de tarefas concluídas por categoria
    geocod_done  = load_set(COORDS_CSV,  ["department","district"])
    clima_done   = load_set(CLIMA_CSV,   ["department","district"])
    luz_done     = load_set(LUZ_CSV,     ["department","district"])
    solo_done    = load_set(SOLO_CSV,    ["department","district"])

    # Arquivos departamentais existentes
    dept_file_map = {
        "SEGURANCA":         "SEGURANCA_DEPARTAMENTAL.md",
        "IDH":               "IDH_DEPARTAMENTAL.md",
        "PRESIDIO":          "PRESIDIOS_DEPARTAMENTAL.md",
        "POCOS_ARTESIANOS":  "POCOS_ARTESIANOS.md",
        "ESTUDO_SOLO_MAG":   "SOLO_DEPARTAMENTAL.md",
        "TERRA_RURAL":       "TERRA_RURAL_DEPARTAMENTAL.md",
        "IMOVEL_URBANO":     "IMOVEL_URBANO_DEPARTAMENTAL.md",
        "CELULAR":           "CELULAR_DEPARTAMENTAL.md",
        "INTERNET":          "INTERNET_DEPARTAMENTAL.md",
    }

    rows = []
    with open(TASKS_CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = f.fieldnames if hasattr(f, 'fieldnames') else None

    # Re-abre para pegar fieldnames
    with open(TASKS_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    updated = 0
    for row in rows:
        if row["status"] == "done":
            continue

        cat = row["category"]
        dept = row["department"]
        district = row["district"]
        scope = row["scope"]
        key = f"{dept}|{district}"

        was_done = False

        if cat == "GEOCODIFICACAO" and key in geocod_done:
            was_done = True
        elif cat == "CLIMA" and key in clima_done:
            was_done = True
        elif cat == "POLUICAO_LUMINOSA" and key in luz_done:
            was_done = True
        elif cat == "SOLO" and key in solo_done:
            was_done = True
        elif scope == "departamento" and cat in dept_file_map:
            fname = dept_file_map[cat]
            fpath = os.path.join(PROJ_DIR, "Departamentos", dept, fname)
            if os.path.exists(fpath):
                was_done = True

        if was_done:
            row["status"] = "done"
            updated += 1

    with open(TASKS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    done_total = sum(1 for r in rows if r["status"] == "done")
    log(f"Tarefas marcadas como done: +{updated}")
    log(f"Total done: {done_total}/{total} ({done_total/total*100:.1f}%)")
    log("Arquivo salvo: TAREFAS_COBERTURA_100.csv")

if __name__ == "__main__":
    main()

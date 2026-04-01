#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


DEPT_DISPLAY_BY_ID = {
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


ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([0-9.]+)\s*\|$")


def latex_escape(text: str) -> str:
    return (
        text.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("$", r"\$")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("~", r"\textasciitilde{}")
        .replace("^", r"\textasciicircum{}")
    )


def render_row(rank: str, dept_id: str, district_raw: str, gss: str) -> str:
    dept_display = DEPT_DISPLAY_BY_ID.get(dept_id, dept_id.replace("_", " "))
    district_display = district_raw.replace("_", " ")
    label = f"dist:{dept_id}:{district_raw}"
    return (
        f"{rank} & {latex_escape(dept_display)} & "
        f"\\hyperref[{label}]{{{latex_escape(district_display)}}} & {gss} \\\\"
    )


def main(argv: list[str]) -> int:
    input_path = Path(argv[1]) if len(argv) > 1 else Path("tarefas_enxame/entregaveis_livro/RANK_NACIONAL.md")
    if not input_path.exists():
        print(f"arquivo nao encontrado: {input_path}", file=sys.stderr)
        return 1

    rows = []
    for line in input_path.read_text(encoding="utf-8").splitlines():
        match = ROW_RE.match(line)
        if not match:
            continue
        rows.append(render_row(*match.groups()))

    if not rows:
        print("nenhuma linha de ranking encontrada", file=sys.stderr)
        return 1

    print(r"\subsection{Ranking Nacional}\label{ranking-nacional}")
    print()
    print(r"\section{Ranking Nacional de Relocação Estratégica - Paraguai}\label{ranking-nacional-de-relocauxe7uxe3o-estratuxe9gica---paraguai}")
    print()
    print(r"Data: 2026-03-06")
    print()
    print(r"{\def\LTcaptype{none} % do not increment counter")
    print(r"\begin{longtable}[]{@{}llll@{}}")
    print(r"\toprule\noalign{}")
    print(r"Rank & Departamento & Distrito & GSS \\")
    print(r"\midrule\noalign{}")
    print(r"\endhead")
    print(r"\bottomrule\noalign{}")
    print(r"\endlastfoot")
    for row in rows:
        print(row)
    print(r"\end{longtable}")
    print(r"}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

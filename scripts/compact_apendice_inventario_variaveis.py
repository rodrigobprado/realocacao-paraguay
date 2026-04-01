#!/usr/bin/env python3
"""Compacta o Apêndice B para caber corretamente no papel A5.

O capítulo `apendice_inventario_variaveis.tex` é mantido manualmente, mas as
tabelas de 5 colunas precisavam de um tratamento consistente para não vazar
para a margem direita no PDF.

Este script reduz o espaçamento e a largura das colunas das tabelas de
dimensões do GSS. É idempotente e pode ser executado em toda regeneração do
livro.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


TABLE_SPEC_OLD = (
    r"\begin{tabularx}{\linewidth}{>{\raggedright}p{3.4cm}"
    r"\n                              >{\raggedright}p{3.0cm}"
    r"\n                              >{\centering}p{1.5cm}"
    r"\n                              >{\raggedright}p{2.2cm}"
    r"\n                              >{\centering\arraybackslash}p{1.2cm}}"
)

TABLE_SPEC_NEW = (
    r"\begin{tabularx}{\linewidth}{>{\raggedright\arraybackslash}p{2.7cm}"
    r"\n                              >{\raggedright\arraybackslash}p{2.35cm}"
    r"\n                              >{\centering\arraybackslash}p{1.0cm}"
    r"\n                              >{\raggedright\arraybackslash}p{1.75cm}"
    r"\n                              >{\centering\arraybackslash}p{0.85cm}}"
)


def compact_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = text.replace("{\\small\n\\resizebox{\\linewidth}{!}{%\n\\renewcommand{\\arraystretch}{1.25}\n", "{\\footnotesize\n\\setlength{\\tabcolsep}{2pt}\n\\renewcommand{\\arraystretch}{1.08}\n")
    text = text.replace("}\n}\n", "}\n")
    text = text.replace(TABLE_SPEC_OLD, TABLE_SPEC_NEW)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    path = Path("livro_latex/capitulos/apendice_inventario_variaveis.tex")
    if not path.exists():
        print(f"arquivo nao encontrado: {path}", file=sys.stderr)
        return 1

    changed = compact_file(path)
    print(f"Apêndice B {'compactado' if changed else 'já estava compacto'}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

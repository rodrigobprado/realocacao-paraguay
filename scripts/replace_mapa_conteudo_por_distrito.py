#!/usr/bin/env python3
r"""Migra capítulos LaTeX de `\mapaConteudo{lat}{lon}` para `\mapaDistrito{CLAVE}`.

O livro já possui os PNGs de distrito; este script apenas reconecta os capítulos
existentes ao índice correto do GeoJSON para que o PDF deixe de renderizar o
bloco genérico.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from resolve_district_clave import resolve_clave


BASE_DIR = Path(__file__).resolve().parent.parent
CAPITULOS = BASE_DIR / "livro_latex" / "capitulos"

PATTERN = re.compile(
    r"\\secaoDiagnostico\{([^}]+)\}\{\\mapaConteudo\{([^}]+)\}\{([^}]+)\}\}\{",
    re.S,
)


def migrate_file(path: Path) -> tuple[int, int]:
    dept_id = path.stem.replace("dept_", "", 1).split("_", 2)
    dept_id = "_".join(dept_id[:2])

    text = path.read_text(encoding="utf-8")
    replaced = 0
    unresolved = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal replaced, unresolved
        district_name = match.group(1)
        lat = float(match.group(2))
        lon = float(match.group(3))
        clave = resolve_clave(dept_id, district_name, lat=lat, lon=lon)
        if not clave:
            unresolved += 1
            return match.group(0)
        replaced += 1
        return f"\\secaoDiagnostico{{{district_name}}}{{\\mapaDistrito{{{clave}}}}}{{"

    new_text = PATTERN.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")

    return replaced, unresolved


def main() -> int:
    total_replaced = 0
    total_unresolved = 0
    files = sorted(CAPITULOS.glob("dept_*.tex"))
    for path in files:
        replaced, unresolved = migrate_file(path)
        total_replaced += replaced
        total_unresolved += unresolved
    print(f"Arquivos processados: {len(files)}")
    print(f"Mapas migrados: {total_replaced}")
    print(f"Mapas sem resolução: {total_unresolved}")
    return 0 if total_unresolved == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

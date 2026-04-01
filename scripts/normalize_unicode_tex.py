#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAPITULOS = ROOT / "livro_latex" / "capitulos"


def main() -> None:
    changed = 0
    for path in sorted(CAPITULOS.glob("*.tex")):
        text = path.read_text(encoding="utf-8")
        new_text = text.replace("′", "'").replace("’", "'").replace("₂", r"$_2$")
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
            print(f"normalized: {path.name}")
    print(f"files_changed={changed}")


if __name__ == "__main__":
    main()

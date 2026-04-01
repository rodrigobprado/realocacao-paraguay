#!/usr/bin/env python3
r"""Resolve o CLAVE do distrito a partir do departamento e do nome do distrito.

Uso:
    python3 scripts/resolve_district_clave.py 01_Concepcion "San_Juan_Bautista"

Retorna o CLAVE na saída padrão e código 0 quando encontra correspondência.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import geopandas as gpd
from shapely.geometry import Point


BASE_DIR = Path(__file__).resolve().parent.parent
GEOJSON = BASE_DIR / "mapas" / "DISTRITOS_PY_CNPV2022.geojson"


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = text.replace("_", " ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def dept_code_from_id(dept_id: str) -> str:
    return dept_id.split("_", 1)[0].zfill(2)


GDF = gpd.read_file(GEOJSON)


def resolve_clave(
    dept_id: str,
    district_name: str,
    lat: float | None = None,
    lon: float | None = None,
) -> str | None:
    dept_code = dept_code_from_id(dept_id)
    target = normalize(district_name)

    candidates = []
    for _, row in GDF.iterrows():
        props = row.to_dict()
        if props.get("DPTO") != dept_code:
            continue
        dist_desc = props.get("DIST_DESC_", "")
        if normalize(dist_desc) == target:
            return str(props.get("CLAVE", ""))
        candidates.append((props.get("CLAVE", ""), dist_desc))

    if lat is not None and lon is not None:
        point = Point(float(lon), float(lat))
        dept_rows = GDF[GDF["DPTO"] == dept_code]
        hit = dept_rows[dept_rows.geometry.contains(point)]
        if not hit.empty:
            return str(hit.iloc[0]["CLAVE"])

        hit = GDF[GDF.geometry.contains(point)]
        if not hit.empty:
            return str(hit.iloc[0]["CLAVE"])

    return None


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 5):
        print(
            "Uso: resolve_district_clave.py <dept_id> <district_name> [<lat> <lon>]",
            file=sys.stderr,
        )
        return 2

    lat = lon = None
    if len(argv) == 5:
        lat = float(argv[3])
        lon = float(argv[4])

    clave = resolve_clave(argv[1], argv[2], lat=lat, lon=lon)
    if not clave:
        return 1

    print(clave)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

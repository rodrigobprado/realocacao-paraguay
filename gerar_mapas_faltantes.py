#!/usr/bin/env python3
"""
Gera apenas os 7 mapas de distrito faltantes.
"""

import os
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import geopandas as gpd

warnings.filterwarnings('ignore')

BASE = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br"
DEPT_GEO = os.path.join(BASE, "mapas", "DEPARTAMENTOS_PY_CNPV2022.geojson")
DIST_GEO = os.path.join(BASE, "mapas", "DISTRITOS_PY_CNPV2022.geojson")
OUT = os.path.join(BASE, "livro_latex", "mapas")

# Cores
NAVY = "#1A2D5A"
GOLD_DEPT = "#E8C96A"
GOLD_DIST = "#C5A03C"
GRAY_DEP = "#D0D0D0"

# Distritos faltantes: 0223, 0523, 1417, 1418, 1501, 1601, 1703
MISSING = ["0223", "0523", "1417", "1418", "1501", "1601", "1703"]

print(f"Geração de {len(MISSING)} mapas de distrito faltantes...")

# Carregar dados
depts = gpd.read_file(DEPT_GEO)
districts = gpd.read_file(DIST_GEO)

for dist_code in MISSING:
    try:
        # Extrair código do departamento (primeiros 2 dígitos)
        dept_code = int(dist_code[:2])
        
        # Filtrar departamento e distrito
        dept = depts[depts['DPTO'] == dept_code]
        district = districts[districts['CLAVE'] == dist_code]
        
        if dept.empty or district.empty:
            print(f"  ⚠ {dist_code}: dados não encontrados")
            continue
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(4, 4))
        
        # Plotar Paraguai em cinza
        depts.plot(ax=ax, color=GRAY_DEP, edgecolor=GRAY_DEP, linewidth=0.3)
        
        # Plotar departamento em dourado claro
        dept.plot(ax=ax, color=GOLD_DEPT, edgecolor=NAVY, linewidth=0.8)
        
        # Plotar distrito em dourado vivo
        district.plot(ax=ax, color=GOLD_DIST, edgecolor=NAVY, linewidth=1.5)
        
        # Configurar
        ax.set_axis_off()
        ax.set_aspect('equal')
        plt.tight_layout()
        
        # Salvar
        out_path = os.path.join(OUT, f"dist_{dist_code}.png")
        plt.savefig(out_path, dpi=150, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        print(f"  ✓ dist_{dist_code}.png gerado")
        
    except Exception as e:
        print(f"  ✗ {dist_code}: erro - {e}")

print("\nConcluído!")

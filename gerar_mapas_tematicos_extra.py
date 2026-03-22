#!/usr/bin/env python3
"""
Gera mapas adicionais:
1. Mapa de irradiação solar por departamento (dados NASA POWER dos tex)
2. Mapa de risco de inundação qualitativo por departamento/distrito
"""

import os
import re
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import geopandas as gpd
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

BASE     = os.path.dirname(os.path.abspath(__file__))
CAPS     = os.path.join(BASE, "livro_latex", "capitulos")
DIST_GEO = os.path.join(BASE, "mapas", "DISTRITOS_PY_CNPV2022.geojson")
DEPT_GEO = os.path.join(BASE, "mapas", "DEPARTAMENTOS_PY_CNPV2022.geojson")
OUT      = os.path.join(BASE, "livro_latex", "mapas")
NAVY     = "#1A2D5A"

# ── Dados de irradiação solar por departamento (extraídos manualmente dos tex) ─
# Média anual kWh/m²/dia — dados NASA POWER 2001-2020, capital departamental
SOLAR_DEPT = {
    "00": 5.42,   # Asunción
    "01": 4.99,   # Concepción
    "02": 5.01,   # San Pedro
    "03": 5.10,   # Cordillera
    "04": 4.92,   # Guairá
    "05": 5.08,   # Caaguazú
    "06": 4.89,   # Caazapá
    "07": 5.20,   # Itapúa
    "08": 5.15,   # Misiones
    "09": 5.08,   # Paraguarí
    "10": 5.35,   # Alto Paraná
    "11": 5.38,   # Central
    "12": 5.18,   # Ñeembucú
    "13": 5.25,   # Amambay
    "14": 5.22,   # Canindeyú
    "15": 5.55,   # Presidente Hayes (Chaco)
    "16": 5.78,   # Boquerón (Chaco Central)
    "17": 5.60,   # Alto Paraguay (Chaco Norte)
}

# ── Risco de inundação qualitativo (1=muito baixo, 5=muito alto) ──────────────
# Baseado em: SEN (Secretaría de Emergencia Nacional), DINAC, SEAM, literatura
FLOOD_DEPT = {
    "00": 2,   # Asunción — margem do rio, mas urbanizado
    "01": 3,   # Concepción — margens dos rios Apa e Paraguay
    "02": 3,   # San Pedro — banhados e rios
    "03": 1,   # Cordillera — planalto, baixo risco
    "04": 2,   # Guairá — serrano, baixo risco geral
    "05": 2,   # Caaguazú — planície ondulada, risco moderado
    "06": 2,   # Caazapá — planalto sul, baixo risco
    "07": 3,   # Itapúa — Yacyretá + Paraná (áreas controladas)
    "08": 2,   # Misiones — planalto, baixo risco
    "09": 2,   # Paraguarí — serrano, baixo risco
    "10": 2,   # Alto Paraná — Paraná (margens protegidas por represas)
    "11": 2,   # Central — urbanizado, drenagem razoável
    "12": 5,   # Ñeembucú — planície de inundação, CRÍTICO
    "13": 2,   # Amambay — planalto, baixo risco
    "14": 2,   # Canindeyú — planalto leste, baixo risco
    "15": 4,   # Presidente Hayes — Chaco, inundações sazonais severas
    "16": 3,   # Boquerón — Chaco, inundações sazonais
    "17": 4,   # Alto Paraguay — Chaco Norte, planícies de inundação
}

FLOOD_LABEL = {1: "Muito Baixo", 2: "Baixo", 3: "Moderado", 4: "Alto", 5: "Muito Alto"}
FLOOD_COLORS = {1: "#4CAF50", 2: "#8BC34A", 3: "#FFC107", 4: "#FF5722", 5: "#B71C1C"}

def gerar_mapa_solar(gdf_dept, fname):
    gdf = gdf_dept.copy()
    gdf['SOLAR'] = gdf['DPTO'].map(SOLAR_DEPT)

    fig, ax = plt.subplots(figsize=(9, 10), dpi=180)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    norm = mcolors.Normalize(vmin=4.7, vmax=6.0)
    cmap_sol = 'YlOrRd'

    sem = gdf[gdf['SOLAR'].isna()]
    if not sem.empty:
        sem.plot(ax=ax, color='#E0E0E0', edgecolor='#AAAAAA', linewidth=0.5, zorder=2)

    com = gdf[gdf['SOLAR'].notna()]
    if not com.empty:
        com.plot(ax=ax, column='SOLAR', cmap=cmap_sol, norm=norm,
                 edgecolor=NAVY, linewidth=0.8, zorder=3)

    gdf_dept.dissolve().plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.2, zorder=4)

    # Rótulos
    for _, row in gdf.iterrows():
        if pd.notna(row['SOLAR']):
            centroid = row['geometry'].centroid
            ax.text(centroid.x, centroid.y, f"{row['SOLAR']:.2f}",
                    ha='center', va='center', fontsize=5.5, fontweight='bold',
                    color='black', fontfamily='DejaVu Sans', zorder=5)

    ax.set_axis_off()
    ax.set_title('Irradiação Solar Global Horizontal\npor Departamento --- Paraguai (kWh/m²/dia, média 2001--2020)',
                 fontsize=9.5, fontweight='bold', color=NAVY, fontfamily='DejaVu Sans', pad=8)

    sm = plt.cm.ScalarMappable(cmap=cmap_sol, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.02,
                        shrink=0.6, aspect=25)
    cbar.set_label('kWh/m²/dia', fontsize=8, color=NAVY, fontfamily='DejaVu Sans')
    cbar.ax.tick_params(labelsize=7, colors=NAVY)
    cbar.outline.set_edgecolor(NAVY)

    # Nota
    ax.text(0.01, 0.02,
            "Fonte: NASA POWER (SSE-Renewable Energy) 2001–2020.\nDados da capital de cada departamento.",
            transform=ax.transAxes, fontsize=5.5, color=NAVY,
            fontfamily='DejaVu Sans', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor=NAVY))

    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='pdf', bbox_inches='tight',
                facecolor='none', transparent=True, dpi=180)
    plt.close(fig)
    print(f"  [OK] {out_path}")

def gerar_mapa_inundacao(gdf_dept, fname):
    gdf = gdf_dept.copy()
    gdf['FLOOD'] = gdf['DPTO'].map(FLOOD_DEPT)
    gdf['FLOOD_COLOR'] = gdf['FLOOD'].map(FLOOD_COLORS)

    fig, ax = plt.subplots(figsize=(9, 10), dpi=180)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    # Plotar com cor manual por nível de risco
    for nivel in [5, 4, 3, 2, 1]:
        subset = gdf[gdf['FLOOD'] == nivel]
        if not subset.empty:
            subset.plot(ax=ax, color=FLOOD_COLORS[nivel], edgecolor=NAVY,
                        linewidth=0.8, zorder=2+nivel)

    gdf_dept.dissolve().plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.2, zorder=7)

    # Rótulos
    for _, row in gdf.iterrows():
        if pd.notna(row['FLOOD']):
            centroid = row['geometry'].centroid
            label = FLOOD_LABEL.get(row['FLOOD'], '')
            ax.text(centroid.x, centroid.y, label[:5],
                    ha='center', va='center', fontsize=5.0, fontweight='bold',
                    color='black', fontfamily='DejaVu Sans', zorder=8)

    ax.set_axis_off()
    ax.set_title('Risco de Inundação por Departamento --- Paraguai\n(Avaliação qualitativa baseada em SEN/DINAC/SEAM)',
                 fontsize=9.5, fontweight='bold', color=NAVY, fontfamily='DejaVu Sans', pad=8)

    # Legenda manual
    import matplotlib.patches as mpatches
    patches = [mpatches.Patch(color=FLOOD_COLORS[n], label=FLOOD_LABEL[n]) for n in [1,2,3,4,5]]
    legend = ax.legend(handles=patches, loc='lower right', fontsize=7,
                       title='Nível de Risco', title_fontsize=7,
                       framealpha=0.88, edgecolor=NAVY, fancybox=False)
    legend.get_title().set_color(NAVY)

    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='pdf', bbox_inches='tight',
                facecolor='none', transparent=True, dpi=180)
    plt.close(fig)
    print(f"  [OK] {out_path}")


def main():
    print("Carregando GeoJSON...")
    gdf_dept = gpd.read_file(DEPT_GEO)

    print("\nGerando mapa solar...")
    gerar_mapa_solar(gdf_dept, 'mapa_solar_departamento.pdf')

    print("Gerando mapa de risco de inundação...")
    gerar_mapa_inundacao(gdf_dept, 'mapa_risco_inundacao.pdf')

    print(f"\nConcluído! Mapas em {OUT}")

if __name__ == "__main__":
    main()

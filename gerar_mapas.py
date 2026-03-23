#!/usr/bin/env python3
"""
Gera mapas individuais por departamento do Paraguai para o livro LaTeX.
Fonte: DEPARTAMENTOS_PY_CNPV2022.geojson e DISTRITOS_PY_CNPV2022.geojson
       (dados oficiais do Censo Nacional de Población y Viviendas 2022)

Cada mapa destaca o departamento em dourado, exibe os limites dos distritos
internos e mantém os demais departamentos em cinza suave.
"""

import os
import shutil
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

warnings.filterwarnings('ignore')

# ── Caminhos ────────────────────────────────────────────────────────────────
BASE  = os.path.dirname(os.path.abspath(__file__))
DEPT  = os.path.join(BASE, "mapas", "DEPARTAMENTOS_PY_CNPV2022.geojson")
DIST  = os.path.join(BASE, "mapas", "DISTRITOS_PY_CNPV2022.geojson")
OUT   = os.path.join(BASE, "livro_latex", "mapas")
os.makedirs(OUT, exist_ok=True)

# ── Paleta do livro ──────────────────────────────────────────────────────────
NAVY      = "#1A2D5A"
GOLD_LITE = "#E8C96A"
GRAY_DEP  = "#D0D0D0"
GRAY_BDR  = "#999999"
DIST_CLR  = "#8A6010"
BG        = "#F4F4EF"
WATER     = "#BDD5E8"

# ── Departamentos com área muito pequena → usam zoom-inset ───────────────────
SMALL_DEPTS = {"00", "11"}   # Asunción e Central (DPTO code)

# ── Mapeamento: código DPTO → nome para exibição ─────────────────────────────
NOME_MAP = {
    "00": "Asunción",
    "01": "Concepción",
    "02": "San Pedro",
    "03": "Cordillera",
    "04": "Guairá",
    "05": "Caaguazú",
    "06": "Caazapá",
    "07": "Itapúa",
    "08": "Misiones",
    "09": "Paraguarí",
    "10": "Alto Paraná",
    "11": "Central",
    "12": "Ñeembucú",
    "13": "Amambay",
    "14": "Canindeyú",
    "15": "Presidente Hayes",
    "16": "Boquerón",
    "17": "Alto Paraguay",
}

def north_arrow(ax, x=0.94, y=0.10, size=0.07):
    ax.annotate("", xy=(x, y + size), xytext=(x, y),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8,
                                mutation_scale=14))
    ax.text(x, y - 0.03, "N", transform=ax.transAxes,
            ha='center', va='top', fontsize=7.5, fontweight='bold',
            color=NAVY, fontfamily='DejaVu Sans')

def scale_bar(ax, xmin, xmax, ymin, ymax):
    """Barra de escala posicionada via coordenadas de axes (sem conflito com legenda)."""
    span_deg = xmax - xmin
    km_per_deg = 111 * np.cos(np.radians(23))
    bar_km = round((span_deg * 0.20 * km_per_deg) / 50) * 50
    # Converte bar_km de volta para fração do eixo x
    bar_frac = (bar_km / km_per_deg) / (xmax - xmin)

    # Posição: canto inferior esquerdo em coordenadas de axes
    x0, y0 = 0.05, 0.04
    x1 = x0 + bar_frac

    ax.plot([x0, x1], [y0, y0], transform=ax.transAxes,
            color=NAVY, linewidth=2.5, solid_capstyle='butt',
            clip_on=False, zorder=10)
    for xp in [x0, x1]:
        ax.plot([xp, xp], [y0 - 0.012, y0 + 0.012], transform=ax.transAxes,
                color=NAVY, linewidth=1.5, clip_on=False, zorder=10)
    ax.text((x0 + x1) / 2, y0 + 0.022, f"{int(bar_km)} km",
            transform=ax.transAxes,
            ha='center', va='bottom', fontsize=6.5, color=NAVY,
            fontfamily='DejaVu Sans', clip_on=False, zorder=10)

def plot_layers(ax, outros, dest, distritos, gdf_pais, lw_dept=1.8):
    """Desenha todas as camadas num eixo."""
    if not outros.empty:
        outros.plot(ax=ax, color=GRAY_DEP, edgecolor=GRAY_BDR,
                    linewidth=0.4, zorder=2)
    if not dest.empty:
        dest.plot(ax=ax, color=GOLD_LITE, edgecolor=NAVY,
                  linewidth=lw_dept, zorder=3)
    if not distritos.empty:
        distritos.plot(ax=ax, facecolor='none', edgecolor=DIST_CLR,
                       linewidth=0.7, linestyle='--', zorder=4)
    gdf_pais.plot(ax=ax, facecolor='none', edgecolor=NAVY,
                  linewidth=0.9, zorder=5)

def gerar_mapa(dpto_code, nome_display, gdf_dept, gdf_dist,
               xmin_p, xmax_p, ymin_p, ymax_p):

    dest     = gdf_dept[gdf_dept['DPTO'] == dpto_code]
    outros   = gdf_dept[gdf_dept['DPTO'] != dpto_code]
    distritos = gdf_dist[gdf_dist['DPTO'] == dpto_code]
    pais     = gdf_dept.dissolve()

    fig, ax = plt.subplots(figsize=(7, 8), dpi=200)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    plot_layers(ax, outros, dest, distritos, pais)

    # Extensão fixa (país inteiro)
    mx = (xmax_p - xmin_p) * 0.03
    my = (ymax_p - ymin_p) * 0.03
    ax.set_xlim(xmin_p - mx, xmax_p + mx)
    ax.set_ylim(ymin_p - my, ymax_p + my)
    ax.set_aspect('equal')

    # ── Zoom-inset para departamentos pequenos ────────────────────────────────
    use_inset = dpto_code in SMALL_DEPTS and not dest.empty
    if use_inset:
        bx = dest.total_bounds
        span = max(bx[2] - bx[0], bx[3] - bx[1])
        pad = max(span * 2.5, 0.5)   # área ao redor no inset
        cx = (bx[0] + bx[2]) / 2
        cy = (bx[1] + bx[3]) / 2

        # Inset de tamanho fixo: 38% da largura e altura do axes, no canto superior esquerdo
        axins = ax.inset_axes([0.01, 0.58, 0.38, 0.38])
        axins.set_facecolor('none')
        plot_layers(axins, outros, dest, distritos, pais, lw_dept=1.5)
        axins.set_xlim(cx - pad, cx + pad)
        axins.set_ylim(cy - pad, cy + pad)
        axins.set_aspect('equal')
        axins.set_xticks([])
        axins.set_yticks([])
        for spine in axins.spines.values():
            spine.set_edgecolor(NAVY)
            spine.set_linewidth(1.2)
        ax.indicate_inset_zoom(axins, edgecolor=NAVY, linewidth=0.8, alpha=0.7)

        # Estrela marcadora no mapa principal
        cx_m = dest.geometry.centroid.x.values[0]
        cy_m = dest.geometry.centroid.y.values[0]
        ax.plot(cx_m, cy_m, '*', color="#C5A03C", markersize=10,
                markeredgecolor=NAVY, markeredgewidth=0.7, zorder=7)
    else:
        if not dest.empty:
            cx = dest.geometry.centroid.x.values[0]
            cy = dest.geometry.centroid.y.values[0]
            ax.plot(cx, cy, 'o', color=NAVY, markersize=3.5,
                    markeredgecolor='white', markeredgewidth=0.7, zorder=6)

    scale_bar(ax, xmin_p, xmax_p, ymin_p, ymax_p)
    north_arrow(ax)

    ax.set_title(nome_display, fontsize=12, fontweight='bold',
                 color=NAVY, fontfamily='DejaVu Sans', pad=6)

    patch_dest   = mpatches.Patch(facecolor=GOLD_LITE, edgecolor=NAVY,
                                   linewidth=0.8, label=nome_display)
    patch_outros = mpatches.Patch(facecolor=GRAY_DEP, edgecolor=GRAY_BDR,
                                   linewidth=0.4, label='Demais departamentos')
    # Legenda sempre no canto inferior direito (escala fica no inferior esquerdo)
    ax.legend(handles=[patch_dest, patch_outros],
              loc='lower right', fontsize=6.5,
              framealpha=0.88, edgecolor=NAVY, fancybox=False,
              handlelength=1.2, handleheight=0.9)

    ax.set_axis_off()

    # Salva sem e com zero-padding para compatibilidade
    num = int(dpto_code)
    path_no_pad = os.path.join(OUT, f"mapa_dept_{num}.png")
    path_padded = os.path.join(OUT, f"mapa_dept_{num:02d}.png")
    fig.savefig(path_no_pad, format='png', bbox_inches='tight',
                dpi=200)
    if path_no_pad != path_padded:
        shutil.copy2(path_no_pad, path_padded)
    plt.close(fig)
    print(f"  [OK] {path_no_pad}")


def main():
    print("Carregando dados CNPV2022…")
    gdf_dept = gpd.read_file(DEPT)
    gdf_dist = gpd.read_file(DIST)

    bounds = gdf_dept.total_bounds
    xmin_p, ymin_p, xmax_p, ymax_p = bounds

    print(f"Departamentos: {len(gdf_dept)} | Distritos: {len(gdf_dist)}")
    print(f"CRS: {gdf_dept.crs}")
    print(f"Extensão: lon [{xmin_p:.2f}, {xmax_p:.2f}]  lat [{ymin_p:.2f}, {ymax_p:.2f}]")
    print("\nGerando mapas…\n")

    for code, nome in sorted(NOME_MAP.items()):
        print(f"  [{code}] {nome}")
        gerar_mapa(code, nome, gdf_dept, gdf_dist,
                   xmin_p, xmax_p, ymin_p, ymax_p)

    print(f"\nConcluído! {len(NOME_MAP)} mapas em {OUT}")


if __name__ == "__main__":
    main()

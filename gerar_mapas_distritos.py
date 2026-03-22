#!/usr/bin/env python3
"""
Gera mapas individuais por DISTRITO do Paraguai para o livro LaTeX.
Estilo idêntico aos mapas de departamento:
  - Paraguay inteiro em cinza
  - Departamento do distrito em dourado claro
  - Distrito específico em dourado vivo com borda navy espessa

Também atualiza os arquivos .tex substituindo \mapaConteudo{lat}{lon}
por \mapaDistrito{CLAVE} e atualiza a definição em main.tex.
"""

import os
import re
import shutil
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
from shapely.geometry import Point
import numpy as np

warnings.filterwarnings('ignore')

# ── Caminhos ────────────────────────────────────────────────────────────────
BASE      = os.path.dirname(os.path.abspath(__file__))
DEPT_GEO  = os.path.join(BASE, "mapas", "DEPARTAMENTOS_PY_CNPV2022.geojson")
DIST_GEO  = os.path.join(BASE, "mapas", "DISTRITOS_PY_CNPV2022.geojson")
CAPS      = os.path.join(BASE, "livro_latex", "capitulos")
MAIN_TEX  = os.path.join(BASE, "livro_latex", "main.tex")
OUT       = os.path.join(BASE, "livro_latex", "mapas")
os.makedirs(OUT, exist_ok=True)

# ── Paleta (mesma dos mapas de departamento) ─────────────────────────────────
NAVY      = "#1A2D5A"
GOLD_DEPT = "#E8C96A"   # departamento do distrito (dourado claro)
GOLD_DIST = "#C5A03C"   # distrito em destaque (dourado vivo)
GRAY_DEP  = "#D0D0D0"
GRAY_BDR  = "#999999"
DIST_CLR  = "#8A6010"   # bordas dos outros distritos internos

# ── Mapeamento DPTO code → nome display ─────────────────────────────────────
NOME_DEPT = {
    "00": "Asunción", "01": "Concepción", "02": "San Pedro",
    "03": "Cordillera", "04": "Guairá", "05": "Caaguazú",
    "06": "Caazapá", "07": "Itapúa", "08": "Misiones",
    "09": "Paraguarí", "10": "Alto Paraná", "11": "Central",
    "12": "Ñeembucú", "13": "Amambay", "14": "Canindeyú",
    "15": "Presidente Hayes", "16": "Boquerón", "17": "Alto Paraguay",
}

def north_arrow(ax, x=0.93, y=0.08, size=0.07):
    ax.annotate("", xy=(x, y + size), xytext=(x, y),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5,
                                mutation_scale=11))
    ax.text(x, y - 0.03, "N", transform=ax.transAxes,
            ha='center', va='top', fontsize=6, fontweight='bold',
            color=NAVY, fontfamily='DejaVu Sans')

def plot_dist_layers(ax, outros_dept, dest_dept, outros_dist, dest_dist, pais,
                     lw_dept=0.9, lw_dist=1.4):
    """Desenha todas as camadas de um mapa de distrito num eixo."""
    if not outros_dept.empty:
        outros_dept.plot(ax=ax, color=GRAY_DEP, edgecolor=GRAY_BDR,
                         linewidth=0.35, zorder=2)
    if not dest_dept.empty:
        dest_dept.plot(ax=ax, color=GOLD_DEPT, edgecolor=NAVY,
                       linewidth=lw_dept, zorder=3)
    if not outros_dist.empty:
        outros_dist.plot(ax=ax, facecolor='none', edgecolor=DIST_CLR,
                         linewidth=0.5, linestyle='--', zorder=4)
    if not dest_dist.empty:
        dest_dist.plot(ax=ax, color=GOLD_DIST, edgecolor=NAVY,
                       linewidth=lw_dist, zorder=5)
    pais.plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=0.8, zorder=6)


def gerar_mapa_distrito(clave, dist_name, dept_code,
                         gdf_dept, gdf_dist,
                         xmin_p, xmax_p, ymin_p, ymax_p):
    dest_dist  = gdf_dist[gdf_dist['CLAVE'] == clave]
    dest_dept  = gdf_dept[gdf_dept['DPTO'] == dept_code]
    outros_dept = gdf_dept[gdf_dept['DPTO'] != dept_code]
    outros_dist = gdf_dist[(gdf_dist['DPTO'] == dept_code) & (gdf_dist['CLAVE'] != clave)]
    pais = gdf_dept.dissolve()

    fig, ax = plt.subplots(figsize=(4, 4.6), dpi=180)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    # ── Mapa principal: país inteiro ─────────────────────────────────────────
    plot_dist_layers(ax, outros_dept, dest_dept, outros_dist, dest_dist, pais)

    mx = (xmax_p - xmin_p) * 0.02
    my = (ymax_p - ymin_p) * 0.02
    ax.set_xlim(xmin_p - mx, xmax_p + mx)
    ax.set_ylim(ymin_p - my, ymax_p + my)
    ax.set_aspect('equal')

    # ── Zoom-inset: departamento ampliado com distrito destacado ─────────────
    if not dest_dist.empty and not dest_dept.empty:
        # Bounds do departamento (área do zoom)
        bx_dept = dest_dept.total_bounds   # [xmin, ymin, xmax, ymax]
        span_dept = max(bx_dept[2] - bx_dept[0], bx_dept[3] - bx_dept[1])
        pad_dept  = span_dept * 0.12        # margem ao redor do dept

        cx_dept = (bx_dept[0] + bx_dept[2]) / 2
        cy_dept = (bx_dept[1] + bx_dept[3]) / 2

        # Inset fixo: 42% da largura e altura, canto superior esquerdo
        axins = ax.inset_axes([0.01, 0.56, 0.42, 0.42])
        axins.set_facecolor('none')
        plot_dist_layers(axins, outros_dept, dest_dept, outros_dist, dest_dist, pais,
                         lw_dept=0.7, lw_dist=1.2)
        axins.set_xlim(bx_dept[0] - pad_dept, bx_dept[2] + pad_dept)
        axins.set_ylim(bx_dept[1] - pad_dept, bx_dept[3] + pad_dept)
        axins.set_aspect('equal')
        axins.set_xticks([])
        axins.set_yticks([])
        for spine in axins.spines.values():
            spine.set_edgecolor(NAVY)
            spine.set_linewidth(0.9)

        ax.indicate_inset_zoom(axins, edgecolor=NAVY, linewidth=0.7, alpha=0.7)

    north_arrow(ax)

    dept_nome = NOME_DEPT.get(dept_code, dept_code)
    ax.set_title(f"{dist_name}\n{dept_nome}", fontsize=7, fontweight='bold',
                 color=NAVY, fontfamily='DejaVu Sans', pad=3, linespacing=1.3)

    ax.set_axis_off()

    out_path = os.path.join(OUT, f"dist_{clave}.pdf")
    fig.savefig(out_path, format='pdf', bbox_inches='tight',
                facecolor='none', transparent=True, dpi=180)
    plt.close(fig)
    return out_path


def extrair_claves_tex():
    """Lê todos os .tex e extrai o conjunto de CLAVEs usadas em \mapaDistrito{CLAVE}."""
    padrao = re.compile(r'\\mapaDistrito\{([^}]+)\}')
    claves = set()
    for fname in sorted(os.listdir(CAPS)):
        if not fname.endswith('.tex'):
            continue
        fpath = os.path.join(CAPS, fname)
        with open(fpath, encoding='utf-8') as f:
            texto = f.read()
        for m in padrao.finditer(texto):
            claves.add(m.group(1))
    return claves


def main():
    print("Carregando dados CNPV2022…")
    gdf_dept = gpd.read_file(DEPT_GEO)
    gdf_dist = gpd.read_file(DIST_GEO)

    bounds = gdf_dept.total_bounds
    xmin_p, ymin_p, xmax_p, ymax_p = bounds

    print(f"Departamentos: {len(gdf_dept)} | Distritos: {len(gdf_dist)}")
    print(f"CLAVE exemplos: {gdf_dist['CLAVE'].head(5).tolist()}")

    # ── 1. Ler CLAVEs usadas nos tex ─────────────────────────────────────────
    print("\nLendo CLAVEs dos arquivos .tex…")
    claves_usadas = extrair_claves_tex()
    print(f"  {len(claves_usadas)} CLAVEs encontradas\n")

    # ── 2. Gerar mapas por CLAVE ─────────────────────────────────────────────
    # Índice CLAVE → (DPTO, DIST_DESC_)
    dist_idx = gdf_dist.set_index('CLAVE')[['DPTO', 'DIST_DESC_']].to_dict('index')

    print(f"Gerando {len(claves_usadas)} mapas de distritos com zoom-inset…\n")
    for i, clave in enumerate(sorted(claves_usadas), 1):
        info = dist_idx.get(clave)
        if not info:
            print(f"  [{i:03d}] AVISO: CLAVE {clave} não encontrada no GeoJSON")
            continue
        dpto = info['DPTO']
        dist_desc = info['DIST_DESC_']
        out = gerar_mapa_distrito(clave, dist_desc, dpto,
                                   gdf_dept, gdf_dist,
                                   xmin_p, xmax_p, ymin_p, ymax_p)
        print(f"  [{i:03d}] {clave} {dist_desc} ({dpto})")

    print(f"\nConcluído! {len(claves_usadas)} mapas gerados em {OUT}")


if __name__ == "__main__":
    main()

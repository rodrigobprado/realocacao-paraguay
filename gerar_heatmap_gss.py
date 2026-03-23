#!/usr/bin/env python3
"""
Gera heatmap GSS por distrito e por departamento.
Extrai scores dos arquivos .tex e cria mapas coropléticos.
"""

import os
import re
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.colorbar import ColorbarBase
import geopandas as gpd
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

BASE     = os.path.dirname(os.path.abspath(__file__))
CAPS     = os.path.join(BASE, "livro_latex", "capitulos")
DIST_GEO = os.path.join(BASE, "mapas", "DISTRITOS_PY_CNPV2022.geojson")
DEPT_GEO = os.path.join(BASE, "mapas", "DEPARTAMENTOS_PY_CNPV2022.geojson")
OUT      = os.path.join(BASE, "livro_latex", "mapas")
os.makedirs(OUT, exist_ok=True)

NAVY  = "#1A2D5A"
# Escala de cor: vermelho (baixo) → amarelo → verde (alto)
CMAP  = "RdYlGn"

# ── Extrair GSS por CLAVE dos arquivos tex ────────────────────────────────────
def extrair_gss_tex():
    """
    Lê todos os dept_*.tex e extrai pares (CLAVE, GSS_final).
    Padrão: \secaoDiagnostico{Nome}{\mapaDistrito{CLAVE}}{...
    e depois:  \textbf{GSS FINAL} & \textbf{N.N} &
    """
    padrao_sec = re.compile(
        r'\\secaoDiagnostico\{[^}]+\}\{\\mapaDistrito\{([^}]+)\}\}',
        re.DOTALL
    )
    padrao_gss = re.compile(r'\\textbf\{GSS FINAL\}\s*&\s*\\textbf\{(\d+(?:[.,]\d+)?)\}')

    dados = {}  # CLAVE → GSS

    for fname in sorted(os.listdir(CAPS)):
        if not (fname.startswith('dept_') and fname.endswith('.tex')):
            continue
        fpath = os.path.join(CAPS, fname)
        with open(fpath, encoding='utf-8') as f:
            conteudo = f.read()

        # Encontrar todas as seções de diagnóstico com seu CLAVE
        sec_matches = list(padrao_sec.finditer(conteudo))

        for i, m in enumerate(sec_matches):
            clave = m.group(1)
            # Pegar o texto entre esta seção e a próxima
            inicio = m.end()
            fim = sec_matches[i+1].start() if i+1 < len(sec_matches) else len(conteudo)
            trecho = conteudo[inicio:fim]

            # Extrair GSS FINAL
            gss_m = padrao_gss.search(trecho)
            if gss_m:
                gss_val = float(gss_m.group(1).replace(',', '.'))
                dados[clave] = gss_val

    return dados

# ── Extrair sub-scores GSS (A,B,C,D,E) ───────────────────────────────────────
def extrair_subscores_tex():
    """Extrai também os sub-scores A,B,C,D,E por CLAVE."""
    padrao_sec = re.compile(
        r'\\secaoDiagnostico\{[^}]+\}\{\\mapaDistrito\{([^}]+)\}\}',
        re.DOTALL
    )
    # A - Ameaças Estratégicas & N.N &
    padrao_sub = re.compile(
        r'A - Ameaças Estratégicas\s*&\s*(\d+(?:[.,]\d+)?)\s*&.*?'
        r'B - Risco Social\s*&\s*(\d+(?:[.,]\d+)?)\s*&.*?'
        r'C - Riscos Naturais\s*&\s*(\d+(?:[.,]\d+)?)\s*&.*?'
        r'D - Autossuficiência\s*&\s*(\d+(?:[.,]\d+)?)\s*&.*?'
        r'E - Institucional\s*&\s*(\d+(?:[.,]\d+)?)\s*&',
        re.DOTALL
    )

    dados = {}

    for fname in sorted(os.listdir(CAPS)):
        if not (fname.startswith('dept_') and fname.endswith('.tex')):
            continue
        fpath = os.path.join(CAPS, fname)
        with open(fpath, encoding='utf-8') as f:
            conteudo = f.read()

        sec_matches = list(padrao_sec.finditer(conteudo))
        for i, m in enumerate(sec_matches):
            clave = m.group(1)
            inicio = m.end()
            fim = sec_matches[i+1].start() if i+1 < len(sec_matches) else len(conteudo)
            trecho = conteudo[inicio:fim]
            sub_m = padrao_sub.search(trecho)
            if sub_m:
                dados[clave] = {
                    'A': float(sub_m.group(1).replace(',','.')),
                    'B': float(sub_m.group(2).replace(',','.')),
                    'C': float(sub_m.group(3).replace(',','.')),
                    'D': float(sub_m.group(4).replace(',','.')),
                    'E': float(sub_m.group(5).replace(',','.')),
                }
    return dados

# ── IDH por departamento (dos arquivos tex) ───────────────────────────────────
def extrair_idh_tex():
    """Extrai IDH de cada departamento."""
    padrao = re.compile(r'IDH\s*&\s*(0,\d+)\s*\\\\')
    dados = {}
    for fname in sorted(os.listdir(CAPS)):
        if not (fname.startswith('dept_') and fname.endswith('.tex')):
            continue
        # Código do departamento
        m_code = re.match(r'dept_(\d{2})_', fname)
        if not m_code:
            continue
        dpto = m_code.group(1)
        fpath = os.path.join(CAPS, fname)
        with open(fpath, encoding='utf-8') as f:
            conteudo = f.read()
        m = padrao.search(conteudo)
        if m:
            dados[dpto] = float(m.group(1).replace(',', '.'))
    return dados

# ── Gerar mapa heatmap GSS por distrito ──────────────────────────────────────
def gerar_heatmap_distrito(gdf_dist, gdf_dept, gss_dict, titulo, fname):
    fig, ax = plt.subplots(figsize=(9, 10), dpi=150)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    # Juntar GSS ao GeoDataFrame
    gdf = gdf_dist.copy()
    gdf['GSS'] = gdf['CLAVE'].map(gss_dict)

    cmap = plt.cm.get_cmap(CMAP)
    norm = mcolors.Normalize(vmin=3.0, vmax=9.0)

    # Distritos sem GSS (cor neutra)
    sem_gss = gdf[gdf['GSS'].isna()]
    if not sem_gss.empty:
        sem_gss.plot(ax=ax, color='#E0E0E0', edgecolor='#BBBBBB', linewidth=0.3, zorder=2)

    # Distritos com GSS
    com_gss = gdf[gdf['GSS'].notna()]
    if not com_gss.empty:
        com_gss.plot(ax=ax, column='GSS', cmap=CMAP, norm=norm,
                     edgecolor='white', linewidth=0.15, zorder=3)

    # Contorno dos departamentos
    gdf_dept.plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=0.8, zorder=4)
    # Contorno do país
    gdf_dept.dissolve().plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.2, zorder=5)

    ax.set_axis_off()
    ax.set_title(titulo, fontsize=11, fontweight='bold', color=NAVY,
                 fontfamily='DejaVu Sans', pad=8)

    # Barra de cores
    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.02,
                        shrink=0.6, aspect=25)
    cbar.set_label('GSS (Global Safety Score)', fontsize=8, color=NAVY,
                   fontfamily='DejaVu Sans')
    cbar.ax.tick_params(labelsize=7, colors=NAVY)
    cbar.outline.set_edgecolor(NAVY)

    # Estatísticas movidas para legenda LaTeX; não embutir no gráfico

    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='png', bbox_inches='tight',
                dpi=150)
    plt.close(fig)
    print(f"  [OK] {out_path}")
    return com_gss.shape[0]

# ── Gerar mapa heatmap por departamento ──────────────────────────────────────
def gerar_heatmap_departamento(gdf_dist, gdf_dept, gss_dict, titulo, fname):
    """Agrega GSS por departamento (média) e plota."""
    gdf = gdf_dist.copy()
    gdf['GSS'] = gdf['CLAVE'].map(gss_dict)

    dept_gss = gdf.groupby('DPTO')['GSS'].mean().reset_index()
    dept_gss.columns = ['DPTO', 'GSS_medio']

    gdf_d = gdf_dept.merge(dept_gss, on='DPTO', how='left')

    fig, ax = plt.subplots(figsize=(9, 10), dpi=150)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    norm = mcolors.Normalize(vmin=3.0, vmax=9.0)

    sem = gdf_d[gdf_d['GSS_medio'].isna()]
    if not sem.empty:
        sem.plot(ax=ax, color='#E0E0E0', edgecolor='#AAAAAA', linewidth=0.5, zorder=2)

    com = gdf_d[gdf_d['GSS_medio'].notna()]
    if not com.empty:
        com.plot(ax=ax, column='GSS_medio', cmap=CMAP, norm=norm,
                 edgecolor=NAVY, linewidth=0.8, zorder=3)

    gdf_dept.dissolve().plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.2, zorder=4)

    # Rótulos com o GSS médio
    for _, row in gdf_d.iterrows():
        if pd.notna(row['GSS_medio']):
            centroid = row['geometry'].centroid
            ax.text(centroid.x, centroid.y, f"{row['GSS_medio']:.1f}",
                    ha='center', va='center', fontsize=5.5, fontweight='bold',
                    color='black', fontfamily='DejaVu Sans', zorder=5)

    ax.set_axis_off()
    ax.set_title(titulo, fontsize=11, fontweight='bold', color=NAVY,
                 fontfamily='DejaVu Sans', pad=8)

    sm = plt.cm.ScalarMappable(cmap=CMAP, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.02,
                        shrink=0.6, aspect=25)
    cbar.set_label('GSS médio por departamento', fontsize=8, color=NAVY,
                   fontfamily='DejaVu Sans')
    cbar.ax.tick_params(labelsize=7, colors=NAVY)
    cbar.outline.set_edgecolor(NAVY)

    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='png', bbox_inches='tight',
                dpi=150)
    plt.close(fig)
    print(f"  [OK] {out_path}")

# ── Gerar mapa de IDH por departamento ───────────────────────────────────────
def gerar_mapa_idh(gdf_dept, idh_dict, fname):
    gdf = gdf_dept.copy()
    gdf['IDH'] = gdf['DPTO'].map(idh_dict)

    fig, ax = plt.subplots(figsize=(9, 10), dpi=150)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    norm = mcolors.Normalize(vmin=0.60, vmax=0.85)
    cmap_idh = 'YlOrRd_r'  # azul-verde = alto IDH

    sem = gdf[gdf['IDH'].isna()]
    if not sem.empty:
        sem.plot(ax=ax, color='#E0E0E0', edgecolor='#AAAAAA', linewidth=0.5, zorder=2)

    com = gdf[gdf['IDH'].notna()]
    if not com.empty:
        com.plot(ax=ax, column='IDH', cmap=cmap_idh, norm=norm,
                 edgecolor=NAVY, linewidth=0.8, zorder=3)

    gdf_dept.dissolve().plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.2, zorder=4)

    # Rótulos
    for _, row in gdf.iterrows():
        if pd.notna(row['IDH']):
            centroid = row['geometry'].centroid
            ax.text(centroid.x, centroid.y, f"{row['IDH']:.3f}",
                    ha='center', va='center', fontsize=5.5, fontweight='bold',
                    color='black', fontfamily='DejaVu Sans', zorder=5)

    ax.set_axis_off()
    ax.set_title('Índice de Desenvolvimento Humano (IDH)\npor Departamento --- Paraguai (est. 2020)',
                 fontsize=10, fontweight='bold', color=NAVY, fontfamily='DejaVu Sans', pad=8)

    sm = plt.cm.ScalarMappable(cmap=cmap_idh, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.02,
                        shrink=0.6, aspect=25)
    cbar.set_label('IDH Estimado', fontsize=8, color=NAVY, fontfamily='DejaVu Sans')
    cbar.ax.tick_params(labelsize=7, colors=NAVY)
    cbar.outline.set_edgecolor(NAVY)

    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='png', bbox_inches='tight',
                dpi=150)
    plt.close(fig)
    print(f"  [OK] {out_path}")

# ── Gerar mapa de risco social (sub-score B) ──────────────────────────────────
def gerar_mapa_risco_social(gdf_dist, gdf_dept, subscores_dict, fname):
    """Usa sub-score B (Risco Social) como proxy de violência/criminalidade.
    Score B é invertido: 10 = muito seguro, 0 = muito perigoso."""
    gdf = gdf_dist.copy()
    # Risco real = 10 - score_B (maior = mais perigoso)
    gdf['RISCO_B'] = gdf['CLAVE'].map(
        lambda c: 10.0 - subscores_dict[c]['B'] if c in subscores_dict else None
    )

    fig, ax = plt.subplots(figsize=(9, 10), dpi=150)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    norm = mcolors.Normalize(vmin=0, vmax=7)
    cmap_risk = 'YlOrRd'  # amarelo-laranja-vermelho = maior risco

    sem = gdf[gdf['RISCO_B'].isna()]
    if not sem.empty:
        sem.plot(ax=ax, color='#E0E0E0', edgecolor='#BBBBBB', linewidth=0.3, zorder=2)

    com = gdf[gdf['RISCO_B'].notna()]
    if not com.empty:
        com.plot(ax=ax, column='RISCO_B', cmap=cmap_risk, norm=norm,
                 edgecolor='white', linewidth=0.15, zorder=3)

    gdf_dept.plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=0.8, zorder=4)
    gdf_dept.dissolve().plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.2, zorder=5)

    ax.set_axis_off()
    ax.set_title('Risco Social por Distrito\n(Baseado no sub-critério B do GSS)',
                 fontsize=10, fontweight='bold', color=NAVY, fontfamily='DejaVu Sans', pad=8)

    sm = plt.cm.ScalarMappable(cmap=cmap_risk, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.02,
                        shrink=0.6, aspect=25)
    cbar.set_label('Nível de risco (0=baixo, 7=alto)', fontsize=8, color=NAVY,
                   fontfamily='DejaVu Sans')
    cbar.ax.tick_params(labelsize=7, colors=NAVY)
    cbar.outline.set_edgecolor(NAVY)

    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='png', bbox_inches='tight',
                dpi=150)
    plt.close(fig)
    print(f"  [OK] {out_path}")

# ── Gerar mapa de autossuficiência (sub-score D) ──────────────────────────────
def gerar_mapa_autossuficiencia(gdf_dist, gdf_dept, subscores_dict, fname):
    """Sub-score D = Autossuficiência (solo, água, energia)."""
    gdf = gdf_dist.copy()
    gdf['AUTOSUF'] = gdf['CLAVE'].map(
        lambda c: subscores_dict[c]['D'] if c in subscores_dict else None
    )

    fig, ax = plt.subplots(figsize=(9, 10), dpi=150)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    norm = mcolors.Normalize(vmin=3.0, vmax=9.5)
    cmap_d = 'YlGn'

    sem = gdf[gdf['AUTOSUF'].isna()]
    if not sem.empty:
        sem.plot(ax=ax, color='#E0E0E0', edgecolor='#BBBBBB', linewidth=0.3, zorder=2)

    com = gdf[gdf['AUTOSUF'].notna()]
    if not com.empty:
        com.plot(ax=ax, column='AUTOSUF', cmap=cmap_d, norm=norm,
                 edgecolor='white', linewidth=0.15, zorder=3)

    gdf_dept.plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=0.8, zorder=4)
    gdf_dept.dissolve().plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.2, zorder=5)

    ax.set_axis_off()
    ax.set_title('Potencial de Autossuficiência por Distrito\n(Sub-critério D: Solo, Água e Energia)',
                 fontsize=10, fontweight='bold', color=NAVY, fontfamily='DejaVu Sans', pad=8)

    sm = plt.cm.ScalarMappable(cmap=cmap_d, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.03, pad=0.02,
                        shrink=0.6, aspect=25)
    cbar.set_label('Score D (0=baixo, 10=alto)', fontsize=8, color=NAVY,
                   fontfamily='DejaVu Sans')
    cbar.ax.tick_params(labelsize=7, colors=NAVY)
    cbar.outline.set_edgecolor(NAVY)

    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='png', bbox_inches='tight',
                dpi=150)
    plt.close(fig)
    print(f"  [OK] {out_path}")


def main():
    print("Carregando GeoJSONs...")
    gdf_dist = gpd.read_file(DIST_GEO)
    gdf_dept = gpd.read_file(DEPT_GEO)

    print("Extraindo GSS dos arquivos tex...")
    gss_dict = extrair_gss_tex()
    print(f"  {len(gss_dict)} distritos com GSS extraído")

    print("Extraindo sub-scores GSS...")
    subscores = extrair_subscores_tex()
    print(f"  {len(subscores)} distritos com sub-scores")

    print("Extraindo IDH por departamento...")
    idh_dict = extrair_idh_tex()
    print(f"  {len(idh_dict)} departamentos com IDH: {idh_dict}")

    print("\nGerando mapas temáticos...")

    n1 = gerar_heatmap_distrito(
        gdf_dist, gdf_dept, gss_dict,
        'Heatmap GSS por Distrito --- Paraguai',
        'heatmap_gss_distrito.png'
    )
    print(f"  → {n1} distritos com dados")

    gerar_heatmap_departamento(
        gdf_dist, gdf_dept, gss_dict,
        'Heatmap GSS Médio por Departamento --- Paraguai',
        'heatmap_gss_departamento.png'
    )

    gerar_mapa_idh(gdf_dept, idh_dict, 'mapa_idh_departamento.png')

    if subscores:
        gerar_mapa_risco_social(
            gdf_dist, gdf_dept, subscores, 'mapa_risco_social.png'
        )
        gerar_mapa_autossuficiencia(
            gdf_dist, gdf_dept, subscores, 'mapa_autossuficiencia.png'
        )

    print(f"\nConcluído! Mapas em {OUT}")

    # Exportar CSV com todos os GSS
    df = pd.DataFrame([(k, v) for k, v in gss_dict.items()], columns=['CLAVE', 'GSS'])
    df.to_csv(os.path.join(BASE, 'gss_por_distrito.csv'), index=False)
    print(f"CSV exportado: gss_por_distrito.csv ({len(df)} linhas)")

if __name__ == "__main__":
    main()

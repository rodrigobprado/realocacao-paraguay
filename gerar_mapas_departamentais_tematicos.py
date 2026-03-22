#!/usr/bin/env python3
"""
Gera mapas temáticos detalhados por departamento.
Para cada departamento, produz uma figura com 3 painéis:
  1. GSS por distrito (heatmap com valores e nomes)
  2. Risco Social (sub-score B invertido)
  3. Autossuficiência (sub-score D)

Salva como mapas/mapas_tematicos_dept_XX.pdf
E atualiza cada dept_XX_*.tex inserindo a figura logo após \mapaparaguai.
"""

import os
import re
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as pe
import geopandas as gpd
import pandas as pd
import numpy as np

warnings.filterwarnings('ignore')

BASE     = os.path.dirname(os.path.abspath(__file__))
CAPS     = os.path.join(BASE, "livro_latex", "capitulos")
DIST_GEO = os.path.join(BASE, "mapas", "DISTRITOS_PY_CNPV2022.geojson")
DEPT_GEO = os.path.join(BASE, "mapas", "DEPARTAMENTOS_PY_CNPV2022.geojson")
OUT      = os.path.join(BASE, "livro_latex", "mapas")

NAVY = "#1A2D5A"

# ── Abreviaturas para rótulos de distrito (nomes longos) ─────────────────────
ABREV = {
    'SARGENTO JOSE FELIX LOPEZ': 'Sgt. J.F. López',
    'ROQUE GONZALEZ DE SANTA CRUZ': 'Roque González',
    'DOMINGO MARTINEZ DE IRALA': 'Dte. M. de Irala',
    'SAN JOSE DE LOS ARROYOS': 'S.J. Arroyos',
    'SANTA ROSA DEL MONDAY': 'Sta. Rosa Monday',
    'SANTA ROSA DEL AGUARAY': 'Sta. Rosa Aguaray',
    'ITACURUBI DEL ROSARIO': 'Itacurubí Rosario',
    'SAN PEDRO DEL YCUAMANDYYU': 'S.Pedro Ycuam.',
    'GENERAL BERNARDINO CABALLERO': 'Gral. B. Caballero',
    'CORONEL MARTINEZ': 'Cnel. Martínez',
    'COLONIA INDEPENDENCIA': 'Col. Independencia',
    'MARIANO ROQUE ALONSO': 'M. Roque Alonso',
    'BENJAMIN ACEVAL': 'Benj. Aceval',
    'FUERTE OLIMPO': 'Fte. Olimpo',
    'PUERTO CASADO': 'Pto. Casado',
    'VILLA DEL ROSARIO': 'Villa Rosario',
    'SAN RAFAEL DEL PARANA': 'S. Rafael Paraná',
    'SAN PEDRO DEL PARANA': 'S.Pedro Paraná',
    'CAPITAN MIRANDA': 'Cap. Miranda',
    'CAPITAN MEZA': 'Cap. Meza',
    'GENERAL ARTIGAS': 'Gral. Artigas',
    'CORONEL BOGADO': 'Cnel. Bogado',
    'ITAPUA POTY': 'Itapúa Poty',
    'ALTO VERA': 'Alto Vera',
    'NATALIO': 'Natalio',
    'SAN JUAN DEL PARANA': 'S.Juan Paraná',
    'SAN COSME Y DAMIAN': 'S.Cosme Damián',
    'TRINIDAD': 'Trinidad',
    'ENCARNACION': 'Encarnación',
    'HOHENAU': 'Hohenau',
    'BELLA VISTA': 'Bella Vista',
    'VILLALBIN': 'Villaalbín',
    'FRAM': 'Fram',
    'CARLOS A. LOPEZ': 'C.A.López',
    'SAN PATRICIO': 'S.Patricio',
    'SAN JUAN BAUTISTA': 'S.Juan Bautista',
    'VILLA FLORIDA': 'Villa Florida',
    'AYOLAS': 'Ayolas',
    'MAYOR MARTINEZ': 'Mayor Martínez',
    'SAN MIGUEL': 'S.Miguel',
    'SANTA MARIA': 'Sta.María',
    'SANTA ROSA MISIONES': 'Sta.Rosa (Mis.)',
    'YABEBYRY': 'Yabebyry',
    'ARROYOS Y ESTEROS': 'Arroyos/Est.',
    'PIRIBEBUY': 'Piribebuy',
    'CAACUPE': 'Caacupé',
    'SAN BERNARDINO': 'S.Bernardino',
    'EUSEBIO AYALA': 'Eusebio Ayala',
    'NUEVA COLOMBIA': 'Nueva Colombia',
    'ISLA PUCU': 'Isla Pucú',
    'SAN JOSE OBRERO': 'S.José Obrero',
    'ITACURUBI DE LA CORDILLERA': 'Itacurubí Cord.',
    'LOMA GRANDE': 'Loma Grande',
    'CNEL OVIEDO': 'Cnel.Oviedo',
    'CORONEL OVIEDO': 'Cnel.Oviedo',
    'JOSE DOMINGO OCAMPOS': 'J.D.Ocampos',
    'SIMON BOLIVAR': 'S.Bolívar',
    'NUEVA TOLEDO': 'Nueva Toledo',
    'SANTA ROSA DEL MBUTUY': 'Sta.Rosa Mbutuy',
    'DOCTOR JUAN EULOGIO ESTIGARRIBIA': 'Dr. Estigarribia',
    'PEDRO JUAN CABALLERO': 'P.J. Caballero',
    'ZANJA PYTA': 'Zanja Pytá',
    'CAPITAN BADO': 'Cap. Badó',
    'BELLA VISTA NORTE': 'B.Vista Norte',
    'SALTO DEL GUAIRA': 'Salto Guairá',
    'CURUGUATY': 'Curuguatý',
    'YBYRAROVANA': 'Ybyrarovaña',
    'CORPUS CHRISTI': 'Corpus Christi',
    'VILLA DEL ROSARIO CANINDEYU': 'V.Rosario (Can.)',
    'GENERAL FRANCISCO ALVAREZ': 'Gral. Álvarez',
    'ITURBE': 'Iturbe',
    'CORONEL MARTINEZ': 'Cnel.Martínez',
    'NUMI': 'Numí',
    'MBOCAYATY': 'Mbocayaty',
    'FELIX PEREZ CARDOZO': 'F.P.Cardozo',
    'YATAITY DEL GUAIRA': 'Yataity',
    'NUEVA ITALIA': 'Nueva Italia',
    'LAMBARE': 'Lambaré',
    'VILLA ELISA': 'Villa Elisa',
    'SAN ANTONIO': 'S.Antonio',
    'YPANE': 'Ypané',
    'J. AUGUSTO SALDIVAR': 'J.A.Saldívar',
    'AREGUA': 'Areguá',
    'ITAUGUA': 'Itauguá',
    'CAPIATA': 'Capiatá',
    'SAN LORENZO': 'S.Lorenzo',
    'LUQUE': 'Luque',
    'GUARAMBARE': 'Guarambaré',
    'VILLETA': 'Villeta',
    'HERNANDARIAS': 'Hernandarias',
    'MINGA GUAZU': 'Minga Guazú',
    'SAN ALBERTO': 'S.Alberto',
    'DOCTOR RAUL PENA': 'Dr.R.Peña',
    'FRIDAY': 'Friday',
    'YGUAZU': 'Yguazú',
    'LOS CEDRALES': 'Los Cedrales',
    'MINGA PORA': 'Minga Porá',
    'NARANJAL': 'Naranjal',
    'SANTA RITA': 'Sta.Rita',
    'ITAKYRY': 'Itakyry',
    'JUAN LEON MALLORQUIN': 'J.L.Mallorquín',
    'PRESIDENTE FRANCO': 'Pte.Franco',
}

def abrev_nome(nome):
    n = nome.strip().upper()
    if n in ABREV:
        return ABREV[n]
    # Se nome longo (>15 chars), abreviar
    palavras = nome.title().split()
    if len(nome) <= 14:
        return nome.title()
    # Abreviar primeiras palavras
    resultado = []
    for p in palavras:
        if p.lower() in ('de','del','do','da','dos','das','e','y','el','la','los','las'):
            resultado.append(p.lower())
        elif len(resultado) > 0 and len(' '.join(resultado)) > 10:
            resultado.append(p[0] + '.')
        else:
            resultado.append(p)
    return ' '.join(resultado)


def extrair_gss_subscores():
    """Extrai GSS final e sub-scores A,B,C,D,E de todos os tex."""
    padrao_sec = re.compile(
        r'\\secaoDiagnostico\{[^}]+\}\{\\mapaDistrito\{([^}]+)\}\}',
        re.DOTALL
    )
    padrao_gss = re.compile(r'\\textbf\{GSS FINAL\}\s*&\s*\\textbf\{(\d+(?:[.,]\d+)?)\}')
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

            gss_m = padrao_gss.search(trecho)
            sub_m = padrao_sub.search(trecho)

            entry = {}
            if gss_m:
                entry['GSS'] = float(gss_m.group(1).replace(',', '.'))
            if sub_m:
                entry['A'] = float(sub_m.group(1).replace(',', '.'))
                entry['B'] = float(sub_m.group(2).replace(',', '.'))
                entry['C'] = float(sub_m.group(3).replace(',', '.'))
                entry['D'] = float(sub_m.group(4).replace(',', '.'))
                entry['E'] = float(sub_m.group(5).replace(',', '.'))
            if entry:
                dados[clave] = entry
    return dados


def painel_mapa(ax, gdf_dept_sel, gdf_outros_dept, gdf_distritos, coluna, norm, cmap,
                titulo_painel, unidade='', label_fn=None, pad_frac=0.15):
    """Desenha um painel temático para um departamento."""
    # Fundo: outros departamentos em cinza muito claro
    gdf_outros_dept.plot(ax=ax, color='#EBEBEB', edgecolor='#CCCCCC', linewidth=0.3, zorder=1)

    # Departamento selecionado: distritos coloridos
    sem = gdf_distritos[gdf_distritos[coluna].isna()]
    com = gdf_distritos[gdf_distritos[coluna].notna()]

    if not sem.empty:
        sem.plot(ax=ax, color='#D0D0D0', edgecolor='white', linewidth=0.4, zorder=2)
    if not com.empty:
        com.plot(ax=ax, column=coluna, cmap=cmap, norm=norm,
                 edgecolor='white', linewidth=0.5, zorder=3)

    # Contorno do departamento
    gdf_dept_sel.plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.2, zorder=4)

    # Rótulos nos distritos
    for _, row in gdf_distritos.iterrows():
        centroid = row['geometry'].centroid
        val = row.get(coluna)
        nome = abrev_nome(row['DIST_DESC_'])

        if pd.notna(val):
            val_str = f"{val:.1f}" if label_fn is None else label_fn(val)
        else:
            val_str = '?'

        # Texto: nome do distrito (pequeno) + valor (maior)
        txt_val = ax.text(centroid.x, centroid.y + 0.0,
                          val_str, ha='center', va='center',
                          fontsize=5.5, fontweight='bold', color='white',
                          fontfamily='DejaVu Sans', zorder=5)
        txt_val.set_path_effects([pe.withStroke(linewidth=1.2, foreground='black')])

        txt_nome = ax.text(centroid.x, centroid.y - 0.0,
                           nome, ha='center', va='top',
                           fontsize=3.8, color='#222222',
                           fontfamily='DejaVu Sans', zorder=5)

    # Zoom no departamento
    bx = gdf_distritos.total_bounds  # [xmin, ymin, xmax, ymax]
    span = max(bx[2]-bx[0], bx[3]-bx[1])
    pad = span * pad_frac
    ax.set_xlim(bx[0]-pad, bx[2]+pad)
    ax.set_ylim(bx[1]-pad, bx[3]+pad)
    ax.set_aspect('equal')
    ax.set_axis_off()
    ax.set_title(titulo_painel, fontsize=7, fontweight='bold', color=NAVY,
                 fontfamily='DejaVu Sans', pad=3)


def gerar_mapa_departamento(dpto_code, dpto_nome, gdf_dist_all, gdf_dept_all, dados_dict):
    """Gera figura 3-painel para um departamento."""
    gdf_dept_sel  = gdf_dept_all[gdf_dept_all['DPTO'] == dpto_code]
    gdf_outros    = gdf_dept_all[gdf_dept_all['DPTO'] != dpto_code]
    gdf_dist_dept = gdf_dist_all[gdf_dist_all['DPTO'] == dpto_code].copy()

    if gdf_dist_dept.empty:
        print(f"  [{dpto_code}] sem distritos — pulando")
        return None

    # Adicionar colunas de dados
    gdf_dist_dept['GSS']    = gdf_dist_dept['CLAVE'].map(
        lambda c: dados_dict[c]['GSS'] if c in dados_dict and 'GSS' in dados_dict[c] else None)
    gdf_dist_dept['RISCO_B'] = gdf_dist_dept['CLAVE'].map(
        lambda c: 10.0 - dados_dict[c]['B'] if c in dados_dict and 'B' in dados_dict[c] else None)
    gdf_dist_dept['AUTOSUF'] = gdf_dist_dept['CLAVE'].map(
        lambda c: dados_dict[c]['D'] if c in dados_dict and 'D' in dados_dict[c] else None)

    n_distritos = len(gdf_dist_dept)
    tem_dados = gdf_dist_dept['GSS'].notna().sum()

    # Layout: 1 linha × 3 colunas
    fig, axes = plt.subplots(1, 3, figsize=(12, 5.5), dpi=180)
    fig.patch.set_facecolor('none')

    # ── Painel 1: GSS ──────────────────────────────────────────────────────────
    norm_gss = mcolors.Normalize(vmin=3.5, vmax=9.0)
    painel_mapa(axes[0], gdf_dept_sel, gdf_outros, gdf_dist_dept, 'GSS',
                norm_gss, 'RdYlGn',
                f'GSS por Distrito\n(Global Safety Score)')

    sm1 = plt.cm.ScalarMappable(cmap='RdYlGn', norm=norm_gss)
    sm1.set_array([])
    cb1 = fig.colorbar(sm1, ax=axes[0], orientation='horizontal',
                       fraction=0.05, pad=0.02, shrink=0.85, aspect=20)
    cb1.ax.tick_params(labelsize=5.5, colors=NAVY)
    cb1.set_label('GSS (3.5–9.0)', fontsize=5.5, color=NAVY)
    cb1.outline.set_edgecolor(NAVY)

    # ── Painel 2: Risco Social (B invertido) ───────────────────────────────────
    norm_b = mcolors.Normalize(vmin=0, vmax=7)
    painel_mapa(axes[1], gdf_dept_sel, gdf_outros, gdf_dist_dept, 'RISCO_B',
                norm_b, 'YlOrRd',
                f'Risco Social\n(0=baixo · 7=alto)')

    sm2 = plt.cm.ScalarMappable(cmap='YlOrRd', norm=norm_b)
    sm2.set_array([])
    cb2 = fig.colorbar(sm2, ax=axes[1], orientation='horizontal',
                       fraction=0.05, pad=0.02, shrink=0.85, aspect=20)
    cb2.ax.tick_params(labelsize=5.5, colors=NAVY)
    cb2.set_label('Risco (0–7)', fontsize=5.5, color=NAVY)
    cb2.outline.set_edgecolor(NAVY)

    # ── Painel 3: Autossuficiência (D) ─────────────────────────────────────────
    norm_d = mcolors.Normalize(vmin=3.5, vmax=9.5)
    painel_mapa(axes[2], gdf_dept_sel, gdf_outros, gdf_dist_dept, 'AUTOSUF',
                norm_d, 'YlGn',
                f'Autossuficiência\n(Solo · Água · Energia)')

    sm3 = plt.cm.ScalarMappable(cmap='YlGn', norm=norm_d)
    sm3.set_array([])
    cb3 = fig.colorbar(sm3, ax=axes[2], orientation='horizontal',
                       fraction=0.05, pad=0.02, shrink=0.85, aspect=20)
    cb3.ax.tick_params(labelsize=5.5, colors=NAVY)
    cb3.set_label('Score D (3.5–9.5)', fontsize=5.5, color=NAVY)
    cb3.outline.set_edgecolor(NAVY)

    # Título geral
    distritos_com = gdf_dist_dept['GSS'].notna().sum()
    fig.suptitle(
        f'{dpto_nome.title()} — Análise Temática por Distrito  '
        f'({distritos_com}/{n_distritos} distritos com dados)',
        fontsize=9, fontweight='bold', color=NAVY,
        fontfamily='DejaVu Sans', y=1.01
    )

    plt.tight_layout(rect=[0, 0, 1, 1])

    fname = f"mapas_tematicos_dept_{dpto_code}.pdf"
    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='pdf', bbox_inches='tight',
                facecolor='none', transparent=True, dpi=180)
    plt.close(fig)
    return fname


def inserir_mapa_no_tex(dpto_code, dpto_nome_tex, fname_mapa):
    """Insere o mapa temático no arquivo tex do departamento."""
    # Encontrar o arquivo tex
    arquivos = [f for f in os.listdir(CAPS)
                if f.startswith(f'dept_{dpto_code}_') and f.endswith('.tex')]
    if not arquivos:
        print(f"  Arquivo tex não encontrado para dept {dpto_code}")
        return

    fpath = os.path.join(CAPS, arquivos[0])
    with open(fpath, encoding='utf-8') as f:
        conteudo = f.read()

    # Verificar se já foi inserido
    if fname_mapa in conteudo:
        print(f"  [{dpto_code}] mapa já presente no tex")
        return

    # Inserir após \vfill\clearpage (que vem depois do \mapaparaguai)
    marcador = r'\vfill\clearpage'
    bloco_mapa = (
        f'\n\\clearpage\n'
        f'\\subsection*{{Análise Temática por Distrito}}\n'
        f'\\addcontentsline{{toc}}{{subsection}}{{Análise Temática por Distrito}}\n'
        f'\n'
        f'Os mapas abaixo detalham, para cada distrito de {dpto_nome_tex}, '
        f'o GSS final, o nível de risco social e o potencial de autossuficiência. '
        f'Os valores são os calculados na metodologia GSS deste guia.\n'
        f'\n'
        f'\\begin{{figure}}[h!]\n'
        f'\\centering\n'
        f'\\includegraphics[width=\\textwidth]{{mapas/{fname_mapa}}}\n'
        f'\\caption{{Análise temática dos distritos de {dpto_nome_tex}: '
        f'GSS, risco social e autossuficiência. Fonte: análise deste guia (2024).}}\n'
        f'\\label{{fig:tematico-{dpto_code}}}\n'
        f'\\end{{figure}}\n'
        f'\n'
        f'\\clearpage\n'
    )

    # Substituir a primeira ocorrência de \vfill\clearpage
    novo_conteudo = conteudo.replace(marcador, marcador + bloco_mapa, 1)

    if novo_conteudo == conteudo:
        print(f"  [{dpto_code}] AVISO: marcador não encontrado em {arquivos[0]}")
        return

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)
    print(f"  [{dpto_code}] tex atualizado: {arquivos[0]}")


def main():
    print("Carregando GeoJSONs...")
    gdf_dist_all = gpd.read_file(DIST_GEO)
    gdf_dept_all = gpd.read_file(DEPT_GEO)

    print("Extraindo GSS e sub-scores dos tex...")
    dados = extrair_gss_subscores()
    print(f"  {len(dados)} distritos com dados")

    dept_list = sorted(gdf_dept_all['DPTO'].unique())

    print(f"\nGerando mapas para {len(dept_list)} departamentos...\n")

    for dpto_code in dept_list:
        row = gdf_dept_all[gdf_dept_all['DPTO'] == dpto_code].iloc[0]
        dpto_nome = row['DPTO_DESC']
        n_dist = len(gdf_dist_all[gdf_dist_all['DPTO'] == dpto_code])

        print(f"  [{dpto_code}] {dpto_nome} ({n_dist} distritos)...")

        fname = gerar_mapa_departamento(dpto_code, dpto_nome, gdf_dist_all, gdf_dept_all, dados)
        if fname:
            inserir_mapa_no_tex(dpto_code, dpto_nome.title(), fname)
            print(f"        → {fname}")

    print(f"\nConcluído! PDFs em {OUT}")
    print("Execute pdflatex para recompilar.")


if __name__ == "__main__":
    main()

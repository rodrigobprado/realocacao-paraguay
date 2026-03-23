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


def desenhar_mapa_unico(ax, gdf_dept_sel, gdf_outros_dept, gdf_distritos,
                        coluna, norm, cmap, titulo, pad_frac=0.12):
    """Desenha um mapa individual (largura total) para um departamento."""
    # Outros departamentos em cinza muito claro
    gdf_outros_dept.plot(ax=ax, color='#EBEBEB', edgecolor='#CCCCCC',
                         linewidth=0.3, zorder=1)

    sem = gdf_distritos[gdf_distritos[coluna].isna()]
    com = gdf_distritos[gdf_distritos[coluna].notna()]

    if not sem.empty:
        sem.plot(ax=ax, color='#C8C8C8', edgecolor='white', linewidth=0.6, zorder=2)
    if not com.empty:
        com.plot(ax=ax, column=coluna, cmap=cmap, norm=norm,
                 edgecolor='white', linewidth=0.8, zorder=3)

    # Contorno espesso do departamento
    gdf_dept_sel.plot(ax=ax, facecolor='none', edgecolor=NAVY, linewidth=1.8, zorder=4)

    # Rótulos — tamanhos maiores pois o mapa é maior
    for _, row in gdf_distritos.iterrows():
        centroid = row['geometry'].centroid
        val = row[coluna]
        nome = abrev_nome(row['DIST_DESC_'])

        val_str = f"{val:.1f}" if pd.notna(val) else '?'

        # Valor em destaque
        txt_v = ax.text(centroid.x, centroid.y,
                        val_str, ha='center', va='bottom',
                        fontsize=7.5, fontweight='bold', color='white',
                        fontfamily='DejaVu Sans', zorder=5)
        txt_v.set_path_effects([pe.withStroke(linewidth=2.0, foreground='#1A1A1A')])

        # Nome do distrito
        txt_n = ax.text(centroid.x, centroid.y,
                        nome, ha='center', va='top',
                        fontsize=5.5, color='#111111',
                        fontfamily='DejaVu Sans', zorder=5)
        txt_n.set_path_effects([pe.withStroke(linewidth=1.5, foreground='white')])

    # Zoom no departamento
    bx = gdf_distritos.total_bounds
    span = max(bx[2]-bx[0], bx[3]-bx[1])
    pad = span * pad_frac
    ax.set_xlim(bx[0]-pad, bx[2]+pad)
    ax.set_ylim(bx[1]-pad, bx[3]+pad)
    ax.set_aspect('equal')
    ax.set_axis_off()
    ax.set_title(titulo, fontsize=10, fontweight='bold', color=NAVY,
                 fontfamily='DejaVu Sans', pad=5)


def gerar_mapa_unico(dpto_code, dpto_nome, gdf_dist_dept, gdf_dept_sel,
                     gdf_outros, coluna, norm, cmap, titulo, sufixo):
    """Gera e salva um único mapa temático (largura A5)."""
    fig, ax = plt.subplots(figsize=(7, 6.5), dpi=150)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')

    desenhar_mapa_unico(ax, gdf_dept_sel, gdf_outros,
                        gdf_dist_dept, coluna, norm, cmap, titulo)

    # Barra de cor lateral
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical',
                        fraction=0.035, pad=0.02, shrink=0.75, aspect=22)
    cbar.ax.tick_params(labelsize=7, colors=NAVY)
    cbar.outline.set_edgecolor(NAVY)
    for lbl in cbar.ax.get_yticklabels():
        lbl.set_color(NAVY)
        lbl.set_fontfamily('DejaVu Sans')

    plt.tight_layout()
    fname = f"mapas_tematicos_dept_{dpto_code}_{sufixo}.png"
    out_path = os.path.join(OUT, fname)
    fig.savefig(out_path, format='png', bbox_inches='tight',
                dpi=150)
    plt.close(fig)
    return fname


def gerar_mapa_departamento(dpto_code, dpto_nome, gdf_dist_all, gdf_dept_all, dados_dict):
    """Gera 3 PDFs separados (GSS, risco social, autossuficiência) por departamento."""
    gdf_dept_sel  = gdf_dept_all[gdf_dept_all['DPTO'] == dpto_code]
    gdf_outros    = gdf_dept_all[gdf_dept_all['DPTO'] != dpto_code]
    gdf_dist_dept = gdf_dist_all[gdf_dist_all['DPTO'] == dpto_code].copy()

    if gdf_dist_dept.empty:
        print(f"  [{dpto_code}] sem distritos — pulando")
        return None, None, None

    gdf_dist_dept['GSS']     = gdf_dist_dept['CLAVE'].map(
        lambda c: dados_dict[c]['GSS'] if c in dados_dict and 'GSS' in dados_dict[c] else None)
    gdf_dist_dept['RISCO_B'] = gdf_dist_dept['CLAVE'].map(
        lambda c: 10.0 - dados_dict[c]['B'] if c in dados_dict and 'B' in dados_dict[c] else None)
    gdf_dist_dept['AUTOSUF'] = gdf_dist_dept['CLAVE'].map(
        lambda c: dados_dict[c]['D'] if c in dados_dict and 'D' in dados_dict[c] else None)

    n  = len(gdf_dist_dept)
    nc = int(gdf_dist_dept['GSS'].notna().sum())

    # ── Mapa 1: GSS ────────────────────────────────────────────────────────────
    f1 = gerar_mapa_unico(
        dpto_code, dpto_nome, gdf_dist_dept, gdf_dept_sel, gdf_outros,
        'GSS', mcolors.Normalize(3.5, 9.0), 'RdYlGn',
        f'{dpto_nome.title()} — GSS por Distrito  ({nc}/{n} com dados)',
        'gss'
    )

    # ── Mapa 2: Risco Social ───────────────────────────────────────────────────
    f2 = gerar_mapa_unico(
        dpto_code, dpto_nome, gdf_dist_dept, gdf_dept_sel, gdf_outros,
        'RISCO_B', mcolors.Normalize(0, 7), 'YlOrRd',
        f'{dpto_nome.title()} — Risco Social por Distrito  (0 = baixo · 7 = alto)',
        'risco'
    )

    # ── Mapa 3: Autossuficiência ───────────────────────────────────────────────
    f3 = gerar_mapa_unico(
        dpto_code, dpto_nome, gdf_dist_dept, gdf_dept_sel, gdf_outros,
        'AUTOSUF', mcolors.Normalize(3.5, 9.5), 'YlGn',
        f'{dpto_nome.title()} — Autossuficiência por Distrito  (Solo · Água · Energia)',
        'autosuf'
    )

    return f1, f2, f3


def remover_bloco_antigo(conteudo, dpto_code):
    """Remove o bloco de mapa temático combinado inserido anteriormente."""
    # Padrão do bloco antigo (figura única combinada)
    padrao = re.compile(
        r'\n\\clearpage\n'
        r'\\subsection\*\{Análise Temática por Distrito\}.*?'
        r'\\clearpage\n',
        re.DOTALL
    )
    novo = padrao.sub('\n', conteudo, count=1)
    return novo


def inserir_mapa_no_tex(dpto_code, dpto_nome_tex, f_gss, f_risco, f_autosuf):
    """Insere os 3 mapas sequenciais no arquivo tex do departamento."""
    arquivos = [f for f in os.listdir(CAPS)
                if f.startswith(f'dept_{dpto_code}_') and f.endswith('.tex')]
    if not arquivos:
        print(f"  Arquivo tex não encontrado para dept {dpto_code}")
        return

    fpath = os.path.join(CAPS, arquivos[0])
    with open(fpath, encoding='utf-8') as f:
        conteudo = f.read()

    # Remove bloco antigo (versão combinada 3-em-1) se existir
    conteudo = remover_bloco_antigo(conteudo, dpto_code)

    # Verificar se já está atualizado
    if f_gss in conteudo:
        print(f"  [{dpto_code}] mapas já presentes")
        return

    marcador = r'\vfill\clearpage'

    bloco = (
        f'\n'
        f'\\clearpage\n'
        f'\\subsection*{{Análise Temática por Distrito}}\n'
        f'\\addcontentsline{{toc}}{{subsection}}{{Análise Temática por Distrito}}\n'
        f'\n'
        f'Os mapas a seguir mostram, para cada distrito de {dpto_nome_tex}, '
        f'o GSS final (pontuação geral), o risco social (criminalidade e instabilidade) '
        f'e o potencial de autossuficiência (solo, água e energia). '
        f'Cada valor é o calculado na metodologia GSS deste guia.\n'
        f'\n'
        # Mapa 1 — GSS
        f'\\begin{{figure}}[h!]\n'
        f'\\centering\n'
        f'\\includegraphics[width=\\textwidth, height=0.55\\textheight, keepaspectratio]'
        f'{{mapas/{f_gss}}}\n'
        f'\\caption{{GSS (Global Safety Score) por distrito de {dpto_nome_tex}. '
        f'Verde = alta viabilidade · Vermelho = baixa viabilidade.}}\n'
        f'\\label{{fig:gss-{dpto_code}}}\n'
        f'\\end{{figure}}\n'
        f'\n'
        f'\\vspace{{0.5em}}\n'
        f'\n'
        # Mapa 2 — Risco Social
        f'\\begin{{figure}}[h!]\n'
        f'\\centering\n'
        f'\\includegraphics[width=\\textwidth, height=0.55\\textheight, keepaspectratio]'
        f'{{mapas/{f_risco}}}\n'
        f'\\caption{{Risco social por distrito de {dpto_nome_tex}. '
        f'Amarelo = baixo risco · Vermelho = alto risco.}}\n'
        f'\\label{{fig:risco-{dpto_code}}}\n'
        f'\\end{{figure}}\n'
        f'\n'
        f'\\clearpage\n'
        f'\n'
        # Mapa 3 — Autossuficiência
        f'\\begin{{figure}}[h!]\n'
        f'\\centering\n'
        f'\\includegraphics[width=\\textwidth, height=0.55\\textheight, keepaspectratio]'
        f'{{mapas/{f_autosuf}}}\n'
        f'\\caption{{Autossuficiência por distrito de {dpto_nome_tex}: '
        f'solo, recursos hídricos e potencial energético. '
        f'Branco = baixo · Verde escuro = alto.}}\n'
        f'\\label{{fig:autosuf-{dpto_code}}}\n'
        f'\\end{{figure}}\n'
        f'\n'
        f'\\clearpage\n'
    )

    novo_conteudo = conteudo.replace(marcador, marcador + bloco, 1)

    if novo_conteudo == conteudo:
        print(f"  [{dpto_code}] AVISO: marcador não encontrado")
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

        f1, f2, f3 = gerar_mapa_departamento(dpto_code, dpto_nome, gdf_dist_all, gdf_dept_all, dados)
        if f1:
            inserir_mapa_no_tex(dpto_code, dpto_nome.title(), f1, f2, f3)
            print(f"        → {f1} | {f2} | {f3}")

    print(f"\nConcluído! PNGs em {OUT}")
    print("Execute pdflatex para recompilar.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Gera livro_latex/capitulos/apendice_dados_departamentais.tex
com os dados departamentais coletados (SEGURANCA, IDH, PRESIDIO, POCOS,
SOLO, TERRA_RURAL, IMOVEL_URBANO, CELULAR, INTERNET).
Autônomo. Log: tarefas_enxame/gerar_apendice_latex.log
"""
import os, re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJ_DIR = os.path.dirname(BASE_DIR)
OUT_TEX  = os.path.join(PROJ_DIR, "livro_latex", "capitulos", "apendice_dados_departamentais.tex")
LOG_FILE = os.path.join(BASE_DIR, "gerar_apendice_latex.log")

DEPTS = [
    ("00_Distrito_Capital", "Distrito Capital (Asunción)"),
    ("01_Concepcion",       "Concepción"),
    ("02_San_Pedro",        "San Pedro"),
    ("03_Cordillera",       "Cordillera"),
    ("04_Guaira",           "Guairá"),
    ("05_Caaguazu",         "Caaguazú"),
    ("06_Caazapa",          "Caazapá"),
    ("07_Itapua",           "Itapúa"),
    ("08_Misiones",         "Misiones"),
    ("09_Paraguari",        "Paraguarí"),
    ("10_Alto_Parana",      "Alto Paraná"),
    ("11_Central",          "Central"),
    ("12_Neembucu",         "Ñeembucú"),
    ("13_Amambay",          "Amambay"),
    ("14_Canindeyu",        "Canindeyú"),
    ("15_Presidente_Hayes", "Presidente Hayes"),
    ("16_Boqueron",         "Boquerón"),
    ("17_Alto_Paraguay",    "Alto Paraguay"),
]

FILES = [
    ("SEGURANCA_DEPARTAMENTAL.md",  "Segurança Pública"),
    ("IDH_DEPARTAMENTAL.md",        "IDH e Desenvolvimento Humano"),
    ("PRESIDIOS_DEPARTAMENTAL.md",  "Sistema Prisional"),
    ("POCOS_ARTESIANOS.md",         "Recursos Hídricos Subterrâneos"),
    ("SOLO_DEPARTAMENTAL.md",       "Aptidão do Solo"),
    ("TERRA_RURAL_DEPARTAMENTAL.md","Terra Rural"),
    ("IMOVEL_URBANO_DEPARTAMENTAL.md","Mercado Imobiliário"),
    ("CELULAR_DEPARTAMENTAL.md",    "Cobertura Celular"),
    ("INTERNET_DEPARTAMENTAL.md",   "Internet"),
]

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def md_table_to_latex(md_table_lines):
    """Converte tabela markdown simples para LaTeX tabular."""
    rows = []
    for line in md_table_lines:
        line = line.strip()
        if not line or set(line.replace("|","").replace("-","").replace(" ","")) == set():
            continue  # linha separadora
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return ""
    ncols = len(rows[0])
    if ncols == 2:
        col_spec = (
            r">{\raggedright\arraybackslash}p{0.34\linewidth}"
            r" >{\raggedright\arraybackslash}p{0.62\linewidth}"
        )
    elif ncols == 3:
        col_spec = (
            r">{\raggedright\arraybackslash}p{0.30\linewidth}"
            r" >{\raggedright\arraybackslash}p{0.18\linewidth}"
            r" >{\raggedright\arraybackslash}p{0.44\linewidth}"
        )
    elif ncols == 4:
        col_spec = (
            r">{\raggedright\arraybackslash}p{0.24\linewidth}"
            r" >{\raggedright\arraybackslash}p{0.22\linewidth}"
            r" >{\raggedright\arraybackslash}p{0.18\linewidth}"
            r" >{\raggedright\arraybackslash}p{0.26\linewidth}"
        )
    else:
        col_spec = "l" + "X" * (ncols - 1)
    tex = [
        "{\\small",
        "\\setlength{\\tabcolsep}{3pt}",
        "\\renewcommand{\\arraystretch}{1.12}",
        f"\\begin{{tabularx}}{{\\linewidth}}{{{col_spec}}}",
        "\\toprule",
    ]
    for i, row in enumerate(rows):
        # Escapa caracteres especiais LaTeX
        cells = []
        for c in row:
            c = c.replace("&","\\&").replace("%","\\%").replace("_","\\_")
            c = c.replace("↑","$\\uparrow$").replace("↓","$\\downarrow$").replace("→","$\\rightarrow$")
            c = c.replace("≈","$\\approx$").replace("°","$^\\circ$").replace("×","$\\times$")
            c = c.replace("≥","$\\geq$").replace("≤","$\\leq$").replace("±","$\\pm$")
            c = c.replace("²","$^2$").replace("³","$^3$").replace("–","--").replace("—","---")
            c = c.replace("**","").replace("*","")
            cells.append(c)
        tex.append(" & ".join(cells) + " \\\\")
        if i == 0:
            tex.append("\\midrule")
    tex.append("\\bottomrule")
    tex.append("\\end{tabularx}")
    tex.append("}")
    return "\n".join(tex)

_SKIP_PATTERNS = re.compile(
    r'^\*{0,2}(Ano de refer[eê]ncia:|Atualizado em:|Fontes?:|Fontes?-base)'
    r'|^[-*]\s*https?://'
    r'|^https?://'
    r'|^[-*]\s*\[.*?\]\(https?://',
    re.IGNORECASE
)

def md_to_latex_snippet(md_content, max_chars=0):
    """Converte markdown para LaTeX. max_chars=0 = sem limite (evita tabelas truncadas)."""
    if max_chars and max_chars > 0:
        md_content = md_content[:max_chars]
    lines = md_content.split("\n")
    out = []
    in_table = False
    table_buf = []

    for line in lines:
        # Pula metadados editoriais e URLs
        if _SKIP_PATTERNS.match(line.strip()):
            continue
        # Remove data de acesso inline
        line = re.sub(r'\s*\(acesso em \d{4}-\d{2}-\d{2}\)', '', line)
        line = re.sub(r',?\s*acesso em \d{4}-\d{2}-\d{2}', '', line)
        # Remove URLs inline (mantém o texto ao redor)
        line = re.sub(r'https?://\S+', '', line)
        # Pula cabeçalhos H1/H2 e headings vazios (já temos no \subsection)
        if re.match(r'^#{1,2}(\s|$)', line):
            continue
        # H3 → \subsubsection*
        if line.startswith("### "):
            if in_table:
                out.append(md_table_to_latex(table_buf))
                table_buf = []; in_table = False
            title = line[4:].strip()
            title = title.replace("&","\\&").replace("%","\\%").replace("_","\\_")
            out.append(f"\n\\subsubsection*{{{title}}}")
            continue
        # Tabela
        if line.startswith("|"):
            in_table = True
            table_buf.append(line)
            continue
        else:
            if in_table:
                out.append(md_table_to_latex(table_buf))
                table_buf = []; in_table = False
        # Negrito
        line = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', line)
        # Itálico
        line = re.sub(r'\*(.+?)\*', r'\\textit{\1}', line)
        # Escapa especiais
        line = line.replace("&","\\&").replace("%","\\%").replace("↑","$\\uparrow$")
        line = line.replace("↓","$\\downarrow$").replace("→","$\\rightarrow$")
        line = line.replace("≈","$\\approx$").replace("°","$^\\circ$").replace("×","$\\times$")
        line = line.replace("≥","$\\geq$").replace("≤","$\\leq$").replace("±","$\\pm$")
        line = line.replace("²","$^2$").replace("³","$^3$").replace("–","--").replace("—","---")
        line = line.replace("_","\\_")
        # Linha em branco
        if line.strip() == "":
            out.append("")
        else:
            out.append(line)

    if in_table:
        out.append(md_table_to_latex(table_buf))

    return "\n".join(out)

def main():
    log("=== gerar_apendice_latex.py iniciado ===")

    tex_parts = [
        "% Gerado automaticamente por gerar_apendice_latex.py em 2026-03-20",
        "% NÃO EDITAR MANUALMENTE — regenerar via script",
        "",
        "\\chapter{Dados Departamentais Detalhados}",
        "\\label{chap:dados_departamentais}",
        "",
        "Este apêndice reúne os dados departamentais coletados durante a fase de cobertura 100\\%"
        " do projeto: segurança pública, IDH, sistema prisional, recursos hídricos, aptidão do solo,"
        " mercado imobiliário, telecomunicações e infraestrutura.",
        "",
    ]

    for dept_dir, dept_nome in DEPTS:
        dept_path = os.path.join(PROJ_DIR, "Departamentos", dept_dir)
        tex_parts.append(f"\n\\clearpage")
        tex_parts.append(f"\\section{{{dept_nome}}}")
        tex_parts.append(f"\\label{{sec:dept_{dept_dir}}}")
        tex_parts.append("")

        found_any = False
        for fname, title in FILES:
            fpath = os.path.join(dept_path, fname)
            if not os.path.exists(fpath):
                continue
            with open(fpath, encoding="utf-8") as f:
                content = f.read()
            if len(content.strip()) < 50:
                continue

            tex_parts.append(f"\\subsection{{{title}}}")
            snippet = md_to_latex_snippet(content)
            tex_parts.append(snippet)
            tex_parts.append("")
            found_any = True

        if not found_any:
            tex_parts.append("\\textit{Dados em coleta.}\n")

        log(f"  {dept_nome} processado")

    tex_content = "\n".join(tex_parts)

    with open(OUT_TEX, "w", encoding="utf-8") as f:
        f.write(tex_content)

    log(f"=== Concluído: {OUT_TEX} ===")
    log(f"Tamanho: {len(tex_content):,} caracteres")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Corrige sistematicamente os 5 problemas identificados na revisão LaTeX."""

import re
import os
import glob

CAPITULOS = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos"

# ── 1. Remove figura autosuf duplicada (segunda ocorrência) ──────────────────
def remover_autosuf_duplicada(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Padrão: bloco figure com autosuf (captura o bloco inteiro)
    padrao = r'(\n?\n?\\begin\{figure\}\[h[^]]*\]\n\\centering\n\\includegraphics\[.*?\]\{mapas/mapas_tematicos_dept_\d+_autosuf\.png\}\n\\caption\{[^}]*\}\n\\label\{fig:autosuf-\d+\}\n\\end\{figure\})'

    ocorrencias = list(re.finditer(padrao, content, re.DOTALL))
    if len(ocorrencias) >= 2:
        # Remove segunda ocorrência
        inicio = ocorrencias[1].start()
        fim    = ocorrencias[1].end()
        # Remove também \clearpage imediatamente após, se existir
        resto = content[fim:]
        resto_limpo = re.sub(r'^\s*\n?\s*\\clearpage\s*\n', '\n', resto, count=1)
        content = content[:inicio] + resto_limpo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# ── 2. Remove \label duplicados de \paragraph (irradiação/precipitação/etc) ──
def remover_labels_paragraph(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    original = content
    # Remove \label{...} que seguem imediatamente um \paragraph{...}
    # Padrão: qualquer \label{ depois de } fechando um \paragraph
    content = re.sub(
        r'(\\paragraph\{[^}]*\})\\label\{[^}]+\}',
        r'\1',
        content
    )
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# ── 3. Padroniza labels de capítulo (remove acentos de \label{dept:...}) ─────
MAPA_LABELS = {
    r'\\label\{dept:Guair[aá]\}':        r'\\label{dept:Guaira}',
    r'\\label\{dept:Caaguaz[uú]\}':      r'\\label{dept:Caaguazu}',
    r'\\label\{dept:Caazap[aá]\}':       r'\\label{dept:Caazapa}',
    r'\\label\{dept:Itap[uú]a\}':        r'\\label{dept:Itapua}',
    r'\\label\{dept:Paraguar[ií]\}':     r'\\label{dept:Paraguari}',
    r'\\label\{dept:Alto Paran[aá]\}':   r'\\label{dept:Alto Parana}',
    r'\\label\{dept:[ÑN]eembuc[uú]\}':   r'\\label{dept:Neembucu}',
    r'\\label\{dept:Canindey[uú]\}':     r'\\label{dept:Canindeyu}',
    r'\\label\{dept:Boquer[oó]n\}':      r'\\label{dept:Boqueron}',
}

def normalizar_labels_dept(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    original = content
    for padrao, substituto in MAPA_LABELS.items():
        content = re.sub(padrao, substituto, content)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# ── 4. Troca [h!] por [htbp] em \begin{figure} ───────────────────────────────
def corrigir_float_specifier(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    original = content
    content = re.sub(r'\\begin\{figure\}\[h[!]?\]', r'\\begin{figure}[htbp]', content)
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# ── EXECUÇÃO ─────────────────────────────────────────────────────────────────
dept_files = sorted(glob.glob(os.path.join(CAPITULOS, "dept_*.tex")))

print(f"Processando {len(dept_files)} arquivos de departamento...\n")

for fp in dept_files:
    nome = os.path.basename(fp)
    fixes = []

    if remover_autosuf_duplicada(fp):
        fixes.append("autosuf_duplicada")
    if remover_labels_paragraph(fp):
        fixes.append("labels_paragraph")
    if normalizar_labels_dept(fp):
        fixes.append("label_dept_acento")
    if corrigir_float_specifier(fp):
        fixes.append("[h!]→[htbp]")

    if fixes:
        print(f"  {nome}: {', '.join(fixes)}")
    else:
        print(f"  {nome}: sem alterações")

print("\nPronto! Agora corrija manualmente as tabelas largas.")

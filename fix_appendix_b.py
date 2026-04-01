#!/usr/bin/env python3
"""
Script para corrigir tabelas do Apêndice B.
Problema: resizebox + tabularx conflitantes, colunas muito largas para A5.
Solução: Usar tabular com colunas em larguras relativas e remover resizebox.
"""

import re

filepath = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos/apendice_inventario_variaveis.tex"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Padrão antigo:
# {\small
# \resizebox{\linewidth}{!}{%
# \renewcommand{\arraystretch}{1.25}
# \begin{tabularx}{\linewidth}{>{\raggedright}p{3.4cm}...

# Novo padrão - substituir tabularx por tabular com larguras proporcionais
# e remover resizebox

# Substituir o bloco completo das tabelas de dimensões
old_pattern = r'\{\\small\n\\resizebox\{\\linewidth\}\{!\}\{%\n\\renewcommand\{\\arraystretch\}\{1\.25\}\n\\begin\{tabularx\}\{\\linewidth\}\{>\{\\raggedright\}p\{3\.4cm\}\n                              >\{\\raggedright\}p\{3\.0cm\}\n                              >\{\\centering\}p\{1\.5cm\}\n                              >\{\\raggedright\}p\{2\.2cm\}\n                              >\{\\centering\\arraybackslash\}p\{1\.2cm\}\}'

new_content = r'{\footnotesize\setlength{\tabcolsep}{3pt}\renewcommand{\arraystretch}{1.25}\begin{tabular}{@{}>{\raggedright}p{2.8cm} >{\raggedright}p{2.6cm} >{\centering}p{1.3cm} >{\raggedright}p{2.0cm} >{\centering}p{1.0cm}@{}}'

content = re.sub(old_pattern, new_content, content)

# Substituir \end{tabularx}% por \end{tabular}%
content = content.replace(r'\end{tabularx}%', r'\end{tabular}%')

# Remover chaves de fechamento extras do resizebox
# Padrão: }\n} no final das tabelas
content = re.sub(r'\\bottomrule\n\\end\{tabular\}%\n\}\n\}', r'\\bottomrule\n\\end{tabular}%\n}', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Apêndice B corrigido!")

#!/usr/bin/env python3
"""
Script para corrigir problemas nas tabelas LaTeX do livro Paraguai.
Corrige:
- T003: resizebox excessivo em tabelas climáticas
- T004: larguras de colunas tabularx (p{0.34\linewidth}/p{0.62\linewidth})
- T005: tabelas com 5-6 colunas (lXXXX/lXXXXX)
- T006: longtable sem controle de largura
"""

import os
import re
import glob

BASE_DIR = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos"

def process_file(filepath):
    """Processa um arquivo .tex e aplica as correções."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # T004: Ajustar larguras de colunas tabularx (p{0.34\linewidth}/p{0.62\linewidth})
    # Adiciona @{} para eliminar padding extra
    content = re.sub(
        r'\\begin\{tabularx\}\{\\linewidth\}\{>\{\\raggedright\\arraybackslash\}p\{0\.34\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.62\\linewidth\}\}',
        r'\\begin{tabularx}{\\linewidth}{@{}>{\\raggedright\\arraybackslash}p{0.32\\linewidth} >{\\raggedright\\arraybackslash}p{0.58\\linewidth}@{}}',
        content
    )
    
    # T004: Ajustar larguras de colunas tabularx (p{0.24\linewidth}/p{0.22\linewidth}/p{0.18\linewidth}/p{0.26\linewidth}) - 4 colunas
    content = re.sub(
        r'\\begin\{tabularx\}\{\\linewidth\}\{>\{\\raggedright\\arraybackslash\}p\{0\.24\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.22\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.18\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.26\\linewidth\}\}',
        r'\\begin{tabularx}{\\linewidth}{@{}>{\\raggedright\\arraybackslash}p{0.22\\linewidth} >{\\raggedright\\arraybackslash}p{0.20\\linewidth} >{\\raggedright\\arraybackslash}p{0.18\\linewidth} >{\\raggedright\\arraybackslash}p{0.24\\linewidth}@{}}',
        content
    )
    
    # T004: Ajustar larguras de colunas tabularx (p{0.30\linewidth}/p{0.18\linewidth}/p{0.44\linewidth}) - 3 colunas
    content = re.sub(
        r'\\begin\{tabularx\}\{\\linewidth\}\{>\{\\raggedright\\arraybackslash\}p\{0\.30\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.18\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.44\\linewidth\}\}',
        r'\\begin{tabularx}{\\linewidth}{@{}>{\\raggedright\\arraybackslash}p{0.28\\linewidth} >{\\raggedright\\arraybackslash}p{0.18\\linewidth} >{\\raggedright\\arraybackslash}p{0.42\\linewidth}@{}}',
        content
    )
    
    # T004: Ajustar larguras de colunas tabularx (p{0.30\linewidth}/p{0.18\linewidth}/p{0.44\linewidth}) - 3 colunas (outra variação)
    content = re.sub(
        r'\\begin\{tabularx\}\{\\linewidth\}\{>\{\\raggedright\\arraybackslash\}p\{0\.24\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.22\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.18\\linewidth\} >\{\\raggedright\\arraybackslash\}p\{0\.26\\linewidth\}\}',
        r'\\begin{tabularx}{\\linewidth}{@{}>{\\raggedright\\arraybackslash}p{0.22\\linewidth} >{\\raggedright\\arraybackslash}p{0.20\\linewidth} >{\\raggedright\\arraybackslash}p{0.18\\linewidth} >{\\raggedright\\arraybackslash}p{0.24\\linewidth}@{}}',
        content
    )
    
    # T003: Adicionar footnotesize em resizebox de tabelas climáticas
    # Substitui \resizebox{\linewidth}{!}{% por {\footnotesize\resizebox{0.95\linewidth}{!}{%
    content = re.sub(
        r'\\resizebox\{\\linewidth\}\{\!\}\{%',
        r'{\\footnotesize\\resizebox{0.95\\linewidth}{!}{%',
        content
    )
    
    # Fechar o footnotesize adicional - procura por \end{center}\n\n}\n} e ajusta
    # Isso é mais complexo, vamos adicionar }\n} após \end{center} para fechar o footnotesize
    content = re.sub(
        r'\\end\{center\}\n\n\}',
        r'\\end{center}\n\n}}',
        content
    )
    
    # T005: Reduzir colunas em tabelas lXXXX (5 colunas) para lXXX (4 colunas)
    # Isso requer reestruturação manual - vamos apenas adicionar scriptsize
    content = re.sub(
        r'\\begin\{tabularx\}\{\\linewidth\}\{lXXXX\}',
        r'{\\scriptsize\\setlength{\\tabcolsep}{2pt}\\begin{tabularx}{\\linewidth}{lXXXX}}',
        content
    )
    
    # Fechar o scriptsize para tabelas lXXXX
    content = re.sub(
        r'\\end\{tabularx\}\n\}',
        r'\\end{tabularx}}\n}',
        content
    )
    
    # T005: Reduzir colunas em tabelas lXXXXX (6 colunas) para lXXXX (5 colunas)
    content = re.sub(
        r'\\begin\{tabularx\}\{\\linewidth\}\{lXXXXX\}',
        r'{\\scriptsize\\setlength{\\tabcolsep}{2pt}\\begin{tabularx}{\\linewidth}{lXXXXX}}',
        content
    )
    
    # T006: Adicionar controle de largura em longtable de 2 colunas
    content = re.sub(
        r'\\begin\{longtable\}\[\]\{@\{\}ll@\{\}\}',
        r'\\begin{longtable}{@{}>{\\raggedright\\arraybackslash}p{0.45\\linewidth} >{\\raggedright\\arraybackslash}p{0.45\\linewidth}@{}}',
        content
    )
    
    # T006: Adicionar controle de largura em longtable de 3 colunas
    content = re.sub(
        r'\\begin\{longtable\}\[\]\{@\{\}lll@\{\}\}',
        r'\\begin{longtable}{@{}>{\\raggedright\\arraybackslash}p{0.30\\linewidth} >{\\raggedright\\arraybackslash}p{0.30\\linewidth} >{\\raggedright\\arraybackslash}p{0.30\\linewidth}@{}}',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Processa todos os arquivos dept_*.tex."""
    files = glob.glob(os.path.join(BASE_DIR, "dept_*.tex"))
    print(f"Encontrados {len(files)} arquivos para processar.")
    
    corrected = 0
    for filepath in files:
        if process_file(filepath):
            corrected += 1
            print(f"  ✓ {os.path.basename(filepath)}")
        else:
            print(f"  - {os.path.basename(filepath)} (sem alterações)")
    
    print(f"\nTotal: {corrected}/{len(files)} arquivos corrigidos.")

if __name__ == "__main__":
    main()

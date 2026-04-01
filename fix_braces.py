#!/usr/bin/env python3
"""
Script para corrigir chaves extras nas tabelas climáticas.
"""

import os
import re
import glob

BASE_DIR = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos"

def process_file(filepath):
    """Processa um arquivo .tex e remove chaves extras."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Corrigir o fechamento de chaves para tabelas climáticas
    # Substituir \end{center}\n\n}}}\n} por \end{center}\n\n}}\n}
    content = re.sub(
        r'\\end\{center\}\n\n\}\}\}\n\}',
        r'\\end{center}\n\n}}\n}',
        content,
        flags=re.MULTILINE
    )
    
    # Também corrigir padrão alternativo
    content = re.sub(
        r'\\end\{center\}\n\}\}\n',
        r'\\end{center}\n}\n',
        content,
        flags=re.MULTILINE
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
    
    print(f"\nTotal: {corrected}/{len(files)} arquivos corrigidos.")

if __name__ == "__main__":
    main()

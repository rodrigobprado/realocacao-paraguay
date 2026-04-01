#!/usr/bin/env python3
"""
Script para adicionar labels em todos os \secaoDiagnostico.
Adiciona \label{dist:XX_Nome} após a linha do \secaoDiagnostico.
"""

import os
import re
import glob

BASE_DIR = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos"

def normalize_label(text):
    """Normaliza nome para formato de label."""
    replacements = [
        ('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'),
        ('ã', 'a'), ('õ', 'o'), ('â', 'a'), ('ê', 'e'), ('ô', 'o'),
        ('ç', 'c'), ('ñ', 'n'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text = text.lower()
    result = ''
    for c in text:
        if c.isalnum():
            result += c
        else:
            result += '_'
    while '__' in result:
        result = result.replace('__', '_')
    return result.strip('_')

def process_file(filepath):
    """Processa um arquivo .tex e adiciona labels."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    additions = 0
    dept_code = re.search(r'dept_(\d+)_', filepath)
    dept_code = dept_code.group(1) if dept_code else '00'
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if r'\secaoDiagnostico' in line and r'\label{dist:' not in line:
            # Extrair nome do distrito
            match = re.search(r'\\secaoDiagnostico\{([^}]+)\}', line)
            if match:
                nome = match.group(1)
                label_normalized = normalize_label(nome)
                label = f"dist:{dept_code}_{label_normalized}"
                
                # Adicionar linha com \label após a linha do \secaoDiagnostico
                new_lines.append(line)
                new_lines.append(f'\\label{{{label}}}\n')
                additions += 1
                i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    if additions > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    
    return additions

def main():
    files = glob.glob(os.path.join(BASE_DIR, "dept_*.tex"))
    print(f"Encontrados {len(files)} arquivos.\n")
    
    total = 0
    for filepath in files:
        additions = process_file(filepath)
        if additions > 0:
            print(f"  ✓ {os.path.basename(filepath)}: {additions} labels")
            total += additions
    
    print(f"\nTotal: {total} labels adicionadas.")

if __name__ == "__main__":
    main()

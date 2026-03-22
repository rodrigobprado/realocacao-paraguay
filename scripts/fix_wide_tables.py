#!/usr/bin/env python3
r"""
Corrige tabelas largas nos arquivos .tex para papel A5:

1. longtable com 8+ colunas (tabelas mensais Jan-Dez):
   Converte para tabular dentro de \resizebox{\linewidth}{!}{...}
   para garantir que caibam na margem.

2. tabularx com 5+ colunas X: aplica \small ao ambiente.
"""
import re
import os
import sys
import glob


def fix_wide_longtables(text):
    """
    Detecta longtable com 8+ colunas e converte para tabular dentro de resizebox.
    Longtables mensais (Jan-Dez + total = 13 cols) causam overflow no papel A5.
    """
    changes = 0

    longtable_re = re.compile(
        r'\\begin\{longtable\}\[.*?\]\{@\{\}(.*?)@\{\}\}(.*?)\\end\{longtable\}',
        re.DOTALL
    )

    def replace_longtable(m):
        nonlocal changes
        col_spec_inner = m.group(1)
        body = m.group(2)

        ncols = col_spec_inner.count(r'\real{')
        if ncols < 8:
            return m.group(0)

        # Extrai especificações de coluna simplificadas
        # O pandoc gera: >{\raggedright\arraybackslash}p{...}
        # Simplificamos para: c (centered)
        col_types = re.findall(r'>.*?p\{[^}]+\}', col_spec_inner)
        if len(col_types) == ncols:
            # Mantém as specs originais mas usa \linewidth / ncols
            tabular_spec = '@{\\hspace{1pt}}' + '@{\\hspace{1pt}}'.join(['c'] * ncols) + '@{\\hspace{1pt}}'
        else:
            tabular_spec = '@{}' + 'c' * ncols + '@{}'

        # Remove comandos longtable-specific do corpo
        # Longtable: \toprule...\endhead é o cabeçalho, \bottomrule...\endlastfoot é o rodapé
        # Conversão: cabeçalho + dados + \bottomrule final
        body_clean = body
        body_clean = re.sub(r'\\noalign\{\}', lambda _: '', body_clean)
        # Remove o bloco do footer (\bottomrule...\endlastfoot)
        body_clean = re.sub(r'\\bottomrule\n?\\endlastfoot\n?', lambda _: '', body_clean)
        body_clean = re.sub(r'\\endhead\n?', lambda _: '', body_clean)
        body_clean = re.sub(r'\\endlastfoot\n?', lambda _: '', body_clean)
        # Remove \bottomrule solto restante (será adicionado no template abaixo)
        body_clean = re.sub(r'\\bottomrule\n?', lambda _: '', body_clean)
        # Após remoções, garante \n após \toprule/\midrule
        body_clean = re.sub(
            r'(\\toprule|\\midrule)([^\n\\])',
            lambda mm: mm.group(1) + '\n' + mm.group(2),
            body_clean
        )
        # Remove linhas de minipage dos headers (simplifica para texto direto)
        body_clean = re.sub(
            r'\\begin\{minipage\}[^\n]*\n(.*?)\n\\end\{minipage\}',
            lambda mm: mm.group(1).strip(),
            body_clean,
            flags=re.DOTALL
        )

        new_block = (
            '\n\\begin{center}\n'
            '\\resizebox{\\linewidth}{!}{%\n'
            '\\begin{tabular}{' + tabular_spec + '}\n' +
            body_clean.strip() + '\n'
            '\\bottomrule\n'
            '\\end{tabular}%\n'
            '}\n'
            '\\end{center}\n'
        )
        changes += 1
        return new_block

    text_new = longtable_re.sub(replace_longtable, text)
    return text_new, changes


def fix_wide_tabularx(text):
    """
    Para tabularx com 5+ colunas X, envolve com {\\small ...} para reduzir fonte.
    """
    changes = 0

    # Captura o ambiente tabularx completo com 5+ X columns
    full_re = re.compile(
        r'(\\begin\{tabularx\}\{\\linewidth\}\{l(X{4,})\}.*?\\end\{tabularx\})',
        re.DOTALL
    )

    def wrap_small(m):
        nonlocal changes
        block = m.group(1)
        # Não aplica se já está dentro de {\\small
        changes += 1
        return '{\\small\n' + block + '\n}'

    # Evita aplicar duas vezes
    already_small_re = re.compile(
        r'\{\\small\n\\begin\{tabularx\}'
    )

    text_new = full_re.sub(wrap_small, text)

    # Se aplicou algum, registra
    if text_new != text:
        pass  # changes já foi contado

    return text_new, changes


def fix_content(text, filename):
    changes_list = []

    new_text, n = fix_wide_longtables(text)
    if n:
        changes_list.append(f'  longtable larga (8+ cols): {n} convertida(s) para resizebox+tabular')
        text = new_text

    new_text, n = fix_wide_tabularx(text)
    if n:
        changes_list.append(f'  tabularx larga (5+ X): {n} com \\small')
        text = new_text

    return text, changes_list


def main():
    if len(sys.argv) < 2:
        files = sorted(glob.glob(
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         'livro_latex', 'capitulos', 'dept_*.tex')
        ))
    else:
        files = sys.argv[1:]

    total_files = 0
    for path in files:
        with open(path, 'r', encoding='utf-8') as f:
            original = f.read()

        fixed, chg = fix_content(original, os.path.basename(path))

        if fixed != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            print(f'Corrigido: {os.path.basename(path)}')
            for c in chg:
                print(c)
            total_files += 1

    print(f'\nTotal de arquivos corrigidos: {total_files}/{len(files)}')


if __name__ == '__main__':
    main()

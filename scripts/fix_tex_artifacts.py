#!/usr/bin/env python3
"""
Corrige artefatos nos arquivos dept_*.tex gerados:
1. Remove blocos de texto "Notas (0-10) / Calculo / Classificação"
   (redundantes — a tabela GSS já cobre essa informação)
2. Remove linhas soltas "Fonte: NASA POWER ..." e "Fonte: ISRIC ..."
3. Remove referências inline "(Fonte: acesso: YYYY-MM-DD)"
4. Remove itens de lista que são apenas fontes ("Fonte MOPC/...")
5. Limpa blocos \begin{itemize}...\end{itemize} que ficaram vazios
"""
import re
import sys
import os


def fix_content(text):

    # 1. Remove blocos Notas/Calculo/Classificação
    # Padrão: começa em "Notas (0-10):" e termina após "Classificação: ..."
    # Pode ser seguido por um bloco itemize de fontes antes do próximo \subsubsection
    text = re.sub(
        r'\nNotas \(0-10\):.*?'
        r'Classifica[cç][aã]o:.*?(?=\n\\)',
        '\n',
        text,
        flags=re.DOTALL
    )

    # 2. Remove linhas soltas "Fonte: NASA POWER ..." e "Fonte: ISRIC ..."
    # (linhas que começam com "Fonte: " mas NÃO são \textbf{Fonte})
    text = re.sub(
        r'\nFonte: (?:NASA POWER|ISRIC)[^\n]*\n[^\\\n][^\n]*\n',
        '\n',
        text
    )
    # Qualquer linha remanescente que comece com "Fonte: " (sem \textbf)
    text = re.sub(r'\nFonte: [^\n]+\n', '\n', text)

    # 3. Remove referências inline "(Fonte: acesso: YYYY-MM-DD)"
    text = re.sub(r'\s*\(Fonte:\s*acesso:\s*\d{4}-\d{2}-\d{2}\)', '', text)

    # 4. Remove itens de lista cujo conteúdo começa com "Fonte XXXX/..." (sem \textbf)
    # O item pode ter conteúdo multi-linha (indentado com 2 espaços até o próximo \item ou \end{)
    text = re.sub(
        r'\n\\item\n  Fonte (?:[^\n]*\n)(?:  [^\n]*\n)*',
        '\n',
        text
    )

    # 5. Limpa blocos \begin{itemize}...\end{itemize} que ficaram sem \item
    # (remoção deixou apenas \tightlist e/ou texto solto)
    text = re.sub(
        r'\n\\begin\{itemize\}\n\\tightlist\n\\end\{itemize\}\n',
        '\n',
        text
    )
    text = re.sub(
        r'\n\\begin\{itemize\}\s*\\end\{itemize\}\n',
        '\n',
        text
    )
    # Remove blocos itemize sem \item (texto solto restante após remoção de Fonte items)
    text = re.sub(
        r'\n\\begin\{itemize\}\n\\tightlist\n(?:  [^\n]*\n)+\\end\{itemize\}\n',
        '\n',
        text
    )

    # 6. Limpa excesso de linhas vazias
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text


def main():
    if len(sys.argv) < 2:
        print("Uso: fix_tex_artifacts.py <arquivo.tex> [arquivo2.tex ...]")
        sys.exit(1)

    for path in sys.argv[1:]:
        with open(path, 'r', encoding='utf-8') as f:
            original = f.read()

        fixed = fix_content(original)

        if fixed != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            print(f"  Corrigido: {os.path.basename(path)}")
        else:
            print(f"  Sem alterações: {os.path.basename(path)}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Corrige problemas de formatação nos arquivos dept_*.tex e outros capítulos:

1. Remove \subsubsection{} vazios (heading sem título = linha em branco no PDF)
2. Substitui footnotes repetidas de siglas por \fineXXX (definidas em main.tex)
3. Remove listas numeradas aninhadas (enumerate dentro de itemize) que eram
   listas de pesquisa técnica — converte para lista simples
4. Remove blocos inteiros de "Pesquisa Técnica" (lista numerada de fontes
   que aparece após o Dossiê de Campo)
"""
import re
import os
import sys
import glob


# Mapeamento: texto da footnote → comando \fine...
FOOTNOTE_MAP = {
    'Instituto Nacional de Estadística (Instituto Nacional de Estatística), órgão oficial de dados demográficos e censitários.':
        r'\fineINE',
    'Secretaría de Emergencia Nacional (Secretaria de Emergência Nacional), órgão governamental de resposta a desastres.':
        r'\fineSEN',
    'Administración Nacional de Electricidade (Administração Nacional de Eletricidade), companhia estatal de energia.':
        r'\fineANDE',
    'Empresa de Servicios Sanitarios del Paraguay (Empresa de Serviços Sanitários do Paraguai), responsável pelo saneamento e água urbana.':
        r'\fineESSAP',
    'Ejército del Pueblo Paraguayo (Exército do Povo Paraguaio), grupo insurgente marxista-leninista que atua principalmente no norte do país.':
        r'\fineEPP',
}


def fix_content(text, filename):
    changes = []

    # 1. Remove \subsubsection{} vazios (heading sem texto)
    count_before = text.count(r'\subsubsection{}')
    text = re.sub(r'\n\\subsubsection\{\}\n', '\n', text)
    count_after = text.count(r'\subsubsection{}')
    removed = count_before - count_after
    if removed:
        changes.append(f'  subsubsection{{}}: removidos {removed}')

    # 2. Substitui footnotes repetidas por \fineXXX
    for footnote_text, cmd in FOOTNOTE_MAP.items():
        pattern = r'\\footnote\{' + re.escape(footnote_text) + r'\}'
        replacement = r'\\footnote{' + cmd + r'}'
        new_text = text.replace(
            r'\footnote{' + footnote_text + '}',
            r'\footnote{' + cmd + '}'
        )
        if new_text != text:
            count = text.count(r'\footnote{' + footnote_text + '}')
            changes.append(f'  footnote {cmd}: {count} substituições')
            text = new_text

    # 3. Remove blocos de "Pesquisa Técnica" — lista numerada de fontes
    # Padrão: sequência de \item\n  \begin{enumerate}\n  \def\labelenumi...\n  \item\n    Texto\n  \end{enumerate}
    # dentro de \begin{itemize}...\end{itemize}
    # Essas listas não têm conteúdo editorial — são só listas de fontes de pesquisa

    # Detecta e remove blocos: \begin{itemize}\tightlist com conteúdo apenas de enumerate aninhados
    # A heurística: se o bloco itemize contém SOMENTE \item { \begin{enumerate}...\end{enumerate} }
    # (sem \textbf, sem descrição relevante fora do enumerate), é lista de pesquisa técnica

    def is_research_list(block_content):
        """Retorna True se o bloco é apenas lista de fontes de pesquisa técnica."""
        # Remove whitespace e analisa estrutura
        lines = [l.strip() for l in block_content.split('\n') if l.strip()]
        # Deve conter apenas: \item, \begin{enumerate}, \def\labelenumi, \tightlist,
        # \setcounter, \item (conteúdo), \end{enumerate}
        non_list_content = [
            l for l in lines
            if l and not any(l.startswith(p) for p in [
                r'\item', r'\begin{enumerate}', r'\end{enumerate}',
                r'\def\labelenumi', r'\tightlist', r'\setcounter',
                r'\begin{itemize}', r'\end{itemize}',
            ])
        ]
        # Se tem \textbf é conteúdo editorial
        has_bold = any(r'\textbf' in l for l in non_list_content)
        # Se tem texto longo (>80 chars) é conteúdo editorial
        has_long_text = any(len(l) > 80 for l in non_list_content)
        return not has_bold and not has_long_text

    # Remove blocos itemize de pesquisa técnica entre o fim do Dossiê e o próximo heading
    research_pattern = re.compile(
        r'\n(\\begin\{itemize\}\n\\tightlist\n(?:.*?\n)*?\\end\{itemize\})\n',
        re.DOTALL
    )

    def maybe_remove_research(m):
        block = m.group(1)
        if is_research_list(block):
            return '\n'
        return m.group(0)

    text_new = research_pattern.sub(maybe_remove_research, text)
    if text_new != text:
        changes.append('  blocos de lista de pesquisa técnica: removidos')
        text = text_new

    # 4. Limpa excesso de linhas vazias resultante
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text, changes


def main():
    if len(sys.argv) < 2:
        # Processa todos os dept_*.tex
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

        fixed, changes = fix_content(original, os.path.basename(path))

        if fixed != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed)
            print(f'Corrigido: {os.path.basename(path)}')
            for c in changes:
                print(c)
            total_files += 1
        else:
            pass  # sem alterações — silencioso

    print(f'\nTotal de arquivos corrigidos: {total_files}/{len(files)}')


if __name__ == '__main__':
    main()

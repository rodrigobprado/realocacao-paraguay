#!/usr/bin/env python3
"""
Integra o conteúdo de apendice_dados_departamentais.tex diretamente
em cada dept_*.tex, antes das entradas de distrito (\secaoDiagnostico).

O bloco \subsection*{Dados Departamentais} existente é substituído pelo
conteúdo completo do apêndice para aquele departamento (mais rico).

Após a integração, apendice_dados_departamentais.tex deve ser removido
do main.tex (o script apenas modifica os dept_*.tex).
"""
import re
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APENDICE = os.path.join(BASE, "livro_latex", "capitulos", "apendice_dados_departamentais.tex")
CAPS_DIR = os.path.join(BASE, "livro_latex", "capitulos")

# Mapeamento: número de ordem no apêndice → nome do arquivo dept_*.tex
DEPT_FILES = [
    "dept_00_Distrito_Capital.tex",
    "dept_01_Concepcion.tex",
    "dept_02_San_Pedro.tex",
    "dept_03_Cordillera.tex",
    "dept_04_Guaira.tex",
    "dept_05_Caaguazu.tex",
    "dept_06_Caazapa.tex",
    "dept_07_Itapua.tex",
    "dept_08_Misiones.tex",
    "dept_09_Paraguari.tex",
    "dept_10_Alto_Parana.tex",
    "dept_11_Central.tex",
    "dept_12_Neembucu.tex",
    "dept_13_Amambay.tex",
    "dept_14_Canindeyu.tex",
    "dept_15_Presidente_Hayes.tex",
    "dept_16_Boqueron.tex",
    "dept_17_Alto_Paraguay.tex",
]


def split_apendice(apendice_text):
    """
    Divide o texto do apêndice em seções por departamento.
    Retorna lista de strings (uma por departamento), sem o cabeçalho do capítulo.
    """
    # Remove o cabeçalho do capítulo (tudo antes do primeiro \clearpage\n\section)
    # e divide nas fronteiras \clearpage\n\section{...}
    dept_sections = re.split(r'\n\\clearpage\n(?=\\section\{)', apendice_text)

    # O primeiro elemento é o cabeçalho do capítulo — descartar
    dept_sections = dept_sections[1:]

    cleaned = []
    for sec in dept_sections:
        # Remove a linha \section{...} e \label{...} do topo (dept já tem seu próprio \section)
        sec = re.sub(r'^\\section\{[^}]*\}\n', '', sec)
        sec = re.sub(r'^\\label\{[^}]*\}\n', '', sec)
        # Remove linha "Fonte principal:" e "Data de referência:" soltas (sem \textbf)
        sec = re.sub(r'(?m)^\\textbf\{(?:Fonte principal|Data de refer[eê]ncia):\}[^\n]*\n', '', sec)
        # Ajusta nível dos headings: \subsection → \subsection* (sem numerar)
        sec = re.sub(r'\\subsection\{', r'\\subsection*{', sec)
        # Linhas com apenas "-" (bullets markdown que escaparam) → remover
        sec = re.sub(r'(?m)^- [^\n]+\n', '', sec)
        # Limpa excesso de linhas em branco
        sec = re.sub(r'\n{3,}', '\n\n', sec)
        cleaned.append(sec.strip())

    return cleaned


def integrate_dept(dept_tex_path, apendice_content):
    """
    Insere apendice_content no dept_*.tex, substituindo o bloco
    \clearpage\n\subsection*{Dados Departamentais}...até o ponto antes
    de \clearpage\n\newpage\n\secaoDiagnostico.
    """
    with open(dept_tex_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Padrão do bloco existente: \clearpage seguido de \subsection*{Dados Departamentais}
    # até o \clearpage\n\newpage antes do primeiro \secaoDiagnostico
    pattern = re.compile(
        r'\n\\clearpage\n\\subsection\*\{Dados Departamentais\}.*?(?=\n\\clearpage\n\\newpage\n\\secaoDiagnostico)',
        re.DOTALL
    )

    replacement_block = (
        '\n\\clearpage\n'
        '\\subsection*{Dados Departamentais}\n\n'
        + apendice_content +
        '\n'
    )

    # Usar função para evitar interpretação de \c, \n etc no replacement do re.sub
    new_text = pattern.sub(lambda m: replacement_block, text)
    count = 0 if new_text == text else 1

    if count == 0:
        # Fallback: sem bloco existente — inserir antes do primeiro \secaoDiagnostico
        insert_marker = '\n\\clearpage\n\\newpage\n\\secaoDiagnostico'
        pos = new_text.find(insert_marker)
        if pos == -1:
            print(f"  AVISO: não encontrou ponto de inserção em {os.path.basename(dept_tex_path)}")
            return False
        new_text = (
            new_text[:pos]
            + '\n\\clearpage\n\\subsection*{Dados Departamentais}\n\n'
            + apendice_content
            + '\n'
            + new_text[pos:]
        )

    with open(dept_tex_path, 'w', encoding='utf-8') as f:
        f.write(new_text)

    return True


def main():
    if not os.path.exists(APENDICE):
        print(f"ERRO: arquivo não encontrado: {APENDICE}")
        sys.exit(1)

    with open(APENDICE, 'r', encoding='utf-8') as f:
        apendice_text = f.read()

    dept_sections = split_apendice(apendice_text)
    print(f"Seções extraídas do apêndice: {len(dept_sections)}")

    if len(dept_sections) != len(DEPT_FILES):
        print(f"AVISO: {len(dept_sections)} seções no apêndice mas {len(DEPT_FILES)} arquivos esperados")

    for i, (dept_file, content) in enumerate(zip(DEPT_FILES, dept_sections)):
        dept_path = os.path.join(CAPS_DIR, dept_file)
        if not os.path.exists(dept_path):
            print(f"  AVISO: arquivo não existe: {dept_file}")
            continue
        ok = integrate_dept(dept_path, content)
        if ok:
            print(f"  OK: {dept_file}")
        else:
            print(f"  FALHOU: {dept_file}")

    print("\nIntegração concluída.")
    print("Próximo passo: comentar/remover o \\include{capitulos/apendice_dados_departamentais} no main.tex")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Corrige todos os DADOS.md de 262 distritos:
  1. Precipitação: converte tabela de mm/dia → mm/mês (valores reais)
  2. Precipitação: converte bullet-format de mm/dia → mm/mês
  3. Remove '(acesso em YYYY-MM-DD)' de todo o texto
  4. Remove headings de seção com data de acesso inline
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Dias reais por mês (Fev com 0.25 para fechar 365.25 dias/ano)
MONTH_DAYS = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_NAMES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
               'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']


def convert_precip_table(text):
    """
    Encontra '#### Precipitação (mm/dia)' seguida de tabela Markdown
    e converte cada valor mensal de mm/dia → mm/mês.
    Altera também o título de (mm/dia) → (mm/mês).
    """
    lines = text.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if '#### Precipitação' in line and 'mm/dia' in line:
            # Substituir título
            new_lines.append(line.replace('mm/dia', 'mm/mês'))
            i += 1
            # Processar linhas da tabela
            while i < len(lines):
                l = lines[i]
                stripped = l.strip()
                if not stripped:
                    # Linha em branco: manter e continuar
                    new_lines.append(l)
                    i += 1
                elif '|' in l and re.search(r'\d+\.\d+', l):
                    # Linha de dados com decimais → converter
                    parts = l.split('|')
                    new_parts = []
                    val_idx = 0
                    for p in parts:
                        ps = p.strip()
                        if re.match(r'^\d+\.\d+$', ps) and val_idx < 12:
                            val_mes = int(round(float(ps) * MONTH_DAYS[val_idx]))
                            new_parts.append(f' {val_mes} ')
                            val_idx += 1
                        else:
                            new_parts.append(p)
                    new_lines.append('|'.join(new_parts))
                    i += 1
                    break  # Apenas uma linha de dados por bloco
                elif '|' in l:
                    # Cabeçalho ou separador da tabela: manter
                    new_lines.append(l)
                    i += 1
                else:
                    # Fim da tabela
                    break
        else:
            new_lines.append(line)
            i += 1
    return '\n'.join(new_lines)


def convert_precip_bold_table(text):
    """
    Converte formato: **Precipitação — PRECTOTCORR (mm/dia → mm/ano ~X):**
    seguido de tabela markdown (sem coluna Total/ano).
    Altera o rótulo para 'mm/mês → mm/ano ~X' e converte valores.
    """
    lines = text.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detecta "**Precipitação ... (mm/dia → mm/ano ..." sem "- " no início
        if (re.match(r'^\*\*Precipita', line) and
                'mm/dia' in line and 'mm/ano' in line):
            # Substituir somente a parte "mm/dia" → "mm/mês" na label
            new_lines.append(line.replace('mm/dia', 'mm/mês'))
            i += 1
            while i < len(lines):
                l = lines[i]
                if not l.strip():
                    new_lines.append(l)
                    i += 1
                elif '|' in l and re.search(r'\d+\.\d+', l):
                    # Linha de dados: converter
                    parts = l.split('|')
                    new_parts = []
                    val_idx = 0
                    for p in parts:
                        ps = p.strip()
                        if re.match(r'^\d+\.\d+$', ps) and val_idx < 12:
                            val_mes = int(round(float(ps) * MONTH_DAYS[val_idx]))
                            new_parts.append(f' {val_mes} ')
                            val_idx += 1
                        else:
                            new_parts.append(p)
                    new_lines.append('|'.join(new_parts))
                    i += 1
                    break
                elif '|' in l:
                    new_lines.append(l)
                    i += 1
                else:
                    break
        else:
            new_lines.append(line)
            i += 1
    return '\n'.join(new_lines)


def convert_precip_bullet(text):
    """
    Converte bullet do tipo:
      - **Precipitação — PRECTOTCORR (mm/dia):** Jan 4.06 | Fev 4.92 | ...
    para:
      - **Precipitação — PRECTOTCORR (mm/mês):** Jan 126 | Fev 139 | ...
    """
    month_pat = '|'.join(MONTH_NAMES)

    def repl_values(m):
        month = m.group(1)
        val_dia = float(m.group(2))
        idx = MONTH_NAMES.index(month)
        val_mes = int(round(val_dia * MONTH_DAYS[idx]))
        return f'{month} {val_mes}'

    def repl_bullet(m):
        label = m.group(1).replace('mm/dia', 'mm/mês')
        body = m.group(2)
        body = re.sub(rf'({month_pat}) (\d+\.\d+)', repl_values, body)
        return label + body

    # Padrão: - **Precipitação ...(mm/dia):** <resto da linha>
    # Nota: o ':' vem ANTES do '**' de fechamento: **Precipitação ...:**
    text = re.sub(
        r'(- \*\*Precipita[çc][ãa]o[^*]*:\*\*)(.*?)(?=\n|$)',
        repl_bullet,
        text,
        flags=re.MULTILINE
    )
    return text


def remove_acesso_em(text):
    """
    Remove referências de data de acesso:
      - '(acesso em YYYY-MM-DD)' em qualquer contexto
      - 'acesso em YYYY-MM-DD' sem parênteses após vírgula/espaço
    """
    # Remove "(acesso em YYYY-MM-DD)" com espaço antes opcional
    text = re.sub(r'\s*\(acesso em \d{4}-\d{2}-\d{2}\)', '', text)
    # Remove ", acesso em YYYY-MM-DD" sem parênteses
    text = re.sub(r',?\s*acesso em \d{4}-\d{2}-\d{2}', '', text)
    # Remove "## Pesquisa oficial consolidada" sem nada depois (a data foi removida)
    # Não remove o heading em si, apenas a data que já foi removida acima
    # Limpa linhas de fonte que ficaram só com label vazio:
    # Ex: "- Fonte INE: " (URL já foi removida em edições anteriores)
    text = re.sub(r'(?m)^([ \t]*-[ \t]+Fonte[^:\n]+):[ \t]*\n', '\n', text)
    # Limpa excesso de linhas em branco
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def fix_dados_md(path):
    original = path.read_text(encoding='utf-8')
    text = original

    text = convert_precip_table(text)
    text = convert_precip_bold_table(text)
    text = convert_precip_bullet(text)
    text = remove_acesso_em(text)

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def convert_leitores_alfa(text):
    """
    Converte precipitação em LEITORES_ALFA.md (dois formatos):
    Formato A — inline: **Precipitação ...:** \n Jan 4.06 | Fev 4.92 | ...
    Formato B — tabela: **Precipitação ...:** \n\n | Jan | ... | \n |---|\n | 5.02 | ...
    """
    month_pat = '|'.join(MONTH_NAMES)
    lines = text.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detecta label de precipitação: **Precipitação ... (mm/dia) ...:**
        if re.match(r'^\*\*Precipita', line) and 'mm/dia' in line:
            new_lines.append(line.replace('mm/dia', 'mm/mês'))
            i += 1
            # Pular linhas vazias
            while i < len(lines) and not lines[i].strip():
                new_lines.append(lines[i])
                i += 1
            if i >= len(lines):
                break
            next_line = lines[i]
            if next_line.startswith('| Jan'):
                # Formato B: Markdown table — pular header, passar separador, converter dados
                new_lines.append(next_line)  # | Jan | Fev | ... |
                i += 1
                if i < len(lines) and '|' in lines[i] and re.match(r'^[ |*-]+$', lines[i].replace(' ', '')):
                    new_lines.append(lines[i])  # |---|---|...
                    i += 1
                if i < len(lines) and '|' in lines[i] and re.search(r'\d+\.\d+', lines[i]):
                    parts = lines[i].split('|')
                    new_parts = []
                    val_idx = 0
                    for p in parts:
                        ps = p.strip()
                        if re.match(r'^\d+\.\d+$', ps) and val_idx < 12:
                            new_parts.append(f' {int(round(float(ps) * MONTH_DAYS[val_idx]))} ')
                            val_idx += 1
                        else:
                            new_parts.append(p)
                    new_lines.append('|'.join(new_parts))
                    i += 1
            elif re.match(rf'({month_pat}) \d+\.\d+', next_line):
                # Formato A: inline — Jan 4.06 | Fev 4.92 | ...
                def repl_month(m):
                    month = m.group(1)
                    val_dia = float(m.group(2))
                    idx = MONTH_NAMES.index(month)
                    return f'{month} {int(round(val_dia * MONTH_DAYS[idx]))}'
                new_line = re.sub(rf'({month_pat}) (\d+\.\d+)', repl_month, next_line)
                new_lines.append(new_line)
                i += 1
            else:
                # Outro formato: manter como está
                new_lines.append(next_line)
                i += 1
        else:
            new_lines.append(line)
            i += 1
    return '\n'.join(new_lines)


def fix_leitores_alfa(path):
    original = path.read_text(encoding='utf-8')
    text = original
    text = convert_leitores_alfa(text)
    text = remove_acesso_em(text)
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def main():
    # 1. Corrigir todos os DADOS.md
    dados_files = sorted(BASE_DIR.glob('Departamentos/*/*/DADOS.md'))
    print(f'Processando {len(dados_files)} arquivos DADOS.md...\n')
    ok = unchanged = 0
    for f in dados_files:
        if fix_dados_md(f):
            ok += 1
        else:
            unchanged += 1
    print(f'  Atualizados: {ok}  |  Sem mudança: {unchanged}  |  Total: {len(dados_files)}')

    # 2. Corrigir LEITORES_ALFA.md e pacotes PKG
    alfa_files = sorted((BASE_DIR / 'tarefas_enxame/entregaveis_livro').glob('LEITORES_ALFA*.md'))
    print(f'\nProcessando {len(alfa_files)} arquivo(s) LEITORES_ALFA...')
    for p in alfa_files:
        changed = fix_leitores_alfa(p)
        if changed:
            print(f'  ✓ {p.name}')


if __name__ == '__main__':
    main()

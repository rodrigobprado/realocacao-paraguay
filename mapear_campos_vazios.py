#!/usr/bin/env python3
"""
Mapeia campos vazios/placeholders em todos os arquivos .tex dos capítulos.
Gera relatório CSV e texto com localização exata de cada campo vazio.
"""

import os
import re
import csv
from collections import defaultdict

BASE  = os.path.dirname(os.path.abspath(__file__))
CAPS  = os.path.join(BASE, "livro_latex", "capitulos")
OUT   = os.path.join(BASE, "relatorio_campos_vazios.csv")
OUT_TXT = os.path.join(BASE, "relatorio_campos_vazios.txt")

# ── Padrões de campos vazios ──────────────────────────────────────────────────
# (regex, descrição do problema, prioridade)
PADROES = [
    # Cabeçalhos sem conteúdo: \textbf{Áreas recomendadas:} seguido de linha em branco ou outro \textbf
    (r'\\textbf\{Áreas recomendadas:\}\s*\n\s*\n', 'Áreas recomendadas: vazio', 'alta'),
    (r'\\textbf\{Armadilhas comuns:\}\s*\n\s*\n', 'Armadilhas comuns: vazio', 'alta'),
    (r'\\textbf\{Áreas recomendadas:\}\s*\n\s*\\textbf', 'Áreas recomendadas: sem conteúdo', 'alta'),
    (r'\\textbf\{Armadilhas comuns:\}\s*\n\s*\\', 'Armadilhas comuns: sem conteúdo', 'alta'),

    # Por que sim / Por que não vazios
    (r'\\subsubsection\{Por que sim\}\s*\n\s*\n\s*\\subsubsection', 'Por que sim: vazio', 'alta'),
    (r'\\subsubsection\{Por que não\}\s*\n\s*\n\s*\\subsubsection', 'Por que não: vazio', 'alta'),
    (r'\\subsubsection\{Por que sim\}\s*\n\s*\n\s*\\begin', 'Por que sim: pulou para tabela', 'alta'),
    (r'\\subsubsection\{Por que não\}\s*\n\s*\n\s*\\begin', 'Por que não: pulou para tabela', 'alta'),

    # Células de tabela com --- (dado ausente)
    (r'& ---\s*\\\\', 'Célula tabela com --- (dado ausente)', 'media'),
    (r'& ---\s*&', 'Célula tabela com --- (dado ausente)', 'media'),

    # Valores explicitamente ausentes
    (r'dados não disponíveis|não disponível|N/D|nd\b|n\.d\.', 'Dado explicitamente ausente', 'media'),
    (r'a preencher|preencher|PREENCHER|FIXME|\?\?\?', 'Placeholder explícito', 'alta'),
    (r'\bTODO\b', 'Placeholder TODO (tarefa)', 'alta'),

    # Seções de texto com apenas heading, sem parágrafo
    (r'\\subsection\*\{[^}]+\}\s*\n\s*\n\s*\\subsection', 'Subseção vazia (sem conteúdo)', 'media'),

    # item vazio (lista sem conteúdo)
    (r'\\item\s*\n\s*\\item', 'Item de lista vazio', 'alta'),
    (r'\\item\s*\n\s*\\end\{itemize\}', 'Último item de lista vazio', 'alta'),

    # Dossiê de campo com valor vazio
    (r'\\item\[[^\]]+\]\s*\n', 'Item de dossiê com valor vazio (sem texto após])', 'media'),

    # Seção de internet / Cobertura de internet sem dados de ISP locais
    (r'A cobertura de internet fixa no interior de [A-Za-záéíóúãõâêôçñÁÉÍÓÚÃÕÂÊÔÇÑ\s]+ é \*\*limitada\*\*\.\s*\n\s*\n\s*Para fazendas', 'Internet: faltam ISPs locais listados', 'baixa'),
]

# ── Padrões linha a linha ─────────────────────────────────────────────────────
PADROES_LINHA = [
    # Áreas recomendadas sem conteúdo na linha seguinte
    (r'^\\textbf\{Áreas recomendadas:\}$', 'seguido_de_vazio', 'Áreas recomendadas vazio', 'alta'),
    (r'^\\textbf\{Armadilhas comuns:\}$', 'seguido_de_vazio', 'Armadilhas comuns vazio', 'alta'),
    # Item de dossiê sem valor
    (r'^\\item\[([^\]]+)\]\s*$', None, 'Dossiê: campo sem valor', 'alta'),
    # Célula com traço
    (r'& ---\s*(\\\\|&)', None, 'Célula tabela vazia (---)', 'media'),
]

def extrair_distrito_atual(linhas, idx):
    """Retorna o nome do distrito mais próximo antes da linha idx."""
    for i in range(idx, -1, -1):
        m = re.search(r'\\secaoDiagnostico\{([^}]+)\}', linhas[i])
        if m:
            return m.group(1)
        m = re.search(r'\\chapter\{([^}]+)\}', linhas[i])
        if m:
            return f"[Dept] {m.group(1)}"
    return "desconhecido"

def analisar_arquivo(fpath):
    """Analisa um arquivo .tex e retorna lista de (linha, tipo, distrito, prioridade)."""
    with open(fpath, encoding='utf-8') as f:
        conteudo = f.read()
        linhas = conteudo.splitlines()

    resultados = []
    fname = os.path.basename(fpath)

    # ── Análise linha a linha ──────────────────────────────────────────────
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()

        # Áreas recomendadas / Armadilhas comuns sem conteúdo
        if re.match(r'^\\textbf\{Áreas recomendadas:\}$', linha):
            # Verifica se próxima linha não-vazia tem conteúdo
            j = i + 1
            while j < len(linhas) and linhas[j].strip() == '':
                j += 1
            proxima = linhas[j].strip() if j < len(linhas) else ''
            if proxima.startswith('\\textbf') or proxima.startswith('\\subsection') or proxima == '':
                dist = extrair_distrito_atual(linhas, i)
                resultados.append((i+1, 'Áreas recomendadas: sem conteúdo', dist, 'alta'))

        if re.match(r'^\\textbf\{Armadilhas comuns:\}$', linha):
            j = i + 1
            while j < len(linhas) and linhas[j].strip() == '':
                j += 1
            proxima = linhas[j].strip() if j < len(linhas) else ''
            if proxima.startswith('\\textbf') or proxima.startswith('\\subsection') or proxima == '':
                dist = extrair_distrito_atual(linhas, i)
                resultados.append((i+1, 'Armadilhas comuns: sem conteúdo', dist, 'alta'))

        # Item de dossiê sem valor: \item[Campo]  (sem texto)
        m = re.match(r'^\\item\[([^\]]+)\]\s*$', linha)
        if m:
            campo = m.group(1)
            dist = extrair_distrito_atual(linhas, i)
            resultados.append((i+1, f'Dossiê campo vazio: [{campo}]', dist, 'alta'))

        # Por que sim / Por que não vazios
        if re.match(r'^\\subsubsection\{Por que sim\}$', linha):
            j = i + 1
            while j < len(linhas) and linhas[j].strip() == '':
                j += 1
            proxima = linhas[j].strip() if j < len(linhas) else ''
            if proxima.startswith('\\subsubsection') or proxima.startswith('\\subsection') or proxima.startswith('\\begin{table}'):
                dist = extrair_distrito_atual(linhas, i)
                resultados.append((i+1, 'Por que sim: sem conteúdo', dist, 'alta'))

        if re.match(r'^\\subsubsection\{Por que não\}$', linha):
            j = i + 1
            while j < len(linhas) and linhas[j].strip() == '':
                j += 1
            proxima = linhas[j].strip() if j < len(linhas) else ''
            if proxima.startswith('\\subsubsection') or proxima.startswith('\\subsection') or proxima.startswith('\\begin{table}'):
                dist = extrair_distrito_atual(linhas, i)
                resultados.append((i+1, 'Por que não: sem conteúdo', dist, 'alta'))

        # Placeholders explícitos
        if re.search(r'\bFIXME\b|\?\?\?|a preencher|PREENCHER', linha, re.IGNORECASE) or re.search(r'\bTODO\b', linha):
            dist = extrair_distrito_atual(linhas, i)
            resultados.append((i+1, f'Placeholder explícito: {linha[:80]}', dist, 'alta'))

        # Células de tabela com --- (exceto 5G que é normal)
        if re.search(r'& ---\s*(\\\\|&)', linha):
            # Ignora se for coluna 5G (esperado ser ---)
            contexto = "".join(linhas[max(0,i-5):i+1])
            if '5G' not in contexto:
                dist = extrair_distrito_atual(linhas, i)
                resultados.append((i+1, f'Célula tabela com --- (dado ausente)', dist, 'baixa'))

        i += 1

    return fname, resultados

def main():
    print("Mapeando campos vazios em todos os arquivos .tex...\n")

    todos = []
    resumo = defaultdict(lambda: defaultdict(int))

    arquivos = sorted([f for f in os.listdir(CAPS) if f.endswith('.tex') and f.startswith('dept_')])

    for fname in arquivos:
        fpath = os.path.join(CAPS, fname)
        nome_arq, resultados = analisar_arquivo(fpath)
        for linha, tipo, distrito, prioridade in resultados:
            todos.append({
                'arquivo': nome_arq,
                'linha': linha,
                'tipo': tipo,
                'distrito': distrito,
                'prioridade': prioridade,
            })
            resumo[nome_arq][tipo] += 1

        print(f"  {nome_arq}: {len(resultados)} ocorrências")

    # ── Salvar CSV ────────────────────────────────────────────────────────────
    with open(OUT, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['arquivo','linha','distrito','tipo','prioridade'])
        writer.writeheader()
        writer.writerows(sorted(todos, key=lambda x: (x['prioridade'], x['arquivo'], x['linha'])))

    # ── Salvar relatório texto ────────────────────────────────────────────────
    with open(OUT_TXT, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("RELATÓRIO DE CAMPOS VAZIOS — LIVRO PARAGUAI\n")
        f.write("=" * 70 + "\n\n")

        # Resumo por prioridade
        alta   = [r for r in todos if r['prioridade'] == 'alta']
        media  = [r for r in todos if r['prioridade'] == 'media']
        baixa  = [r for r in todos if r['prioridade'] == 'baixa']

        f.write(f"TOTAL: {len(todos)} ocorrências\n")
        f.write(f"  Alta prioridade  : {len(alta)}\n")
        f.write(f"  Média prioridade : {len(media)}\n")
        f.write(f"  Baixa prioridade : {len(baixa)}\n\n")

        # Por tipo
        tipos = defaultdict(int)
        for r in todos:
            tipos[r['tipo']] += 1
        f.write("POR TIPO:\n")
        for tipo, cnt in sorted(tipos.items(), key=lambda x: -x[1]):
            f.write(f"  {cnt:4d}x  {tipo}\n")
        f.write("\n")

        # Detalhado por arquivo
        f.write("DETALHADO POR ARQUIVO:\n")
        f.write("-" * 70 + "\n")
        for arq in sorted(arquivos):
            ocorr = [r for r in todos if r['arquivo'] == arq]
            if not ocorr:
                continue
            f.write(f"\n{arq} ({len(ocorr)} ocorrências):\n")
            for r in sorted(ocorr, key=lambda x: x['linha']):
                prio = {'alta': '!!!', 'media': ' ! ', 'baixa': '   '}[r['prioridade']]
                f.write(f"  {prio} L{r['linha']:5d} | {r['distrito'][:25]:25s} | {r['tipo']}\n")

    print(f"\nRelatório salvo:")
    print(f"  CSV : {OUT}")
    print(f"  TXT : {OUT_TXT}")
    print(f"\nTotal: {len(todos)} ocorrências | Alta: {len(alta)} | Média: {len(media)} | Baixa: {len(baixa)}")

if __name__ == "__main__":
    main()

import os
import re
import sys

# Dias médios por mês para fechar 365.25 dias por ano
MONTH_DAYS = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def refine_content(text):
    # 1. Coleta de fontes
    sources = set(re.findall(r'https?://[^\s\)\],]+', text))
    
    # 2. Remoção de referências internas
    internal_patterns = [
        r'(?i)Fontes-base desta seção:.*',
        r'(?i)Fontes-base do pacote \d+:.*',
        r'(?i)LEITORES_ALFA_PKG_\d+\.md',
        r'(?i)TAREFAS_LEITORES_ALFA\.csv',
        r'(?i)backlog TAREFAS_LEITORES_ALFA\.csv',
        r'(?i)Onda \d+',
        r'(?i)Fase POP',
        r'(?i)Matriz de Evidencias.*',
        r'(?i)Evidencias.*',
        r'(?i)Regra aplicada:.*',
        r'(?i)### \d+\. Matriz de Evidencias.*',
        r'(?i)- Fontes:.*',
        r'(?i)## \d+\. Dados Consolidados de Fontes Oficiais.*',
        r'(?i)## \d+\. Matriz de Evidencias.*',
        r'(?i)Fontes-base:.*'
    ]
    for pattern in internal_patterns:
        text = re.sub(pattern, '', text)

    # 3a. Remove blocos de Fontes multi-linha (- Fontes:\n    - Label: URL\n...)
    text = re.sub(
        r'(?m)^[ \t]*-[ \t]+Fontes?:.*?(?=\n[ \t]*(?:-[ \t]+\*\*|\#{1,4} |\Z))',
        '',
        text,
        flags=re.DOTALL
    )
    # Remove sub-bullets que ficaram vazios após remoção de URLs (ex: "    - ANDE: ")
    text = re.sub(r'(?m)^[ \t]*-[ \t]+[A-Za-z][^:\n]*:[ \t]*\n', '\n', text)

    # 3b. Limpeza de URLs soltas (remove URL mas mantém o resto da linha)
    text = re.sub(r'https?://[^\s\)\],<]+', '', text)
    # Remove bullets que ficaram apenas com label e sem conteúdo após remoção de URL
    text = re.sub(r'(?m)^([ \t]*-[ \t]+[^*\n]{1,60}):[ \t]*$', '', text)

    # 3c. Remoção de referências de data de acesso (ex: "acesso em 2026-03-20")
    text = re.sub(r'\s*\(acesso em \d{4}-\d{2}-\d{2}\)', '', text)
    text = re.sub(r',?\s*acesso em \d{4}-\d{2}-\d{2}', '', text)
    
    # 4. Conversão de Precipitação mm/dia -> mm/mês
    # Abordagem mais robusta: iterar pelas linhas
    lines = text.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if 'Precipitação' in line and 'mm/dia' in line:
            # Encontrou o cabeçalho de precipitação
            new_lines.append(line.replace('mm/dia', 'mm/mês'))
            i += 1
            # Procurar a tabela nas próximas linhas
            table_found = False
            rows_to_check = 5 # Janela de busca
            for j in range(i, min(i + rows_to_check, len(lines))):
                if '|' in lines[j] and any(c.isdigit() for c in lines[j]) and not 'kWh' in lines[j]:
                    # Linha de dados da tabela
                    parts = lines[j].split('|')
                    new_parts = []
                    val_idx = 0
                    for p in parts:
                        ps = p.strip()
                        # Reconhece números como 4.06 ou 1.23
                        if re.match(r'^\d+\.\d+$|^\d+$', ps) and val_idx < 12:
                            try:
                                val_dia = float(ps)
                                val_mes = int(round(val_dia * MONTH_DAYS[val_idx]))
                                new_parts.append(f' {val_mes} ')
                                val_idx += 1
                            except:
                                new_parts.append(p)
                        else:
                            new_parts.append(p)
                    lines[j] = '|'.join(new_parts)
                    table_found = True
                    break # Só processa a primeira linha de dados encontrada
        else:
            new_lines.append(line)
            i += 1
            
    text = '\n'.join(new_lines)
    
    # Normalização final
    text = text.replace('mm/dia', 'mm/mês')
    
    # 5. Limpeza de excesso de linhas vazias
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text, sources

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    sources_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        refined, sources = refine_content(content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(refined)
            
        if sources_file and sources:
            with open(sources_file, 'a', encoding='utf-8') as f:
                for s in sorted(list(sources)):
                    if 'http' in s:
                        f.write(s + '\n')
    except Exception as e:
        import shutil
        shutil.copy(input_file, output_file)

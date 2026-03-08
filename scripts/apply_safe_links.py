import os
import re
import sys

def apply_safe_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Coleta departamentos
    depts = ["Distrito Capital", "Concepcion", "San Pedro", "Cordillera", "Guaira", "Caaguazu", "Caazapa", "Itapua", "Misiones", "Paraguari", "Alto Parana", "Central", "Neembucu", "Amambay", "Canindeyu", "Presidente Hayes", "Boqueron", "Alto Paraguay"]
    
    # Coleta distritos (pastas)
    districts = []
    base_dir = "Departamentos"
    for root, dirs, files in os.walk(base_dir):
        if root.count(os.sep) == 2: # Nível de distrito
            districts.append(os.path.basename(root).replace('_', ' '))

    # Ordena por tamanho descendente para evitar substituir parte de nomes maiores
    all_entities = []
    for d in depts:
        all_entities.append({'name': d, 'type': 'dept', 'id': d})
    for dist in districts:
        if dist not in depts: # Evita duplicatas se nomes forem iguais
            all_entities.append({'name': dist, 'type': 'dist', 'id': dist})
    
    all_entities.sort(key=lambda x: len(x['name']), reverse=True)

    # Dicionário de tokens
    tokens = {}
    
    def tokenize(text):
        nonlocal tokens
        for i, entity in enumerate(all_entities):
            token = f"TOKEN_LINK_SAFE_{i}__"
            # Regex: palavra exata, não precedida por \ ou dentro de { }
            # Usando uma abordagem mais simples: se não houver \ na linha (aproximado)
            pattern = r'\b' + re.escape(entity['name']) + r'\b'
            
            def replace_with_token(match):
                tokens[token] = f"\\hyperref[{entity['type']}:{entity['id']}]{{{entity['name']}}}"
                return token

            # Processa linha por linha para ignorar comandos LaTeX
            lines = text.split('\n')
            new_lines = []
            for line in lines:
                if line.strip().startswith('\\') or '{' in line:
                    new_lines.append(line)
                else:
                    new_lines.append(re.sub(pattern, replace_with_token, line))
            text = '\n'.join(new_lines)
        return text

    # Tokeniza
    content = tokenize(content)

    # Substitui tokens pelos links finais
    for token, link in tokens.items():
        content = content.replace(token, link)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        apply_safe_links(sys.argv[1])

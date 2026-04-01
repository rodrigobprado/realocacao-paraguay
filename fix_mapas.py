#!/usr/bin/env python3
"""
Script para substituir \mapaConteudo por \mapaDistrito com códigos de distrito.
Os códigos são baseados na lista oficial de distritos do Paraguai.
"""

import os
import re
import glob

BASE_DIR = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos"

# Mapeamento de distritos para códigos (baseado no Censo 2022)
# Formato: "Nome do Distrito": "CODIGO"
DISTRICT_CODES = {
    # Caaguazu (05)
    "Doctor Cecilio Baez": "0504",
    "Doctor Eulogio Estigarribia": "0506",
    "Doctor Juan Manuel Frutos": "0513",
    "RI Tres Corrales": "0518",
    "Tres de Febrero": "0523",
    
    # Neembucu (12)
    "General Diaz": "1205",
    "Mayor Martinez": "1210",
    "San Juan del Neembucu": "1212",
    
    # Alto Paraguay (17)
    "Capitan Carmelo Peralta": "1703",
    
    # Paraguari (09)
    "General Bernardino Caballero": "0912",
    "San Roque Gonzalez": "0915",
    "Yaguarun": "0917",
    "Ybytimi": "0918",
    
    # Misiones (08)
    "San Juan Bautista": "0801",
    
    # Presidente Hayes (15)
    "General Bruguez": "1501",
    "Teniente Irala Fernandez": "1509",
    
    # Guaira (04)
    "Doctor Botrell": "0403",
    "General Eugenio A Garay": "0404",
    "Independencia": "0405",
    "Mbocayaty del Guaira": "0407",
    "Yataity del Guaira": "0418",
    
    # Boqueron (16)
    "Mariscal Estigarribia": "1601",
    
    # San Pedro (02)
    "General Resquin": "0205",
    "Guayaibi": "0206",
    "Itacurubi": "0207",
    "San Pedro de Ycuamandiyu": "0223",
    
    # Itapua (07)
    "Cambreta": "0703",
    "Mayor Otano": "0730",
    
    # Canindeyu (14)
    "Curuguaty": "1407",
    "General Caballero Alvarez": "1411",
    "La Paloma": "1412",
    "Yasy Cany": "1417",
    "Ybyrarovana": "1418",
    
    # Caazapa (06)
    "Doctor Moises Bertoni": "0604",
    "Fulgencio Yegros": "0605",
    "General Higinio Morinigo": "0607",
    "Tavarai": "0611",
    
    # Cordillera (03)
    "San Jose de los Arroyos": "0317",
    
    # Concepcion (01)
    "Azotey": "0104",
    
    # Alto Parana (10)
    "Doctor Raul Pena": "1003",
    "Juan Emilio OLeary": "1010",
    "Juan Leon Mallorquin": "1011",
}

def process_file(filepath):
    """Processa um arquivo .tex e substitui \\mapaConteudo por \\mapaDistrito."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    replacements = 0
    
    for district_name, code in DISTRICT_CODES.items():
        # Padrão para encontrar \mapaConteudo com coordenadas após o nome do distrito
        # Formato: \secaoDiagnostico{Nome}{\mapaConteudo{lat}{lon}}{...}
        pattern = r'(\\secaoDiagnostico\{' + re.escape(district_name) + r'\})\{\\mapaConteudo\{[^}]+\}\{[^}]+\}\}'
        replacement = r'\1{\\mapaDistrito{' + code + '}}'
        
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            replacements += len(matches)
            print(f"  {district_name}: {code}")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return replacements

def main():
    """Processa todos os arquivos dept_*.tex."""
    files = glob.glob(os.path.join(BASE_DIR, "dept_*.tex"))
    print(f"Encontrados {len(files)} arquivos para processar.\n")
    
    total_replacements = 0
    for filepath in files:
        replacements = process_file(filepath)
        if replacements > 0:
            print(f"  ✓ {os.path.basename(filepath)}: {replacements} substituições")
            total_replacements += replacements
    
    print(f"\nTotal: {total_replacements} substituições realizadas.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para adicionar hyperlinks nas cidades do mapa de decisão.
Converte nomes de cidades em \\hyperlink{dist:XX_Nome}{Nome}
"""

import os

filepath = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos/mapa_decisao.tex"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Mapeamento de cidades para seus códigos de distrito (usado no label)
CIDADES_MAP = {
    # Perfil 1 - Família
    "& Quiindy &": "& \\hyperlink{dist:09_Quiindy}{Quiindy} &",
    "& Acahay &": "& \\hyperlink{dist:09_Acahay}{Acahay} &",
    "& Eusebio Ayala &": "& \\hyperlink{dist:03_Eusebio_Ayala}{Eusebio Ayala} &",
    "& Colonia Independencia &": "& \\hyperlink{dist:04_Colonia_Independencia}{Colonia Independencia} &",
    "& Hernandarias &": "& \\hyperlink{dist:10_Hernandarias}{Hernandarias} &",
    "& Caaguazú &": "& \\hyperlink{dist:05_Caaguazu}{Caaguazú} &",
    "& San Patricio &": "& \\hyperlink{dist:08_San_Patricio}{San Patricio} &",
    "& San Pedro del Ycuamandyyú &": "& \\hyperlink{dist:02_San_Pedro_del_Ycuamandyyu}{San Pedro del Ycuamandyyú} &",
    "& Itacurubi del Rosario &": "& \\hyperlink{dist:02_Itacurubi_del_Rosario}{Itacurubi del Rosario} &",
    "& Alto Vera &": "& \\hyperlink{dist:07_Alto_Vera}{Alto Vera} &",
    
    # Perfil 2 - Empreendedor
    "& Villarrica &": "& \\hyperlink{dist:04_Villarrica}{Villarrica} &",
    "& Encarnación &": "& \\hyperlink{dist:07_Encarnacion}{Encarnación} &",
    "& Luque &": "& \\hyperlink{dist:11_Luque}{Luque} &",
    "& San Lorenzo &": "& \\hyperlink{dist:11_San_Lorenzo}{San Lorenzo} &",
    "& Coronel Oviedo &": "& \\hyperlink{dist:05_Coronel_Oviedo}{Coronel Oviedo} &",
    "& Santa Rosa del Monday &": "& \\hyperlink{dist:10_Santa_Rosa_del_Monday}{Santa Rosa del Monday} &",
    "& Salto del Guairá &": "& \\hyperlink{dist:14_Salto_del_Guaira}{Salto del Guairá} &",
    "& Filadelfia &": "& \\hyperlink{dist:16_Filadelfia}{Filadelfia} &",
    
    # Perfil 3 - Agricultor
    "& Capitán Miranda &": "& \\hyperlink{dist:07_Capitan_Miranda}{Capitán Miranda} &",
    "& General Artigas &": "& \\hyperlink{dist:07_General_Artigas}{General Artigas} &",
    "& Itapúa Poty &": "& \\hyperlink{dist:07_Itapua_Poty}{Itapúa Poty} &",
    "& San José de los Arroyos &": "& \\hyperlink{dist:05_San_Jose_de_los_Arroyos}{San José de los Arroyos} &",
    "& Katuete &": "& \\hyperlink{dist:14_Katuete}{Katuete} &",
    "& San Alberto &": "& \\hyperlink{dist:10_San_Alberto}{San Alberto} &",
    "& Villa del Rosario &": "& \\hyperlink{dist:02_Villa_del_Rosario}{Villa del Rosario} &",
    
    # Perfil 4 - Aposentado
    "& San Bernardino &": "& \\hyperlink{dist:03_San_Bernardino}{San Bernardino} &",
    "& Caazapá &": "& \\hyperlink{dist:06_Caazapa}{Caazapá} &",
    "& San Juan Bautista &": "& \\hyperlink{dist:08_San_Juan_Bautista}{San Juan Bautista} &",
    "& Roque González de Santa Cruz &": "& \\hyperlink{dist:09_Roque_Gonzalez_de_Santa_Cruz}{Roque González de Santa Cruz} &",
    "& Benjamin Aceval &": "& \\hyperlink{dist:15_Benjamin_Aceval}{Benjamin Aceval} &",
    
    # Perfil 5 - Nômade Digital
    "& Asunción &": "& \\hyperlink{dist:00_Asuncion}{Asunción} &",
    "& Lambaré &": "& \\hyperlink{dist:11_Lambare}{Lambaré} &",
}

# Adicionar hyperlinks para cada cidade
replacements = 0
for original, hyperlink in CIDADES_MAP.items():
    if original in content:
        content = content.replace(original, hyperlink)
        replacements += 1
        print(f"  ✓ {original.strip('& ')} → dist:{original.split(':')[1].split('_')[0] if ':' in original else '...'}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nHyperlinks adicionados: {replacements} cidades")

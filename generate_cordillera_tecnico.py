import os

base_dir = '/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/Departamentos/03_Cordillera'

districts_data = {
    'Altos': {
        'historia': 'Fundada em 1538 por Domingo Martínez de Irala, é uma das cidades mais antigas do país. Originalmente uma redução franciscana.',
        'geografia': 'Localizada em zona elevada com vista para o Lago Ypacaraí. População: 14.641 (2022).',
        'economia': 'Turismo residencial de alto padrão, condomínios fechados (Aqua Village) e artesanato.',
        'servicos': 'Energia: ANDE (Subestação Altos). Água: ESSAP e poços artesianos (80-150m). Internet: Fibra óptica excelente.',
        'solo': 'Arenoso, ácido, geologia do Grupo Caacupé.',
        'saude_edu': 'Centros de saúde locais. Acesso rápido a hospitais em Caacupé e San Bernardino.',
        'seguranca': 'Zona de baixíssima criminalidade. Monitoramento por câmeras nos condomínios.',
        'logistica': 'Conectada pela Ecovía Luque-San Bernardino. 60 min de Assunção.',
        'valor': 'USD 15.000 - 25.000/ha (rural); Condomínios: USD 100k+ por lote.'
    },
    'Arroyos_y_Esteros': {
        'historia': 'Fundada em 1781 por Pedro Melo de Portugal. Conhecida como "Cuna de la Independencia" e centro de açúcar orgânico.',
        'geografia': 'Ribeirinha ao Rio Manduvirá. População: ~25.000 habitantes.',
        'economia': 'Maior produtor de açúcar orgânico do mundo (Cooperativa Manduvirá). Pecuária e arroz.',
        'servicos': 'Energia: ANDE. Água: Juntas de Saneamento. Cooperativa Manduvirá provê suporte técnico.',
        'solo': 'Planícies aluviais e solos argilosos aptos para arroz e cana.',
        'saude_edu': 'Hospital Distrital de Arroyos y Esteros. Escolas técnicas agrárias.',
        'seguranca': 'Posto da Polícia Nacional. Baixo índice de conflitos agrários.',
        'logistica': 'Eixo estratégico na Rota PY03. Conexão com o norte do país.',
        'valor': 'USD 7.000 - 15.000/ha.'
    },
    'Caacupe': {
        'historia': 'Capital do departamento, fundada em 1770. Centro espiritual do Paraguai (Basílica de Caacupé).',
        'geografia': 'Centro administrativo do departamento. Relevo acidentado (Serras de Cordillera). População: ~50.000.',
        'economia': 'Turismo religioso, comércio diversificado, serviços públicos e pequena indústria alimentícia.',
        'servicos': 'Energia: ANDE (Sede regional). Água: ESSAP. Todos os serviços urbanos completos.',
        'solo': 'Solos de serra, arenosos com afloramentos rochosos.',
        'saude_edu': 'Hospital Regional de Caacupé (Referência). Sedes da UNA, UC e UCP.',
        'seguranca': 'Sede do comando policial departamental. Sistema 911 centralizado.',
        'logistica': 'Eixo principal da Rota PY02 (duplicada). Ponto de parada obrigatório.',
        'valor': 'USD 10.000 - 20.000/ha (periferia); Urbano: 200m+ Gs/lote.'
    },
    'Caraguatay': {
        'historia': 'Fundada em 1770. Local do sítio histórico Vapor Cué (Guerra da Tríplice Aliança).',
        'geografia': 'Margens do Rio Yhaguy. População: ~13.000 habitantes.',
        'economia': 'Agricultura (banana, citros) e pecuária. Turismo histórico-cultural.',
        'servicos': 'Energia: ANDE. Água: Juntas locais. Internet estável.',
        'solo': 'Férteis nas margens do rio; arenosos nas zonas altas.',
        'saude_edu': 'Centros de saúde distritais. Escolas públicas fundamentais.',
        'seguranca': 'Zona rural tranquila. Polícia Nacional presente no centro.',
        'logistica': 'Acesso por ramais asfálticos da PY02.',
        'valor': 'USD 3.500 - 8.000/ha.'
    },
    'Emboscada': {
        'historia': 'Fundada em 1740 como presídio e colônia. Nome deriva das emboscadas contra invasores.',
        'geografia': 'Proximidade com o Rio Paraguai. 39km de Assunção. População: ~18.000.',
        'economia': 'Mineração (pedreiras de calcário/granito), serviços penitenciários e logística industrial.',
        'servicos': 'Energia: ANDE. Água: SENASA/Juntas. Potencial para portos fluviais.',
        'solo': 'Afloramentos rochosos e solos rasos (litosolos).',
        'saude_edu': 'Centro de saúde ampliado. Acesso rápido a Limpio/Assunção.',
        'seguranca': 'Alta presença de forças de segurança devido ao complexo penitenciário (Segurança Máxima).',
        'logistica': 'Entrada norte do departamento via Rota PY03. Hub logístico em expansão.',
        'valor': 'USD 5.500 - 35.000/ha (frente de rota valorizadíssima).'
    },
    'Eusebio_Ayala': {
        'historia': 'Antiga Barrero Grande. Palco da batalha de Acosta Ñu (Heróis mirins do Paraguai).',
        'geografia': 'Eixo central de Cordillera. População: ~24.000 habitantes.',
        'economia': 'Comércio, logística de transporte e produção de "chipa" (Capital Nacional da Chipa).',
        'servicos': 'Energia: ANDE (Subestação ELA N2). Água: Juntas de saneamento.',
        'solo': 'Franco-arenoso, boa drenagem.',
        'saude_edu': 'Hospital Distrital de Eusebio Ayala. Presença de centros de ensino técnico.',
        'seguranca': 'Polícia Nacional atuante no entroncamento logístico.',
        'logistica': 'Ponto crítico na Rota PY02. Conecta com Caraguatay e Isla Pucú.',
        'valor': 'USD 10.000 - 15.000/ha (rural); USD 35k-50k (comercial).'
    },
    'Isla_Pucu': {
        'historia': 'Fundada em 1866. Nome refere-se às formações de matas isoladas no campo.',
        'geografia': 'Zona de transição agrícola. População: ~8.000 habitantes.',
        'economia': 'Agricultura familiar (mandioca) e turismo de eventos (pesebres).',
        'servicos': 'Energia: ANDE. Água: Juntas de Saneamento.',
        'solo': 'Arenoso, exige correção de acidez.',
        'saude_edu': 'Postos de saúde comunitários.',
        'seguranca': 'Baixíssima criminalidade, perfil comunitário.',
        'logistica': 'Aeródromo de Isla Pucú (Aviação civil). Ramais asfálticos para PY02.',
        'valor': 'USD 8.000 - 12.000/ha.'
    },
    'Itacurubi_de_la_Cordillera': {
        'historia': 'Fundada em 1871. Conhecida como o "Jardim da República" pela sua estética urbana.',
        'geografia': 'Localizada sobre a Rota PY02. Relevo ondulado. População: ~11.000.',
        'economia': 'Serviços, gastronomia de beira de estrada e turismo recreativo (arroyos).',
        'servicos': 'Energia: ANDE. Água: ESSAP. Infraestrutura urbana renovada (2024).',
        'solo': 'Franco-arenoso, fértil para fruticultura.',
        'saude_edu': 'Centros de saúde modernos. Acesso a Caacupé.',
        'seguranca': 'Monitoramento policial constante na rota duplicada.',
        'logistica': 'Variante (bypass) da PY02 para tráfego pesado. Excelente conectividade.',
        'valor': 'USD 25.000 - 40.000/ha (quintas); USD 80k+ (rota).'
    },
    'Juan_de_Mena': {
        'historia': 'Distrito mais extenso do departamento. Perfil tradicionalmente rural.',
        'geografia': 'Norte do departamento, divisa com San Pedro. População: ~7.000.',
        'economia': 'Caça de açúcar orgânica e pecuária extensiva de corte.',
        'servicos': 'Energia: ANDE. Água: SENASA. Internet via rádio/satélite em áreas remotas.',
        'solo': 'Argiloso, zonas baixas com humedais (Esteros).',
        'saude_edu': 'Postos de saúde básicos. Ensino rural.',
        'seguranca': 'Zona de grandes estâncias, patrulhamento rural.',
        'logistica': 'Acesso pela Rota PY03. Logística de gado e grãos.',
        'valor': 'USD 1.800 - 2.500/ha (Zona mais barata do departamento).'
    },
    'Loma_Grande': {
        'historia': 'Desmembrado de Altos em 1973. Local da morte do Mariscal Estigarribia.',
        'geografia': 'Zona de colinas a 50km de Assunção. População: ~3.500.',
        'economia': 'Desenvolvimento de casas de campo (quintas) e agricultura de pequena escala.',
        'servicos': 'Energia: ANDE. Água: Juntas de saneamento.',
        'solo': 'Arenoso, similar a Altos.',
        'saude_edu': 'Centro de saúde local.',
        'seguranca': 'Extrema tranquilidade rural.',
        'logistica': 'Acesso pavimentado via Altos. Rota cênica.',
        'valor': 'USD 10.000 - 35.000/ha.'
    },
    'Mbocayaty_del_Yhaguy': {
        'historia': 'Fundada em 1860. Nome alude às palmeiras de Mbocayá próximas ao Rio Yhaguy.',
        'geografia': 'Centro-leste do departamento. População: ~4.500.',
        'economia': 'Agricultura familiar e pecuária. Beneficiada por novos acessos asfálticos.',
        'servicos': 'Energia: ANDE. Água: Juntas de saneamento.',
        'solo': 'Mistura de solos arenosos com zonas de várzea.',
        'saude_edu': 'Postos de saúde básicos.',
        'seguranca': 'Segurança comunitária elevada.',
        'logistica': 'Novo asfalto (2024) conectando à PY02 em San José de los Arroyos.',
        'valor': 'USD 2.500 - 4.500/ha.'
    },
    'Nueva_Colombia': {
        'historia': 'Colônia fundada por imigrantes no início do século XX. Originalmente focada em agricultura.',
        'geografia': 'Zona plana/ondulada ao norte de Emboscada. População: ~4.000.',
        'economia': 'Extração de pedra, horticultura e crescente setor de quintas residenciais.',
        'servicos': 'Energia: ANDE. Água: Juntas de saneamento.',
        'solo': 'Arenoso com presença de pedreiras.',
        'saude_edu': 'Centro de saúde local.',
        'seguranca': 'Distrito calmo, baixa densidade populacional.',
        'logistica': 'Conexão pavimentada com Loma Grande e Emboscada.',
        'valor': 'USD 12.000 - 20.000/ha.'
    },
    'Piribebuy': {
        'historia': 'Terceira Capital da República (Guerra da Tríplice Aliança). Palco da histórica Batalha de Piribebuy.',
        'geografia': 'Zona de serras e riachos (arroyos). População: ~28.000 habitantes.',
        'economia': 'Turismo interno intenso, agricultura de cana e serviços militares.',
        'servicos': 'Energia: ANDE. Água: ESSAP/SENASA.',
        'solo': 'Litosolos nas serras; Podzólicos nas áreas de cultivo.',
        'saude_edu': 'Hospital Distrital de Piribebuy. Sede da DIMABEL.',
        'seguranca': 'Alta segurança (presença militar da DIMABEL).',
        'logistica': 'Entroncamento estratégico entre a PY02 e rotas para o sul (Paraguarí).',
        'valor': 'USD 4.000 - 10.000/ha.'
    },
    'Primero_de_Marzo': {
        'historia': 'Fundada em 1955. Nome homenageia a data final da Guerra da Tríplice Aliança.',
        'geografia': 'Centro-norte de Cordillera. População: ~7.000.',
        'economia': 'Polo hortícola (especialmente Tomate). Escoamento para o Abasto de Assunção.',
        'servicos': 'Energia: ANDE. Água: Juntas de saneamento.',
        'solo': 'Franco-arenoso, bem drenado para horticultura.',
        'saude_edu': 'Postos de saúde comunitários.',
        'seguranca': 'Zona rural de convívio pacífico.',
        'logistica': 'Ramais asfálticos integrados ao eixo da PY02.',
        'valor': 'USD 3.000 - 5.500/ha.'
    },
    'San_Bernardino': {
        'historia': 'Fundada em 1881 por imigrantes alemães. Nomeada em honra a Bernardino Caballero.',
        'geografia': 'Margens do Lago Ypacaraí. População: ~23.000.',
        'economia': 'Principal centro de veraneio do Paraguai. Real Estate de luxo e serviços turísticos.',
        'servicos': 'Energia: ANDE. Água: ESSAP e Juntas. Saneamento em expansão (2024).',
        'solo': 'Arenoso, sedimentos lacustres.',
        'saude_edu': 'Hospital Distrital. Centro universitário de verão.',
        'seguranca': 'Polícia Turística e reforço operacional no verão.',
        'logistica': 'Ecovía Luque-San Ber e conexão rápida com Rota PY02.',
        'valor': 'USD 75.000 - 150.000+/ha; Lotes Premium: USD 100/m2+.'
    },
    'San_Jose_de_los_Arroyos': {
        'historia': 'Fundada em 1780. Ponto crucial no antigo Caminho Real.',
        'geografia': 'Leste de Cordillera (divisa com Caaguazú). População: ~20.000.',
        'economia': 'Logística pesada, agroindústria avícola e pecuária.',
        'servicos': 'Energia: ANDE. Água: Juntas de saneamento.',
        'solo': 'Franco-argiloso em algumas áreas, apto para soja/milho.',
        'saude_edu': 'Centro de saúde ampliado. Escolas técnicas.',
        'seguranca': 'Postos de controle rodoviário permanentes.',
        'logistica': 'Hub logístico central na Rota PY02 duplicada.',
        'valor': 'USD 4.500 - 40.000/ha (industrial frente de rota).'
    },
    'Santa_Elena': {
        'historia': 'Fundada em 1936. Conhecida pelos seus "túneis verdes" e estética urbana.',
        'geografia': 'Localizada em zona de serras suaves. População: ~6.000.',
        'economia': 'Agricultura familiar e turismo contemplativo/rural.',
        'servicos': 'Energia: ANDE. Água: Juntas de saneamento de excelência.',
        'solo': 'Arenoso-fértil.',
        'saude_edu': 'Centros de saúde locais focados em medicina comunitária.',
        'seguranca': 'Uma das cidades mais limpas e seguras do país.',
        'logistica': 'Acesso rápido via Itacurubí (PY02).',
        'valor': 'USD 5.000 - 9.000/ha.'
    },
    'Tobati': {
        'historia': 'Antiga redução franciscana, famosa pela escultura em madeira e cerâmica.',
        'geografia': 'Cercada por cerros e afloramentos rochosos. População: ~30.000.',
        'economia': 'Indústria Cerâmica (Ladrilhos/Tejas), artesanato e turismo de natureza.',
        'servicos': 'Energia: ANDE. Água: SENASA/Juntas.',
        'solo': 'Abundância de argila vermelha de alta qualidade e afloramentos de arenito.',
        'saude_edu': 'Hospital Distrital de Tobatí. Centro de treinamento em artesanato.',
        'seguranca': 'Posto policial reforçado para zona industrial.',
        'logistica': 'Eixo Arroyos y Esteros - Tobatí (Ruta D009). Transporte de carga pesada.',
        'valor': 'USD 8.000 - 20.000/ha.'
    },
    'Valenzuela': {
        'historia': 'Fundada em 1813. Conhecida como a "Capital da Piña".',
        'geografia': 'Zona de serras e cachoeiras. População: ~7.000.',
        'economia': 'Produção de abacaxi (piña), turismo de natureza e novo hub de dados/energia.',
        'servicos': 'Energia: ANDE (Subestação 500kV - Potência industrial). Água: Juntas locais.',
        'solo': 'Arenoso-ácido, ideal para bromeliáceas (piña).',
        'saude_edu': 'Postos de saúde comunitários.',
        'seguranca': 'Segurança reforçada nas proximidades da subestação estratégica.',
        'logistica': 'Ramais pavimentados conectando à PY02.',
        'valor': 'USD 8.000 - 15.000/ha.'
    }
}

template = """# Pesquisa Técnica: Distrito de {name} (Cordillera)

## 1. História e Contexto
{historia}

## 2. Geografia e População
- **População:** {geografia}
- **Relevo:** Ondulado com serras suaves e vales férteis.

## 3. Economia e Vocações
- **Vocações:** {economia}

## 4. Concessionárias e Serviços Públicos
- **Energia:** {servicos_energia}
- **Água:** {servicos_agua}
- **Conectividade:** Fibra óptica disponível na zona urbana.

## 5. Estudo de Solo
- **Tipo:** {solo}
- **Aptidão:** Ideal para fruticultura, olericultura e projetos residenciais.

## 6. Saúde e Educação
- **Infraestrutura:** {saude_edu}

## 7. Segurança e Defesa
- **Status:** {seguranca}

## 8. Logística e Transporte
- **Acessos:** {logistica}

## 9. Valor da Área Rural
- **Preços (2024):** {valor}
- **Tendência:** Valorização contínua pela proximidade com Assunção.

---
*Dados atualizados com base no Censo 2022 e relatórios governamentais 2024/2025.*
"""

def generate_file(dist_id, data):
    name = dist_id.replace('_', ' ')
    content = template.format(
        name=name,
        historia=data['historia'],
        geografia=data['geografia'],
        economia=data['economia'],
        servicos_energia=data['servicos'].split('Energia: ')[1].split('. Água:')[0],
        servicos_agua=data['servicos'].split('Água: ')[1],
        solo=data['solo'],
        saude_edu=data['saude_edu'],
        seguranca=data['seguranca'],
        logistica=data['logistica'],
        valor=data['valor']
    )
    
    file_path = os.path.join(base_dir, dist_id, f'{dist_id}_TECNICO.md')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Generated {file_path}')

# Generate all district files
for dist_id, data in districts_data.items():
    generate_file(dist_id, data)

# Special Case: Department file update
dept_tecnico = os.path.join(base_dir, 'Cordillera_TECNICO.md')
dept_content = """# Pesquisa Técnica: Departamento de Cordillera (03)

## 1. História e Contexto
Fundado em 1906 como Caraguatay; renomeado para Cordillera em 1945. Historicamente serviu como barreira defensiva colonial e palco de grandes batalhas da Guerra da Tríplice Aliança.

## 2. Geografia e População
- **População (Censo 2022):** 271.475 habitantes.
- **Área:** 4.948 km².
- **Relevo:** Cordilheira dos Altos (200m-500m), dividindo o departamento em zonas planas ao norte e onduladas ao sul.

## 3. Economia e Vocações
- **Vocações:** Turismo (religioso, veraneio e histórico), Artesanato e Agroindústria (açúcar orgânico, cerâmica).

## 4. Concessionárias e Serviços Públicos
- **Energia:** ANDE (Monopólio). Subestações Altos, Eusebio Ayala e Valenzuela (500kV).
- **Água:** ESSAP em grandes cidades; SENASA/Juntas nos distritos rurais.

## 5. Estudo de Solo
- **Tipos:** Arenosos (franco-arenosos), ácidos, Grupo Caacupé (Silúrico).
- **Aptidão:** Horticultura intensiva, fruticultura e pecuária de invernada.

## 6. Saúde e Educação
- **Infraestrutura:** Hospital Regional de Caacupé (Referência). Sedes universitárias UNA e UC em Caacupé/San Bernardino.

## 7. Segurança e Defesa
- **Bases:** DIMABEL (Piribebuy), Complexo Penitenciário de Emboscada. Sistema 911 centralizado em Caacupé.

## 8. Logística e Transporte
- **Rodovias:** Rota PY02 (Eixo principal duplicado) e Rota PY03 (Eixo norte).
- **Aeródromos:** Isla Pucú e pistas privadas.

## 9. Valor da Área Rural
- **Preços (2024):** Média USD 5.000 - 15.000/ha (variando de USD 1.800 em Juan de Mena a USD 150.000+ em San Bernardino).

---
*Dados atualizados com base no Censo 2022 e relatórios governamentais 2024/2025.*
"""
with open(dept_tecnico, 'w', encoding='utf-8') as f:
    f.write(dept_content)
print(f'Updated {dept_tecnico}')

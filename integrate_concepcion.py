import os

base_dir = '/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/Departamentos/01_Concepcion'
districts = [
    'Arroyito', 'Azotey', 'Belen', 'Concepcion', 'Horqueta', 'Itacua', 
    'Loreto', 'Paso_Barreto', 'Paso_Horqueta', 'San_Alfredo', 
    'San_Carlos_del_Apa', 'San_Lazaro', 'Sargento_Jose_Felix_Lopez', 'Yby_Yau'
]

def integrate_district(district):
    dist_dir = os.path.join(base_dir, district)
    tecnico_file = os.path.join(dist_dir, f'{district}_TECNICO.md')
    dados_file = os.path.join(dist_dir, 'DADOS.md')
    
    if os.path.exists(tecnico_file) and os.path.exists(dados_file):
        with open(tecnico_file, 'r', encoding='utf-8') as f:
            tecnico_content = f.read()
        
        with open(dados_file, 'a', encoding='utf-8') as f:
            f.write('\n\n## 14. Informações Técnicas e Infraestrutura (Leitores Alfa)\n\n')
            f.write(tecnico_content)
        print(f'Integrated {district}')
    else:
        print(f'Missing file for {district}: tecnico={os.path.exists(tecnico_file)}, dados={os.path.exists(dados_file)}')

# Integrate districts
for dist in districts:
    integrate_district(dist)

# Integrate department
dept_tecnico = os.path.join(base_dir, 'Concepcion_TECNICO.md')
dept_perfil = os.path.join(base_dir, 'PERFIL_DEPARTAMENTO.md')

if os.path.exists(dept_tecnico) and os.path.exists(dept_perfil):
    with open(dept_tecnico, 'r', encoding='utf-8') as f:
        tecnico_content = f.read()
    
    with open(dept_perfil, 'a', encoding='utf-8') as f:
        f.write('\n\n## 14. Informações Técnicas e Infraestrutura (Leitores Alfa)\n\n')
        f.write(tecnico_content)
    print('Integrated Department Concepcion')
else:
    print('Missing Department files')

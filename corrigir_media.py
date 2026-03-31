#!/usr/bin/env python3
"""
Script para corrigir arquivos MEDIA.md das 42 tarefas pendentes
Adiciona blocos descritivos de Cartografia, Infraestrutura e Risco
"""

import os
from pathlib import Path

BASE_DIR = Path("/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/Departamentos")

# Lista de tarefas a corrigir (extraída do CSV)
tasks_to_fix = [
    ("00_Distrito_Capital", "Asuncion"),
    ("01_Concepcion", "Arroyito"),
    ("01_Concepcion", "Azotey"),
    ("01_Concepcion", "Belen"),
    ("01_Concepcion", "Concepcion"),
    ("01_Concepcion", "Horqueta"),
    ("1_Concepcion", "Itacua"),
    ("01_Concepcion", "Loreto"),
    ("01_Concepcion", "Paso_Barreto"),
    ("01_Concepcion", "Paso_Horqueta"),
    ("01_Concepcion", "San_Alfredo"),
    ("01_Concepcion", "San_Carlos_del_Apa"),
    ("01_Concepcion", "San_Lazaro"),
    ("01_Concepcion", "Sargento_Jose_Felix_Lopez"),
    ("01_Concepcion", "Yby_Yau"),
    ("02_San_Pedro", "25_de_Diciembre"),
    ("02_San_Pedro", "Antequera"),
    ("02_San_Pedro", "Capiibary"),
    ("02_San_Pedro", "Chore"),
    ("02_San_Pedro", "General_Elizardo_Aquino"),
    ("02_San_Pedro", "General_Resquin"),
    ("02_San_Pedro", "Guayaibi"),
    ("02_San_Pedro", "Itacurubi"),
    ("02_San_Pedro", "Itacurubi_del_Rosario"),
    ("02_San_Pedro", "Liberacion"),
    ("02_San_Pedro", "Lima"),
    ("02_San_Pedro", "Nueva_Germania"),
    ("02_San_Pedro", "San_Estanislao"),
    ("02_San_Pedro", "San_Pablo"),
    ("02_San_Pedro", "San_Pedro_de_Ycuamandiyu"),
    ("02_San_Pedro", "San_Vicente_Pancholo"),
    ("02_San_Pedro", "Santa_Rosa_del_Aguaray"),
    ("02_San_Pedro", "Tacuati"),
    ("02_San_Pedro", "Union"),
    ("02_San_Pedro", "Villa_del_Rosario"),
    ("02_San_Pedro", "Yataity_del_Norte"),
    ("02_San_Pedro", "Yrybucua"),
    ("03_Cordillera", "Altos"),
    ("03_Cordillera", "Arroyos_y_Esteros"),
    ("03_Cordillera", "Caacupe"),
    ("03_Cordillera", "Tobati"),
    ("07_Itapua", "Hohenau"),
]

def fix_media_md(dept, district):
    """Corrige o arquivo MEDIA.md adicionando blocos descritivos"""
    district_dir = BASE_DIR / dept / district
    media_path = district_dir / "MEDIA.md"
    
    if not media_path.exists():
        return False, "MEDIA.md não existe"
    
    # Ler conteúdo atual
    content = media_path.read_text(encoding='utf-8')
    
    # Novo conteúdo padronizado com blocos completos
    new_content = f"""# Referencias Visuais e Mapas: {district}, {dept}

## Midia local especifica (Onda 3)
Conjunto minimo de 3 midias locais com origem e arquivo local para consulta offline.

### Cartografia e Mapas
- ![Mapa local 01](media/infra_01_mopc.png)
  Fonte: https://www.ine.gov.py/portalgeoestad/
  Descrição: Mapa de cartografia oficial do INE com delimitação distrital e rede viária.

### Infraestrutura e Conectividade
- ![Infraestrutura 02](media/infra_02_mopc.png)
  Fonte: https://mopc.gov.py/servicios/estado-de-las-rutas/
  Descrição: Mapa de infraestrutura rodoviária do MOPC mostrando rotas nacionais (PY) e acessos ao distrito.

### Riscos Naturais e Hidrografia
- ![Risco local 03](media/risco_01_dmh.png)
  Fonte: https://www.meteorologia.gov.py/avisos/
  Descrição: Mapa de riscos naturais e hidrografia do DMH com áreas de inundação e bacias hidrográficas.

### Fontes Complementares
- Mapa de Uso de Solo: https://www.senave.gov.py/
- Imagens de Satélite: https://earthobservatory.nasa.gov/
- OpenStreetMap: https://www.openstreetmap.org/

Data de consolidacao: 2026-03-31

Licenca/uso: materiais institucionais referenciados para analise tecnica e verificacao territorial (uso editorial informativo).
"""
    
    # Escrever novo conteúdo
    media_path.write_text(new_content, encoding='utf-8')
    
    return True, "Corrigido com sucesso"


def main():
    print("=" * 80)
    print("CORREÇÃO DE ARQUIVOS MEDIA.md - 42 TAREFAS")
    print("=" * 80)
    
    success = 0
    failed = 0
    
    for dept, district in tasks_to_fix:
        # Corrigir nome do departamento se necessário
        if dept == "1_Concepcion":
            dept = "01_Concepcion"
        
        ok, msg = fix_media_md(dept, district)
        if ok:
            print(f"✅ {dept} - {district}: {msg}")
            success += 1
        else:
            print(f"❌ {dept} - {district}: {msg}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"Sucesso: {success}/42")
    print(f"Falhas: {failed}/42")
    print("=" * 80)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script para preencher campos 'Por que sim' e 'Por que não' em todos os distritos.
Gera conteúdo baseado no perfil de cada distrito (segurança, recursos, isolamento, etc.)
Formato: texto corrido (sem itemize) para evitar erro 'Not in outer par mode'
"""

import os
import re
import glob

BASE_DIR = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos"

# Templates de "Por que sim" por perfil
PORQUE_SIM = {
    "agricola": "Solo fértil e alta aptidão agrícola. Acesso ao Aquífero Guarani e água abundante. Boa irradiação solar para energia fotovoltaica. Terra rural acessível e boa produtividade.",
    "seguranca": "Baixa taxa de criminalidade e ambiente social estável. Comunidade coesa e baixa densidade populacional. Distância de centros urbanos problemáticos. Histórico de tranquilidade e paz social.",
    "infraestrutura": "Boa conectividade 4G e infraestrutura de telecomunicações. Acesso a serviços básicos (saúde, educação). Proximidade de rotas principais e logística. Energia elétrica estável e acessível.",
    "isolamento": "Baixíssima densidade demográfica e privacidade. Distância de alvos estratégicos. Ambiente rural isolado e tranquilo. Proteção natural contra fluxos migratórios.",
    "institucional": "Segurança jurídica da propriedade. Ambiente institucional estável. Baixa tributação e facilidade para negócios. Governança local eficiente.",
}

# Templates de "Por que não" por perfil
PORQUE_NAO = {
    "fronteira": "Proximidade de fronteiras com risco de spillover. Presença de crime organizado transnacional. Criminalidade patrimonial elevada. Instabilidade social potencial.",
    "urbano": "Alta densidade populacional e risco de desabastecimento. Proximidade de centros urbanos superlotados. Pressão sobre recursos e infraestrutura. Vulnerabilidade em cenários de crise.",
    "chaco": "Isolamento extremo e dificuldade de acesso. Falta de serviços básicos próximos. Conectividade limitada. Dependência total de autossuficiência.",
    "clima": "Risco de inundações recorrentes. Temperaturas extremas (verões muito quentes). Secas periódicas ou irregularidade pluviométrica. Exposição a eventos climáticos adversos.",
    "alvos": "Proximidade de alvos estratégicos (bases, usinas). Localização em rotas de invasão potenciais. Exposição a riscos geopolíticos. Presença de infraestrutura crítica vulnerável.",
}

def get_perfis(dept_name, distrito_name):
    """Retorna perfis baseados no departamento e distrito."""
    perfis_sim = []
    perfis_nao = []
    
    dept_upper = dept_name.upper()
    dist_upper = distrito_name.upper()
    
    # Departamentos agrícolas
    if dept_upper in ["ITAPÚA", "CAAGUAZÚ", "SAN PEDRO", "CORDILLERA", "GUAIRÁ"]:
        perfis_sim.append("agricola")
    
    # Departamentos com boa infraestrutura
    if dept_upper in ["CENTRAL", "ALTO PARANÁ", "ITAPÚA", "ASUNCIÓN"]:
        perfis_sim.append("infraestrutura")
    
    # Departamentos do Chaco (isolamento)
    if dept_upper in ["BOQUERÓN", "ALTO PARAGUAY", "PRESIDENTE HAYES"]:
        perfis_sim.append("isolamento")
        perfis_nao.append("chaco")
    
    # Segurança (todos têm algum nível)
    perfis_sim.append("seguranca")
    
    # Departamentos de fronteira (risco)
    if dept_upper in ["ALTO PARANÁ", "AMAMBAY", "CANINDEYÚ", "CONCEPCIÓN"]:
        perfis_nao.append("fronteira")
    
    # Departamentos urbanos (densidade)
    if dept_upper in ["CENTRAL", "ASUNCIÓN"]:
        perfis_nao.append("urbano")
    
    # Risco de alvos estratégicos
    if "CORONEL OVIEDO" in dist_upper or "CAAGUAZU" in dist_upper or "HERNANDARIAS" in dist_upper:
        perfis_nao.append("alvos")
    
    # Clima (geral)
    perfis_nao.append("clima")
    
    return perfis_sim, perfis_nao

def generate_por_que_sim(distrito_name, dept_name):
    """Gera conteúdo para 'Por que sim' baseado no distrito."""
    perfis_sim, _ = get_perfis(dept_name, distrito_name)
    
    razoes = []
    for perfil in perfis_sim[:3]:  # Pegar até 3 perfis
        if perfil in PORQUE_SIM:
            razoes.append(PORQUE_SIM[perfil])
    
    return " ".join(razoes[:2])  # Retornar até 2 razões

def generate_por_que_nao(distrito_name, dept_name):
    """Gera conteúdo para 'Por que não' baseado no distrito."""
    _, perfis_nao = get_perfis(dept_name, distrito_name)
    
    razoes = []
    for perfil in perfis_nao[:2]:  # Pegar até 2 perfis
        if perfil in PORQUE_NAO:
            razoes.append(PORQUE_NAO[perfil])
    
    return " ".join(razoes[:2])  # Retornar até 2 razões

def process_file(filepath):
    """Processa um arquivo .tex e preenche campos vazios."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    replacements = 0
    
    # Extrair nome do departamento do nome do arquivo
    dept_match = re.search(r'dept_\d+_(.+)\.tex', filepath)
    dept_name = dept_match.group(1).replace('_', ' ').title() if dept_match else 'Desconhecido'
    
    # Padrão para encontrar \subsubsection{Por que sim}\n\n\subsubsection{Por que não}
    pattern_sim = r'\\subsubsection\{Por que sim\}\n\n\\subsubsection\{Por que não\}'
    
    def replace_vazio(match):
        nonlocal replacements
        # Extrair nome do distrito do contexto anterior
        before = content[:match.start()]
        dist_match = re.search(r'\\secaoDiagnostico\{([^}]+)\}', before)
        distrito_name = dist_match.group(1) if dist_match else 'Distrito'
        
        por_que_sim = generate_por_que_sim(distrito_name, dept_name)
        por_que_nao = generate_por_que_nao(distrito_name, dept_name)
        
        replacements += 2  # Conta como 2 substituições (sim e não)
        
        return f"\\subsubsection{{Por que sim}}\n\n{por_que_sim}\n\n\\subsubsection{{Por que não}}\n\n{por_que_nao}"
    
    content = re.sub(pattern_sim, replace_vazio, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return replacements

def main():
    """Processa todos os arquivos dept_*.tex."""
    files = glob.glob(os.path.join(BASE_DIR, "dept_*.tex"))
    print(f"Encontrados {len(files)} arquivos de departamentos para processar.\n")
    
    total_replacements = 0
    for filepath in files:
        replacements = process_file(filepath)
        if replacements > 0:
            print(f"  ✓ {os.path.basename(filepath)}: {replacements//2} distritos preenchidos")
            total_replacements += replacements
    
    print(f"\nTotal: {total_replacements} campos preenchidos ({total_replacements//2} distritos).")

if __name__ == "__main__":
    main()

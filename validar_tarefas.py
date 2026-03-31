#!/usr/bin/env python3
"""
Script de validação em lote para tarefas POP- (popular)
Critérios de validação Nível 2:
1. DADOS.md existe
2. MEDIA.md existe
3. DADOS.md contém blocos 1..5 (geografia, população, riscos, recursos, sociopolítico)
4. DADOS.md contém URLs e referência temporal (data)
5. DADOS.md contém notas A-E
6. DADOS.md contém GSS
7. DADOS.md contém vulnerabilidades e mitigação
8. MEDIA.md contém ao menos 3 links
9. MEDIA.md contém blocos mínimos de cartografia/infraestrutura/risco
"""

import os
import re
import csv
from pathlib import Path

BASE_DIR = Path("/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/Departamentos")

def check_dados_md(filepath):
    """Verifica critérios do arquivo DADOS.md"""
    if not filepath.exists():
        return False, "DADOS.md não existe"
    
    content = filepath.read_text(encoding='utf-8')
    issues = []
    
    # Critério 3: Blocos 1-5
    blocos_minimos = [
        (r'geografia|militar|estrategico|coordenadas', 'Geografia/Contexto Estratégico'),
        (r'populacao|população|demografia|infraestrutura|habitante', 'População/Infraestrutura'),
        (r'risco|desastre|inundacao|inundação|clima|sismico|sísmico', 'Riscos Naturais'),
        (r'recurso|autossuficiencia|autossuficiência|agua|água|energia|solo', 'Recursos/Autossuficiência'),
        (r'politico|político|seguranca|segurança|institucional|sociopolitico', 'Ambiente Sociopolítico'),
    ]
    
    for pattern, nome in blocos_minimos:
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append(f"Falta bloco: {nome}")
    
    # Critério 4: URLs e datas
    urls = re.findall(r'https?://[^\s\)]+', content)
    datas = re.findall(r'\d{4}-\d{2}-\d{2}|acesso em|acessado em|202[4-6]', content, re.IGNORECASE)
    
    if len(urls) < 2:
        issues.append(f"Poucas URLs encontradas: {len(urls)}")
    if not datas:
        issues.append("Sem referência temporal")
    
    # Critério 5: Notas A-E
    notas_pattern = r'[A-E]:\s*\d+\.?\d*'
    notas = re.findall(notas_pattern, content, re.IGNORECASE)
    if len(notas) < 5:
        issues.append(f"Notas A-E incompletas: encontradas {len(notas)}")
    
    # Critério 6: GSS
    gss_pattern = r'GSS[:\s]*\d+\.?\d*|Global Safety Score|GSS\s*='
    if not re.search(gss_pattern, content, re.IGNORECASE):
        issues.append("GSS não encontrado")
    
    # Critério 7: Vulnerabilidades e mitigação
    vuln_patterns = [
        (r'vulnerabilidade|vulnerabilidade|fragilidade|ponto fraco|risco', 'Vulnerabilidades'),
        (r'mitigacao|mitigação|mitigar|recomendacao|recomendação|acao|ação', 'Mitigação'),
    ]
    
    for pattern, nome in vuln_patterns:
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append(f"Falta: {nome}")
    
    return len(issues) == 0, "; ".join(issues) if issues else "OK"


def check_media_md(filepath):
    """Verifica critérios do arquivo MEDIA.md"""
    if not filepath.exists():
        return False, "MEDIA.md não existe"
    
    content = filepath.read_text(encoding='utf-8')
    issues = []
    
    # Critério 8: Ao menos 3 links
    links = re.findall(r'https?://[^\s\)]+', content)
    if len(links) < 3:
        issues.append(f"Poucos links em MEDIA.md: {len(links)}")
    
    # Critério 9: Blocos mínimos
    blocos_media = [
        (r'cartografia|mapa|georreferenciamento', 'Cartografia/Mapas'),
        (r'infraestrutura|rodovia|estrada|energia|telecom', 'Infraestrutura'),
        (r'risco|perigo|ameaca|ameaça|inundacao|inundação', 'Risco'),
    ]
    
    for pattern, nome in blocos_media:
        if not re.search(pattern, content, re.IGNORECASE):
            issues.append(f"Falta bloco em MEDIA: {nome}")
    
    return len(issues) == 0, "; ".join(issues) if issues else "OK"


def validate_task(task_id, department, district):
    """Valida uma tarefa completa"""
    dept_dir = BASE_DIR / department
    district_dir = dept_dir / district
    
    dados_path = district_dir / "DADOS.md"
    media_path = district_dir / "MEDIA.md"
    
    dados_ok, dados_msg = check_dados_md(dados_path)
    media_ok, media_msg = check_media_md(media_path)
    
    status = "APPROVED" if (dados_ok and media_ok) else "NEEDS_FIX"
    
    issues = []
    if not dados_ok:
        issues.append(f"DADOS: {dados_msg}")
    if not media_ok:
        issues.append(f"MEDIA: {media_msg}")
    
    return {
        'task_id': task_id,
        'department': department,
        'district': district,
        'dados_exists': dados_path.exists(),
        'media_exists': media_path.exists(),
        'dados_ok': dados_ok,
        'media_ok': media_ok,
        'status': status,
        'issues': " | ".join(issues) if issues else "OK"
    }


def main():
    # Ler tarefas pendentes de validação
    tasks_file = Path("/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/tarefas_enxame/_needs_validation_sorted.csv")
    
    if not tasks_file.exists():
        print("Arquivo _needs_validation_sorted.csv não encontrado!")
        return
    
    results = []
    
    with open(tasks_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('task_id'):
                continue
            
            parts = line.split(',')
            if len(parts) < 5:
                continue
            
            task_id = parts[0]
            department = parts[2]
            district = parts[3]
            
            result = validate_task(task_id, department, district)
            results.append(result)
    
    # Imprimir resultados
    print("=" * 100)
    print("RELATÓRIO DE VALIDAÇÃO - 42 TAREFAS")
    print("=" * 100)
    
    approved = [r for r in results if r['status'] == 'APPROVED']
    needs_fix = [r for r in results if r['status'] == 'NEEDS_FIX']
    
    print(f"\nTotal: {len(results)} tarefas")
    print(f"✅ Aprovadas: {len(approved)}")
    print(f"❌ Precisa corrigir: {len(needs_fix)}")
    
    if needs_fix:
        print("\n" + "=" * 100)
        print("TAREFAS COM PROBLEMAS:")
        print("=" * 100)
        for r in needs_fix:
            print(f"\n📍 {r['task_id']}")
            print(f"   Departamento: {r['department']}")
            print(f"   Distrito: {r['district']}")
            print(f"   DADOS.md: {'✅' if r['dados_exists'] else '❌'} ({r['dados_ok']})")
            print(f"   MEDIA.md: {'✅' if r['media_exists'] else '❌'} ({r['media_ok']})")
            print(f"   Issues: {r['issues']}")
    
    # Salvar relatório CSV
    output_file = Path("/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/validacao_resultado.csv")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['task_id', 'department', 'district', 'dados_exists', 'media_exists', 'dados_ok', 'media_ok', 'status', 'issues'])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n📄 Relatório completo salvo em: {output_file}")
    
    # Atualizar arquivo TAREFAS_ENXAME.csv se todas aprovadas
    if len(needs_fix) == 0:
        print("\n✅ TODAS AS TAREFAS APROVADAS! Pronto para mover para done definitivo.")
    else:
        print(f"\n⚠️ {len(needs_fix)} tarefas precisam de correção antes de aprovação final.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Insere seções \subsubsection*{Oportunidades} e \subsubsection*{Diferenciais}
em todos os dossiês do livro LaTeX. Gera conteúdo a partir dos dados
já presentes em cada dossiê (intro, GSS, campo).
"""

import re
import os
import unicodedata

BASE = "/home/rodrigo/Projetos/IAs/realocação-estrategica-paraguai-pt-br/livro_latex/capitulos"

# Contexto departamental para enriquecer os textos
DEPT_CONTEXT = {
    "00": {
        "nome": "Distrito Capital",
        "oport_ctx": "principal hub financeiro, comercial e governamental do Paraguai; sede do BCP, ministérios e embaixadas; aeroporto Silvio Pettirossi a 14 km em Luque",
        "dif_ctx": "única capital nacional do Paraguai com oferta completa de serviços especializados, ensino superior (UNA, UCA, UP) e infraestrutura de saúde de alta complexidade",
        "perfil": "profissionais liberais, executivos, empreendedores de serviços de alto valor",
    },
    "01": {
        "nome": "Concepción",
        "oport_ctx": "nó logístico do Norte paraguaio; Rio Paraguai navegável; pecuária extensiva; mineração (calcário em San Lázaro/Vallemí); fronteira com Brasil pelo Rio Apa",
        "dif_ctx": "departamento de maior grau de isolamento estratégico do leste paraguaio, com presença militar consolidada e baixíssima pressão imigratória — ideal para perfis que valorizam anonimato e autossuficiência",
        "perfil": "produtores rurais, pecuaristas, perfis de alta autonomia",
    },
    "02": {
        "nome": "San Pedro",
        "oport_ctx": "expansão da fronteira agrícola de soja e milho no norte; programas MAG/BNF de crédito rural; Rio Jejuí e Rio Ypané com potencial hídrico; nova pavimentação de ramais pela MOPC",
        "dif_ctx": "departamento com maior disponibilidade de terra agricultável acessível (USD 1.500–4.000/ha) do leste paraguaio, com presença brasiguaia histórica que facilita integração",
        "perfil": "agricultores familiares, pecuaristas, pioneiros rurais com capital limitado",
    },
    "03": {
        "nome": "Cordillera",
        "oport_ctx": "turismo religioso e cultural (Caacupé, San Bernardino, Lago Ypacaraí); artesanato ao po'i (Atyra) e cerâmica (Tobatí); proxim idade a Assunção via Ruta 2; programas MAG de diversificação agrícola",
        "dif_ctx": "departamento com melhor combinação de proximidade a Assunção (30–80 km) e custo de vida rural, sendo o mais procurado por famílias brasileiras que trabalham na capital mas buscam residência no interior",
        "perfil": "famílias que trabalham em Assunção, produtores de fruticultura, turismo rural",
    },
    "04": {
        "nome": "Guairá",
        "oport_ctx": "único polo de mineração de ouro do Paraguai (Paso Yobái, ~600 kg/ano); viticultura e enoturismo (Independência); turismo ecológico (Ybytyruzú); artesanato ao po'i; campus regional da UNA",
        "dif_ctx": "departamento com o mais alto IDH do interior paraguaio (0,704) e a única região vinícola do país — diferencial cultural único que atrai imigrantes europeus e brasileiros com perfil enogastronômico",
        "perfil": "produtores rurais diversificados, turismo boutique, mineração artesanal",
    },
    "05": {
        "nome": "Caaguazú",
        "oport_ctx": "hub rodoviário central do Paraguai (cruzamento PY02×PY08 em Coronel Oviedo); maior polo brasiguaio organizado (Campo 9/Dr. Eulogio Estigarribia); silos e agroindústria; expansão soja/milho",
        "dif_ctx": "departamento com maior densidade de comunidade brasileira organizada do Paraguai — supermercados, igrejas, escolas e rádios em português funcionam em múltiplos municípios, reduzindo a barreira de integração",
        "perfil": "agricultores de soja/milho, empreendedores agroindustriais, famílias brasiguaias",
    },
    "06": {
        "nome": "Caazapá",
        "oport_ctx": "reservas naturais Lago Ypoá e Serra de San Rafael; potencial turístico ainda subexplorado; pecuária extensiva; MAG com programas de diversificação para horticultura e fruticultura",
        "dif_ctx": "departamento com menor especulação fundiária do sul paraguaio e maior tranquilidade social — para quem busca terra barata, isolamento real e comunidade campesina conservadora",
        "perfil": "produtores rurais de subsistência, off-gridders, pecuaristas extensivos",
    },
    "07": {
        "nome": "Itapúa",
        "oport_ctx": "maiores GSS do Paraguai (General Artigas 8.8, Fram 8.7); Colonias Unidas com cooperativas modelo alemãs/brasileiras/menonitas; royalties Yacyretá; Encarnación com Carnaval e Costera; Missões UNESCO",
        "dif_ctx": "único departamento do Paraguai com infraestrutura de nível europeu no campo — estradas pavimentadas rurais, silos cooperativos, hospitais privados e escolas técnicas em municípios com menos de 10k habitantes",
        "perfil": "agricultores capitalizados, famílias conservadoras europeias, turismo cultural",
    },
    "08": {
        "nome": "Misiones",
        "oport_ctx": "Rio Tebicuary e Rio Paraná com pesca e turismo náutico; San Juan Bautista como polo de serviços sul; pecuária de qualidade; turismo histórico (Ruta Jesuítica); baixa pressão demográfica",
        "dif_ctx": "departamento com menor competição por terras do sul paraguaio — distritos como San Patricio e Villa Florida oferecem solo fértil a preços 30–40% abaixo de Itapúa com perfil social equivalente",
        "perfil": "pecuaristas, aposentados, turismo pesqueiro, produção orgânica",
    },
    "09": {
        "nome": "Paraguarí",
        "oport_ctx": "Ruta 1 (eixo Assunção-sul) atravessa o departamento; Parque Nacional Ybycuí e Chololo para ecoturismo; Solo fértil para horticultura; distância de 60–90 km de Assunção com custo 40% menor",
        "dif_ctx": "departamento com melhor custo-benefício de proximidade à capital: Paraguarí, Carapeguá e Quiindy oferecem serviços completos, acesso à Ruta 1 e custo de vida campesino — ideal para famílias que não querem pagar preços metropolitanos",
        "perfil": "famílias de classe média, produtores de hortifrutigranjeiros, serviços rurais",
    },
    "10": {
        "nome": "Alto Paraná",
        "oport_ctx": "Itaipu Binacional (royalties, empregos, infraestrutura regional); Ciudad del Este (2ª cidade do PY, Zona Franca); maior colônia brasileira do Paraguai; Lago Itaipu para pesca e turismo náutico",
        "dif_ctx": "único departamento do Paraguai onde o imigrante brasileiro chega a uma comunidade já consolidada com supermercados, hospitais, escolas e empresas brasileiras — a 'Nova Brasil' do Paraguai",
        "perfil": "empresários, agricultores de soja, técnicos da Itaipu, comerciantes",
    },
    "11": {
        "nome": "Central",
        "oport_ctx": "área metropolitana de Assunção; aeroporto Silvio Pettirossi em Luque; CONMEBOL em Luque; porto de Villeta (maior exportação PY); polo industrial Mariano Roque Alonso; UNA em San Lorenzo",
        "dif_ctx": "único departamento com acesso simultâneo a mercado de trabalho metropolitano, infraestrutura industrial e custo de vida 50–60% inferior ao de São Paulo — ideal para quem quer trabalhar no nível de uma capital sem pagar preços de capital",
        "perfil": "profissionais qualificados, industriais, executivos de multinacionais",
    },
    "12": {
        "nome": "Ñeembucú",
        "oport_ctx": "fronteira com Argentina (cruzamento Pilar-Corientes); Rio Paraguai e húmedales para turismo de pesca e natureza; Pilar como polo comercial fronteiriço; bovinos de qualidade exportados para Argentina",
        "dif_ctx": "departamento com menor custo fundiário do sul paraguaio e acesso direto ao mercado argentino — para quem opera em ambos os lados da fronteira ou busca terras para pecuária de qualidade a preços mínimos",
        "perfil": "pecuaristas, pescadores comerciais, turismo de pesca, importadores/exportadores fronteiriços",
    },
    "13": {
        "nome": "Amambay",
        "oport_ctx": "Pedro Juan Caballero como polo comercial fronteiriço com Ponta Porã/BR; turismo de compras; reservas do Bosque Atlântico Interior; soja e milho com logística via BR-163; Parque Nacional Cerro Corá",
        "dif_ctx": "único departamento do Paraguai com fronteira seca com o Brasil (PJC-Ponta Porã), permitindo ao imigrante manter vínculos comerciais, bancários e sociais com o Brasil sem cruzar fronteira formal",
        "perfil": "comerciantes fronteiriços, agricultores do Mato Grosso do Sul, turismo de compras",
    },
    "14": {
        "nome": "Canindeyú",
        "oport_ctx": "expansão da soja no corredor norte; Reserva Biológica Mbaracayú (ecoturismo); fronteira com Brasil; energias renováveis; colonização brasiguaia recente com terras ainda acessíveis",
        "dif_ctx": "departamento com maior ritmo de crescimento agrícola do Paraguai nos últimos 10 anos — para o imigrante que quer entrar em uma região antes que os preços de terra se valorizem completamente",
        "perfil": "agricultores de soja/milho, especuladores de terra, ecoturismo",
    },
    "15": {
        "nome": "Presidente Hayes",
        "oport_ctx": "Ruta Trans-Chaco (PY09) como eixo logístico; pecuária extensiva no Chaco úmido; gás natural (Palo Santo); colonias menonitas com agroindústria diversificada; nova Ponte Héroes del Chaco",
        "dif_ctx": "único departamento chaqueño com infraestrutura urbana adequada (Villa Hayes, Benjamin Aceval) próxima à capital, combinando custo fundiário mínimo com acesso metropolitano — o verdadeiro 'oeste' paraguaio para os pioneiros",
        "perfil": "pecuaristas extensivos, colonos menonitas, agroindustriais do Chaco",
    },
    "16": {
        "nome": "Boquerón",
        "oport_ctx": "maior departamento do PY; colonias menonitas Menno, Fernheim e Neuland com agroindústria de referência mundial; gado de corte e leite de alta qualidade; laticínios Chortitzer exportam para 20 países",
        "dif_ctx": "o modelo menonita de organização cooperativa (Chortitzer, Friesland, TrebolFrisch) é o mais eficiente da América do Sul — imigrantes com capital e disposição para o Chaco acessam um ecossistema produtivo maduro sem precisar construir do zero",
        "perfil": "pecuaristas, colonos religiosos conservadores, agroindustriais capitalizados",
    },
    "17": {
        "nome": "Alto Paraguay",
        "oport_ctx": "Porto Casado com potencial logístico fluvial; mineração (ferro, manganês); Pantanal paraguaio para ecoturismo de alto padrão; pecuária extensiva de baixíssimo custo; fronteira tripartite PY-BR-BO",
        "dif_ctx": "departamento com menor densidade populacional do hemisfério ocidental (~0,15 hab/km²) — para quem busca isolamento absoluto, terra virtualmente gratuita e vida self-sufficient sem presença do Estado",
        "perfil": "extremo-isolamento, ecoturismo de alto padrão, pesquisa científica, pecuária extensiva",
    },
}

def slugify(name):
    """Converte nome para slug lowercase-sem-acentos-com-hífens."""
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore').decode('ascii')
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '-', name)
    name = name.strip('-')
    return name

def extrair_gss(bloco):
    """Extrai scores GSS do bloco do dossiê."""
    scores = {}
    for letra in ['A', 'B', 'C', 'D', 'E']:
        m = re.search(rf'{letra}\s*[-–]\s*\w[^&]*&\s*([\d.]+)', bloco)
        if m:
            try:
                scores[letra] = float(m.group(1))
            except ValueError:
                pass
    # GSS FINAL pode estar em \textbf{8.7} ou apenas 8.7
    m_final = re.search(r'GSS FINAL[^&]*&[^&]*?(\d+\.\d+)', bloco)
    if m_final:
        try:
            scores['FINAL'] = float(m_final.group(1))
        except ValueError:
            pass
    return scores

def extrair_intro(bloco):
    """Extrai o parágrafo de introdução do dossiê."""
    m = re.search(r'\\secaoDiagnostico\{[^}]+\}\{[^}]+\}\{(.+?)(?=\\subsubsection|\\begin\{table\}|\\end\{)', bloco, re.DOTALL)
    if m:
        intro = m.group(1).strip()
        intro = re.sub(r'\s+', ' ', intro)
        return intro[:400]
    return ""

def extrair_campo(bloco, campo):
    """Extrai valor de um campo do Dossiê de Campo."""
    m = re.search(rf'\\item\[{re.escape(campo)}\]\s+(.+?)(?=\\item\[|\\end\{{description\}})', bloco, re.DOTALL)
    if m:
        val = m.group(1).strip()
        val = re.sub(r'\s+', ' ', val)
        return val[:300]
    return ""

def gerar_oportunidades(nome, clave, dept_num, intro, scores, recursos, preco_terra, vias):
    """Gera parágrafo de Oportunidades."""
    ctx = DEPT_CONTEXT.get(dept_num, {})
    oport_ctx = ctx.get("oport_ctx", "")

    d_score = scores.get('D', 5.0)
    final_score = scores.get('FINAL', 5.0)

    # Classificar o GSS
    if final_score >= 8.0:
        gss_label = "pontuação GSS de elite ({:.1f}), indicando condições excepcionais".format(final_score)
    elif final_score >= 7.0:
        gss_label = "GSS de {:.1f}, classificado como Seguro".format(final_score)
    elif final_score >= 6.0:
        gss_label = "GSS de {:.1f}, classificado como Moderadamente Seguro".format(final_score)
    else:
        gss_label = "GSS de {:.1f}, recomendado para perfis resilientes".format(final_score)

    # Construir parágrafo
    partes = []

    # Contexto departamental
    if oport_ctx:
        partes.append(f"{nome} insere-se no departamento de {ctx.get('nome', '')}, caracterizado por {oport_ctx}.")

    # Autossuficiência (dimensão D)
    if d_score >= 7.5:
        partes.append(f"A dimensão de autossuficiência ({d_score:.1f}) é uma das mais fortes do distrito, refletida em recursos agrícolas disponíveis e capacidade local de produção de alimentos.")
    elif d_score >= 6.0:
        partes.append(f"Com dimensão de autossuficiência de {d_score:.1f}, o distrito apresenta base produtiva adequada para projetos de agricultura familiar e pecuária de pequeno a médio porte.")

    # Recursos locais
    if recursos and len(recursos) > 30:
        rec_limpo = re.sub(r'\\[a-zA-Z]+\{?[^}]*\}?', '', recursos)[:200]
        partes.append(f"Os recursos identificados incluem: {rec_limpo.strip('.')}.")

    # Preço da terra
    if preco_terra and 'USD' in preco_terra:
        pt = re.sub(r'\\[a-zA-Z]+\{?[^}]*\}?', '', preco_terra)[:150]
        partes.append(f"O mercado fundiário mostra: {pt.strip('.')}.")

    # Vias de acesso / logística
    if vias and len(vias) > 20:
        via_limpa = re.sub(r'\\[a-zA-Z]+\{?[^}]*\}?', '', vias)[:150]
        partes.append(f"A conectividade logística compreende: {via_limpa.strip('.')}.")

    # GSS final
    partes.append(f"A {gss_label} posiciona {nome} como opção concreta para realocação estratégica no contexto regional.")

    texto = " ".join(partes)
    # Limpar escapes LaTeX no texto gerado
    texto = re.sub(r'\\allowbreak\s*', '', texto)
    texto = re.sub(r'\\textasciitilde\s*', '~', texto)
    texto = re.sub(r'\\textbf\{([^}]+)\}', r'\1', texto)
    texto = re.sub(r'\\textit\{([^}]+)\}', r'\1', texto)
    texto = re.sub(r'\{\}', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

def gerar_diferenciais(nome, clave, dept_num, intro, scores, densidade, seguranca):
    """Gera parágrafo de Diferenciais."""
    ctx = DEPT_CONTEXT.get(dept_num, {})
    dif_ctx = ctx.get("dif_ctx", "")
    perfil = ctx.get("perfil", "imigrantes brasileiros com perfil rural ou empreendedor")

    # Identificar pontos mais altos
    score_items = [(k, v) for k, v in scores.items() if k != 'FINAL']
    score_items.sort(key=lambda x: x[1], reverse=True)

    dimensoes_nomes = {
        'A': 'posicionamento estratégico (ameaças externas)',
        'B': 'segurança social',
        'C': 'estabilidade natural (riscos climáticos e geológicos)',
        'D': 'autossuficiência produtiva',
        'E': 'solidez institucional',
    }

    partes = []

    # Contexto diferencial departamental
    if dif_ctx:
        partes.append(f"No contexto do departamento de {ctx.get('nome', '')}, {dif_ctx}.")

    # Pontos mais fortes
    if len(score_items) >= 2:
        top1 = score_items[0]
        top2 = score_items[1]
        d1 = dimensoes_nomes.get(top1[0], top1[0])
        d2 = dimensoes_nomes.get(top2[0], top2[0])
        partes.append(f"Os diferenciais mais marcantes de {nome} estão na dimensão de {d1} ({top1[0]}={top1[1]:.1f}) e na de {d2} ({top2[0]}={top2[1]:.1f}), combinação pouco comum entre distritos de GSS equivalente.")

    # Densidade / isolamento
    if densidade and len(densidade) > 10:
        dens_limpa = re.sub(r'\\[a-zA-Z]+\{?[^}]*\}?', '', densidade)[:150]
        partes.append(f"A densidade demográfica — {dens_limpa.strip()} — é um fator relevante para quem valoriza privacidade e baixo índice de conflito social.")

    # Segurança local
    if seguranca and len(seguranca) > 20:
        seg_limpa = re.sub(r'\\[a-zA-Z]+\{?[^}]*\}?', '', seguranca)[:180]
        partes.append(f"Em termos de segurança local: {seg_limpa.strip('.')}.")

    # Perfil do imigrante
    partes.append(f"O perfil de imigrante brasileiro que melhor se beneficia de {nome} é o de {perfil}, que encontra aqui uma combinação de custo de entrada acessível e qualidade de vida acima da média regional.")

    texto = " ".join(partes)
    texto = re.sub(r'\\allowbreak\s*', '', texto)
    texto = re.sub(r'\\textasciitilde\s*', '~', texto)
    texto = re.sub(r'\\textbf\{([^}]+)\}', r'\1', texto)
    texto = re.sub(r'\\textit\{([^}]+)\}', r'\1', texto)
    texto = re.sub(r'\{\}', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

def processar_arquivo(filepath, force=False):
    """Processa um arquivo .tex inserindo Oportunidades/Diferenciais."""

    with open(filepath, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Verificar se já tem seções completas
    if r'\subsubsection*{Oportunidades}' in conteudo and not force:
        count_existente = conteudo.count(r'\subsubsection*{Oportunidades}')
        count_total = conteudo.count(r'\secaoDiagnostico')
        if count_existente == count_total:
            print(f"  SKIP {os.path.basename(filepath)}: já completo ({count_existente}/{count_total})")
            return 0

    # Extrair número do departamento do nome do arquivo
    fname = os.path.basename(filepath)
    m_dept = re.match(r'dept_(\d+)_', fname)
    dept_num = m_dept.group(1) if m_dept else "00"

    # Encontrar todos os dossiês
    # Padrão: \secaoDiagnostico{NOME}{\mapaDistrito{CLAVE}}{...}
    pattern_dossiê = re.compile(
        r'(\\secaoDiagnostico\{([^}]+)\}\{\\mapaDistrito\{(\d+)\}\})',
        re.DOTALL
    )

    matches = list(pattern_dossiê.finditer(conteudo))
    if not matches:
        print(f"  SKIP {fname}: nenhum dossiê encontrado")
        return 0

    # Processar de trás para frente para não deslocar posições
    inserções = []

    for i, match in enumerate(matches):
        nome_distrito = match.group(2).strip()
        clave = match.group(3)

        # Extrair bloco do dossiê (do início deste ao início do próximo ou fim do arquivo)
        inicio_bloco = match.start()
        if i + 1 < len(matches):
            # Procurar \newpage antes do próximo \secaoDiagnostico
            proximo_inicio = matches[i + 1].start()
            # Recuar para incluir possível \newpage antes do próximo dossiê
            pre_proximo = conteudo[inicio_bloco:proximo_inicio]
            # Encontrar ponto de inserção: após o último conteúdo real
            m_newpage = re.search(r'(\\newpage\s*)(?=\\secaoDiagnostico)', pre_proximo)
            if m_newpage:
                fim_conteudo = inicio_bloco + m_newpage.start()
            else:
                fim_conteudo = proximo_inicio
        else:
            # Último dossiê: inserir no final do arquivo
            fim_conteudo = len(conteudo)

        bloco = conteudo[inicio_bloco:fim_conteudo]

        # Extrair dados do dossiê
        scores = extrair_gss(bloco)
        intro = extrair_intro(bloco)
        recursos = extrair_campo(bloco, 'Recursos Locais')
        preco_terra = extrair_campo(bloco, 'Preço da Terra')
        vias = extrair_campo(bloco, 'Vias de Acesso')
        densidade = extrair_campo(bloco, 'Densidade')
        seguranca = extrair_campo(bloco, 'Segurança')

        # Gerar conteúdo
        slug = slugify(nome_distrito)
        texto_oport = gerar_oportunidades(nome_distrito, clave, dept_num, intro, scores, recursos, preco_terra, vias)
        texto_dif = gerar_diferenciais(nome_distrito, clave, dept_num, intro, scores, densidade, seguranca)

        secoes = f"""
\\subsubsection*{{Oportunidades}}\\label{{oport-{slug}-{clave}}}
{texto_oport}

\\subsubsection*{{Diferenciais}}\\label{{dif-{slug}-{clave}}}
{texto_dif}
"""

        inserções.append((fim_conteudo, secoes))

    if not inserções:
        print(f"  SKIP {fname}: nenhuma inserção necessária")
        return 0

    # Aplicar inserções de trás para frente
    inserções.sort(key=lambda x: x[0], reverse=True)
    novo_conteudo = conteudo
    for pos, texto in inserções:
        # Encontrar a última linha não-vazia antes de pos
        trecho = novo_conteudo[:pos].rstrip()
        novo_conteudo = trecho + "\n" + texto + novo_conteudo[pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(novo_conteudo)

    count = novo_conteudo.count(r'\subsubsection*{Oportunidades}')
    total = novo_conteudo.count(r'\secaoDiagnostico')
    print(f"  OK {fname}: {count}/{total} seções inseridas")
    return count

def main():
    import sys
    force = '--force' in sys.argv

    arquivos = sorted([
        os.path.join(BASE, f) for f in os.listdir(BASE)
        if f.startswith('dept_') and f.endswith('.tex')
    ])

    total_inserido = 0
    for arq in arquivos:
        n = processar_arquivo(arq, force=force)
        total_inserido += n

    print(f"\nTotal: {total_inserido} seções Oportunidades inseridas")

    # Verificação final
    print("\n=== Verificação Final ===")
    for arq in arquivos:
        fname = os.path.basename(arq)
        with open(arq, 'r', encoding='utf-8') as f:
            c = f.read()
        oport = c.count(r'\subsubsection*{Oportunidades}')
        dossies = c.count(r'\secaoDiagnostico')
        status = "✓" if oport == dossies else "✗"
        print(f"  {status} {fname}: {oport}/{dossies}")

if __name__ == '__main__':
    main()

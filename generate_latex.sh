#!/bin/bash
BASE="livro_latex/capitulos"
LISTA_DEP="livro_latex/capitulos/lista_departamentos.tex"
APENDICE="$BASE/apendice_referencias.tex"
RAW_SOURCES="livro_latex/raw_sources.txt"
LEITORES_ALFA_MD="tarefas_enxame/entregaveis_livro/LEITORES_ALFA.md"
LEITORES_ALFA_TEX="$BASE/leitores_alfa.tex"

# Inicialização
echo "" > "$RAW_SOURCES"
echo "% Lista de departamentos" > "$LISTA_DEP"

clean_geo() {
    # Mantém o nome original (espanhol), apenas remove prefixos numéricos e underscores
    echo "$1" | sed -E 's/^[0-9]+_//' | tr '_' ' '
}

district_label() {
    local dept_id=$1
    local raw_dist_name=$2
    echo "dist:${dept_id}:${raw_dist_name}"
}

resolve_district_clave() {
    local dept_id=$1
    local district_name=$2
    python3 scripts/resolve_district_clave.py "$dept_id" "$district_name"
}

# Nomes oficiais dos departamentos em espanhol
dept_name_es() {
    case "$1" in
        00_Distrito_Capital)  echo "Distrito Capital" ;;
        01_Concepcion)        echo "Concepción" ;;
        02_San_Pedro)         echo "San Pedro" ;;
        03_Cordillera)        echo "Cordillera" ;;
        04_Guaira)            echo "Guairá" ;;
        05_Caaguazu)          echo "Caaguazú" ;;
        06_Caazapa)           echo "Caazapá" ;;
        07_Itapua)            echo "Itapúa" ;;
        08_Misiones)          echo "Misiones" ;;
        09_Paraguari)         echo "Paraguarí" ;;
        10_Alto_Parana)       echo "Alto Paraná" ;;
        11_Central)           echo "Central" ;;
        12_Neembucu)          echo "Ñeembucú" ;;
        13_Amambay)           echo "Amambay" ;;
        14_Canindeyu)         echo "Canindeyú" ;;
        15_Presidente_Hayes)  echo "Presidente Hayes" ;;
        16_Boqueron)          echo "Boquerón" ;;
        17_Alto_Paraguay)     echo "Alto Paraguay" ;;
        *)                    clean_geo "$1" ;;
    esac
}

# Extrai a seção do LEITORES_ALFA correspondente ao departamento e converte para LaTeX
extract_pacote_tex() {
    local dept_id=$1
    local dept_n=$2   # número inteiro sem zero à esquerda
    local outfile=$3

    if [ "$dept_n" -eq 0 ]; then
        # Distrito Capital: do "## 2." até antes de "### 2.6"
        awk '/^## 2\. /,/^### 2\.6 / { if ($0 !~ /^### 2\.6 /) print }' "$LEITORES_ALFA_MD" \
            | sed 's/^## [0-9.]* /## /; s/^### [0-9.]* /### /' \
            | sed 's/^## /# /; s/^### /## /' > t_pacote_raw.md
    else
        local sec_cur=$((dept_n + 5))
        local sec_next=$((dept_n + 6))
        # Outros departamentos: da subseção 2.N até a próxima ou ## 3.
        awk "/^### 2\\.${sec_cur}[ /]/,/^### 2\\.${sec_next}[ /]|^## 3\\./ \
             { if (\$0 !~ /^### 2\\.${sec_next}/ && \$0 !~ /^## 3\\./) print }" \
             "$LEITORES_ALFA_MD" \
            | sed 's/^### [0-9.]* /# /; s/^#### /## /' > t_pacote_raw.md
    fi

    # Remove linhas de fontes internas e referências de arquivos internos
    grep -v "LEITORES_ALFA_PKG\|Fontes-base do pacote\|Pendente para outra etapa\|\.md)\|leitura local esta ancorada\|leitura local está ancorada\|dept_[0-9]*_" t_pacote_raw.md \
        | sed 's/`[0-9]*_[A-Za-z_]*`//' \
        | sed 's/`dept_[^`]*`//g' \
        | sed 's/ ALLSKY_SFC_SW_DWN//g' \
        | sed 's/ PRECTOTCORR//g' \
        | sed 's/ \/ pacote [0-9]*//' \
        | sed 's/^# Pacote [0-9]*: /# /' \
        | sed 's/^## Pacote [0-9]*: /## /' \
        | sed '/^O pacote [0-9]* fecha a leitura/d' \
        | sed '/^O pacote [0-9]* cobre o departamento/d' \
        | sed 's/O pacote [0-9]* consolidou/A análise consolidou/' \
        | sed 's/O que o pacote confirma/Dados confirmados/' \
        | sed 's/cobertas no CSV do pacote/cobertas nesta análise/' \
        | sed 's/ consolidada no pacote/ consolidada/' \
        | sed 's/A leitura do pacote/A análise/' \
        | sed 's/_/ /g' > t_pacote_clean.md

    if [ $(wc -c < t_pacote_clean.md) -gt 50 ]; then
        pandoc t_pacote_clean.md -f markdown -t latex --top-level-division=section 2>/dev/null \
            | sed 's/\\label{[^}]*}//g' \
            | sed 's/\\texttt{[^}]*}//g' > "$outfile"
    else
        echo "" > "$outfile"
    fi
    rm -f t_pacote_raw.md t_pacote_clean.md
}

# Função para escapar caracteres especiais do LaTeX
escape_latex() {
    sed 's/&/\\\&/g; s/%/\\%/g; s/\$/\\\$/g; s/_/\\_/g; s/{/\\{/g; s/}/\\}/g; s/~/\\textasciitilde /g; s/#/\\#/g'
}

# Função para converter DMS para Decimal
convert_coords() {
    local raw=$1
    # Formato esperado: 25°23′S 57°08′W ou 25°23'S 57°08'W
    
    # Extrai Lat
    lat_deg=$(echo "$raw" | grep -oE "[0-9]+°" | head -1 | tr -d '°')
    lat_min=$(echo "$raw" | grep -oE "[0-9]+[′']" | head -1 | tr -d "′'")
    [ -z "$lat_min" ] && lat_min=0
    
    # Extrai Long
    long_deg=$(echo "$raw" | grep -oE "[0-9]+°" | tail -1 | tr -d '°')
    long_min=$(echo "$raw" | grep -oE "[0-9]+[′']" | tail -1 | tr -d "′'")
    [ -z "$long_min" ] && long_min=0
    
    if [[ -z "$lat_deg" ]] || [[ -z "$long_deg" ]]; then
        echo ""
        return
    fi

    # Cálculo com precisão de 4 casas
    lat_dec=$(echo "scale=4; -($lat_deg + $lat_min/60)" | bc -l)
    long_dec=$(echo "scale=4; -($long_deg + $long_min/60)" | bc -l)
    
    echo "$lat_dec $long_dec"
}

# Função para converter dossiê em lista de descrição técnica com enumitem
dossier_to_desc() {
    local input_file=$1
    echo "\begin{description}[style=nextline,leftmargin=0.5cm,font=\bfseries]"
    local has_items=false
    while IFS= read -r line; do
        if [[ $line =~ ^-[[:space:]]*\*\*(.*):\*\*(.*) ]]; then
            key=$(echo "${BASH_REMATCH[1]}" | sed 's/\*\*//g' | escape_latex)
            val=$(echo "${BASH_REMATCH[2]}" | sed 's/\*\*//g' | escape_latex)
            
            if [[ $key == "Leis Local" ]]; then
                val=$(echo "$val" | sed 's/brasileiros/estrangeiros/g')
                val=$(echo "$val" | sed -E 's/(Restrição de Fronteira|Livre de Restrição)/\\\\ \\textbf{\1}/g')
                if [[ $val == *"Restrição"* ]]; then
                    val="${val} \\\\ \textit{Aquisição de terra rural proibida para estrangeiros limítrofes.}"
                elif [[ $val == *"Livre"* ]]; then
                    val="${val} \\\\ \textit{Aquisição de terra rural permitida para estrangeiros.}"
                fi
            fi
            echo "\item[${key}] ${val}"
            has_items=true
        fi
    done < "$input_file"
    if [ "$has_items" = false ]; then echo "\item[-] N/A"; fi
    echo "\end{description}"
}

# Função para limpar e refinar conteúdo usando script Python
refine_content_py() {
    local input_file=$1
    local output_file=$2
    python3 scripts/refine_book_content.py "$input_file" "$output_file" "$RAW_SOURCES"
}

clean_content() {
    # Mantido para compatibilidade simples ou limpezas rápidas de strings específicas do LaTeX
    sed -E 's/^###? [0-9]+\.? (.*)/### \1/' | \
    sed -E 's/([0-9]{2})_//g' | \
    sed 's/_/ /g' | \
    sed -E 's/^[[:space:]•*-]+$//g' | \
    sed 's/nao/não/g' | \
    sed 's/Nao/Não/g' | \
    sed 's/Recomendacao/Recomendação/g' | \
    sed 's/Tecnica/Técnica/g' | \
    sed 's/brasileiros/estrangeiros/g'
}

apply_glossary() {
    local file=$1
    # EPP: Adiciona footnote apenas se não estiver seguido de parênteses (já explicado)
    sed -i 's/EPP\([^(]\)/EPP\\footnote{Ejército del Pueblo Paraguayo (Exército do Povo Paraguaio), grupo insurgente marxista-leninista que atua principalmente no norte do país.}\1/g' "$file"
    # SEN: Secretaría de Emergencia Nacional
    sed -i 's/SEN\([^(]\)/SEN\\footnote{Secretaría de Emergencia Nacional (Secretaria de Emergência Nacional), órgão governamental de resposta a desastres.}\1/g' "$file"
    # ANDE: Administración Nacional de Electricidade
    sed -i 's/ANDE\([^(]\)/ANDE\\footnote{Administración Nacional de Electricidade (Administração Nacional de Eletricidade), companhia estatal de energia.}\1/g' "$file"
    # ESSAP: Empresa de Servicios Sanitarios del Paraguay
    sed -i 's/ESSAP\([^(]\)/ESSAP\\footnote{Empresa de Servicios Sanitarios del Paraguay (Empresa de Serviços Sanitários do Paraguai), responsável pelo saneamento e água urbana.}\1/g' "$file"
    # INE: Instituto Nacional de Estadística
    sed -i 's/INE\([^(]\)/INE\\footnote{Instituto Nacional de Estadística (Instituto Nacional de Estatística), órgão oficial de dados demográficos e censitários.}\1/g' "$file"
}

apply_links() {
    local file=$1
    if [[ "$file" == *"panorama_nacional.tex"* ]]; then
        python3 scripts/apply_safe_links.py "$file"
    fi
}

# Extrai tabelas-chave dos arquivos departamentais (IDH, Segurança, Terra Rural)
# para exibição no capítulo do departamento (seções 3.1-3.4 do plano editorial)
extract_dept_tables() {
    local dept_id=$1
    local outfile=$2
    local dept_dir="Departamentos/${dept_id}"
    local tmpfile="t_dept_tables_raw.md"

    > "$tmpfile"

    local idh_file="${dept_dir}/IDH_DEPARTAMENTAL.md"
    if [ -f "$idh_file" ]; then
        printf "\n### Desenvolvimento Humano e Social\n\n" >> "$tmpfile"
        awk '/^## IDH Departamental$/{p=1} p && /^## / && !/^## IDH Departamental$/{p=0} p{print}' "$idh_file" \
            | grep -v "^> \|^---" >> "$tmpfile"
        printf "\n" >> "$tmpfile"
        awk '/^## Indicadores de Pobreza$/{p=1} p && /^## / && !/^## Indicadores de Pobreza$/{p=0} p{print}' "$idh_file" \
            | grep -v "^> \|^---" >> "$tmpfile"
        printf "\n" >> "$tmpfile"
        awk '/^## Infraestrutura Básica$/{p=1} p && /^## / && !/^## Infraestrutura Básica$/{p=0} p{print}' "$idh_file" \
            | grep -v "^> \|^---" >> "$tmpfile"
    fi

    local seg_file="${dept_dir}/SEGURANCA_DEPARTAMENTAL.md"
    if [ -f "$seg_file" ]; then
        printf "\n### Segurança Pública\n\n" >> "$tmpfile"
        awk '/^## Indicadores$/{p=1} p && /^## / && !/^## Indicadores$/{p=0} p{print}' "$seg_file" \
            | grep -v "^> \|^---" >> "$tmpfile"
    fi

    local terra_file="${dept_dir}/TERRA_RURAL_DEPARTAMENTAL.md"
    if [ -f "$terra_file" ]; then
        printf "\n### Mercado de Terra Rural\n\n" >> "$tmpfile"
        awk '/^## Preços por Tipo/{p=1} p && /^## / && !/^## Preços/{p=0} p{print}' "$terra_file" \
            | grep -v "^> \|^---" >> "$tmpfile"
        printf "\n" >> "$tmpfile"
        awk '/^## Características do Mercado/{p=1} p && /^## / && !/^## Características/{p=0} p{print}' "$terra_file" \
            | grep -v "^> \|^---" >> "$tmpfile"
    fi

    if [ $(wc -c < "$tmpfile") -gt 50 ]; then
        pandoc "$tmpfile" -f markdown -t latex 2>/dev/null \
            | sed 's/\\label{[^}]*}//g' \
            | sed 's/\\section{/\\subsection{/g' > "$outfile"
    else
        echo "" > "$outfile"
    fi
    rm -f "$tmpfile"
}


# 1. Metodologia
refine_content_py METODOLOGIA_RELOCACAO.md t_metod_refined.md
clean_content < t_metod_refined.md > t_metod.md
pandoc t_metod.md -f markdown -t latex -o "$BASE/metodologia.tex"
rm -f t_metod_refined.md

# 2. Panorama Nacional
refine_content_py tarefas_enxame/entregaveis_livro/CAPITULOS_LIVRO.md t_pan_refined.md
grep -vE "Data:|GSS medio|Mediana" t_pan_refined.md | clean_content > t_pan.md
pandoc t_pan.md -f markdown -t latex -o "$BASE/panorama_nacional.tex"
rm -f t_pan_refined.md
apply_glossary "$BASE/panorama_nacional.tex"
apply_links "$BASE/panorama_nacional.tex"
python3 scripts/generate_rank_nacional_tex.py tarefas_enxame/entregaveis_livro/RANK_NACIONAL.md >> "$BASE/panorama_nacional.tex"

# 3. Expansão Editorial - Leituras Alfa (sem seção 2 — vai para cada capítulo de departamento)
if [ -f "$LEITORES_ALFA_MD" ]; then
    # Mantém apenas seção 1 (seções 2-5 são editoriais/operacionais, não vão ao livro)
    awk '/^## [2-9]\./{exit} {print}' \
        "$LEITORES_ALFA_MD" > t_alfa_no_sec2.md
    refine_content_py t_alfa_no_sec2.md t_alfa_refined.md
    pandoc t_alfa_refined.md -f markdown -t latex --top-level-division=chapter -o "$LEITORES_ALFA_TEX"
    rm -f t_alfa_no_sec2.md t_alfa_refined.md
else
    cat > "$LEITORES_ALFA_TEX" <<'EOF'
\chapter{Expansão Editorial: Leituras Alfa}
\label{cap:leitores-alfa}

Este capítulo prepara a próxima etapa editorial do livro a partir das leituras feitas com o público-alvo.
EOF
fi

# 4. Departamentos
shopt -s nullglob
dept_dirs=(Departamentos/*/)
for dept_dir in "${dept_dirs[@]}"; do
    dept_id_raw=$(basename "$dept_dir")
    dept_num=$(echo "$dept_id_raw" | cut -d'_' -f1 | sed 's/^0//') # Remove zero à esquerda para o ifnum do LaTeX
    [ -z "$dept_num" ] && dept_num=0

    dept_name=$(dept_name_es "$dept_id_raw")
    tex_file="dept_${dept_id_raw}.tex"

    # Mapa grande do departamento com nome oficial em espanhol
    echo "\chapter{${dept_name}}\label{dept:${dept_name}}" > "$BASE/$tex_file"
    echo "\mapaparaguai{${dept_num}}{${dept_name}}" >> "$BASE/$tex_file"
    echo "\vfill\clearpage" >> "$BASE/$tex_file"

    # Análise documental do departamento (extraída de LEITORES_ALFA.md seção 2)
    extract_pacote_tex "$dept_id_raw" "$dept_num" t_pacote_dept.tex
    if [ -s t_pacote_dept.tex ]; then
        cat t_pacote_dept.tex >> "$BASE/$tex_file"
        echo "\clearpage" >> "$BASE/$tex_file"
    fi
    rm -f t_pacote_dept.tex

    # Tabelas departamentais (3.1-3.4): IDH, Segurança, Terra Rural
    extract_dept_tables "$dept_id_raw" t_dept_tables.tex
    if [ -s t_dept_tables.tex ]; then
        echo "\subsection*{Dados Departamentais}" >> "$BASE/$tex_file"
        cat t_dept_tables.tex >> "$BASE/$tex_file"
        echo "\clearpage" >> "$BASE/$tex_file"
    fi
    rm -f t_dept_tables.tex

    district_dirs=("${dept_dir}"*/)
    for dist_dir in "${district_dirs[@]}"; do
        dados_file="${dist_dir}DADOS.md"
        if [ -f "$dados_file" ]; then
            raw_dist_name=$(basename "$dist_dir")
            dist_name=$(clean_geo "$raw_dist_name")

            # 1. Pré-processamento e Refino (Fontes, Precipitação, Referências Internas)
            refine_content_py "$dados_file" "t_dados_refined.md"

            # 2. Extração de coordenadas para o Mini-Mapa
            raw_coords=$(grep "**Coordenadas:**" "t_dados_refined.md" | head -1)
            lat_long=$(convert_coords "$raw_coords")
            lat=$(echo "$lat_long" | awk '{print $1}')
            long=$(echo "$lat_long" | awk '{print $2}')

            # 3. Parsing GSS (Notas e Justificativas)
            nA=$(grep "\- A:" "t_dados_refined.md" | sed -E 's/.*A: ([0-9]\.[0-9]).*/\1/')
            jA=$(grep "\- A:" "t_dados_refined.md" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$jA" ] && jA="-"
            nB=$(grep "\- B:" "t_dados_refined.md" | sed -E 's/.*B: ([0-9]\.[0-9]).*/\1/')
            jB=$(grep "\- B:" "t_dados_refined.md" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$jB" ] && jB="-"
            nC=$(grep "\- C:" "t_dados_refined.md" | sed -E 's/.*C: ([0-9]\.[0-9]).*/\1/')
            jC=$(grep "\- C:" "t_dados_refined.md" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$jC" ] && jC="-"
            nD=$(grep "\- D:" "t_dados_refined.md" | sed -E 's/.*D: ([0-9]\.[0-9]).*/\1/')
            jD=$(grep "\- D:" "t_dados_refined.md" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$nD" ] && nD="0.0"
            [ -z "$jD" ] && jD="-"
            nE=$(grep "\- E:" "t_dados_refined.md" | sed -E 's/.*E: ([0-9]\.[0-9]).*/\1/')
            jE=$(grep "\- E:" "t_dados_refined.md" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$jE" ] && jE="-"
            valGSS=$(grep "GSS:" "t_dados_refined.md" | tail -n 1 | grep -oE "[0-9]\.[0-9]")
            classif=$(grep -A 1 "Classificacao:" "t_dados_refined.md" | tail -n 1 | sed 's/- //')

            echo "\newpage" >> "$BASE/$tex_file"
            
            # 4. EXTRAÇÃO DO BLOCO DE RESUMO (DIAGNÓSTICO + PORQUE SIM/NÃO)
            # Captura de "Diagnostico Integrado" até antes de "### Combustível" ou Seção 14 (Pesquisa Técnica)
            awk '/### Diagnostico Integrado/,/### Combustível|## 14\./ { if($0 !~ /### Combustível/ && $0 !~ /### Diagnostico/ && $0 !~ /## 14\./) print }' "t_dados_refined.md" | clean_content > t_full_content.md
            full_text=$(pandoc t_full_content.md -f markdown -t latex | sed 's/\\label{[^}]*}//g')
            
            # MAPA COM TIKZ
            if clave=$(resolve_district_clave "$dept_id_raw" "$raw_dist_name" "$lat" "$long" 2>/dev/null); then
                map_cmd="\mapaDistrito{${clave}}"
            elif [[ ! -z "$lat" ]] && [[ ! -z "$long" ]]; then
                map_cmd="\mapaConteudo{${lat}}{${long}}"
            else
                map_cmd="\mapaConteudo{0}{0}"
            fi

            # CHAMADA DO COMANDO PADRONIZADO (CONTEÚDO COMPLETO SURFANDO NO WRAPFIG)
            dist_label=$(district_label "$dept_id_raw" "$raw_dist_name")
            echo "\secaoDiagnostico{${dist_name}}{${map_cmd}}{${full_text}}{${dist_label}}" >> "$BASE/$tex_file"
            
            # 5. TABELA DE NOTAS GSS
            echo "\begin{table}[ht!]" >> "$BASE/$tex_file"
            echo "\small \begin{tabular}{p{3.0cm}p{0.8cm}p{6.0cm}} \toprule" >> "$BASE/$tex_file"
            echo "\textbf{Critério} & \textbf{Nota} & \textbf{Justificativa} \\\\ \midrule" >> "$BASE/$tex_file"
            echo "A - Ameaças Estratégicas & $nA & $(echo "$jA" | escape_latex) \\\\" >> "$BASE/$tex_file"
            echo "B - Risco Social & $nB & $(echo "$jB" | escape_latex) \\\\" >> "$BASE/$tex_file"
            echo "C - Riscos Naturais & $nC & $(echo "$jC" | escape_latex) \\\\" >> "$BASE/$tex_file"
            echo "D - Autossuficiência & $nD & $(echo "$jD" | escape_latex) \\\\" >> "$BASE/$tex_file"
            echo "E - Institucional & $nE & $(echo "$jE" | escape_latex) \\\\" >> "$BASE/$tex_file"
            echo "\midrule \textbf{GSS FINAL} & \textbf{$valGSS} & \textbf{$(echo "$classif" | escape_latex | sed 's/brasileiros/estrangeiros/g')} \\\\ \bottomrule \end{tabular}" >> "$BASE/$tex_file"
            echo "\end{table}" >> "$BASE/$tex_file"

            # 6. VULNERABILIDADES E DOSSIÊ TÉCNICO
            awk '/## 7\./,/## 9\.|## 14\./ { if($0 !~ /## [0-9]+\./) print }' "t_dados_refined.md" | clean_content > t_content.md
            if [ $(wc -c < t_content.md) -gt 5 ]; then
                echo -e "\n### Vulnerabilidades e Mitigação\n" > t_dist.md
                cat t_content.md >> t_dist.md
                pandoc t_dist.md -f markdown -t latex | sed "s/\\\\label{/\\\\label{vuln-${raw_dist_name}-/g" >> "$BASE/$tex_file"
            fi

            # Extração de Clima e Recursos (Dossiê)
            (awk '/### 1\./,/### 2\./ { if($0 !~ /### [0-9]+\./) print }' "t_dados_refined.md"; echo ""; \
             awk '/### 2\./,/### 3\./ { if($0 !~ /### [0-9]+\./) print }' "t_dados_refined.md"; echo ""; \
             awk '/### 3\./,/### 4\./ { if($0 !~ /### [0-9]+\./) print }' "t_dados_refined.md"; echo ""; \
             awk '/### 4\./,/### 5\./ { if($0 !~ /### [0-9]+\./) print }' "t_dados_refined.md"; echo ""; \
             awk '/### 5\./,/## 7\./ { if($0 !~ /## [67]\./ && $0 !~ /### [0-9]\./) print }' "t_dados_refined.md") > t_raw_dossier.md
            
            if [ $(wc -c < t_raw_dossier.md) -gt 20 ]; then
                echo -e "### Dossiê de Campo\n" > t_title.md
                pandoc t_title.md -f markdown -t latex | sed "s/\\\\label{/\\\\label{dossie-${raw_dist_name}-/g" >> "$BASE/$tex_file"
                dossier_to_desc t_raw_dossier.md >> "$BASE/$tex_file"
            fi
            
            # Clima (seção ### 3. Dados Climáticos e Ambientais — valores em mm/mês)
            awk '/### 3\. Dados Clim/,/### 4\./ { if($0 !~ /### [0-9]\./) print }' "t_dados_refined.md" | clean_content > t_clima.md
            if [ $(wc -c < t_clima.md) -gt 20 ]; then
                pandoc t_clima.md -f markdown -t latex >> "$BASE/$tex_file"
            fi

            # Solo (SoilGrids 2.0 — extrai bloco #### Solo com a tabela, para na próxima seção ###/##)
            awk 'found && (/^### / || /^## / || /^# [^#]/) {exit} /^#### Solo/{found=1} found' "t_dados_refined.md" > t_solo.md
            if [ $(wc -c < t_solo.md) -gt 20 ]; then
                pandoc t_solo.md -f markdown -t latex | sed 's/\\label{[^}]*}//g' >> "$BASE/$tex_file"
            fi

            # 4.2 Indicadores Sociais (tabela derivada dos dados departamentais e distritais)
            awk 'p && /^### / {exit} /^### Indicadores Sociais$/ {p=1} p' "t_dados_refined.md" > t_social.md
            if [ $(wc -c < t_social.md) -gt 20 ]; then
                pandoc t_social.md -f markdown -t latex | sed 's/\\label{[^}]*}//g' >> "$BASE/$tex_file"
            fi

            # 4.3 Serviços e Custo de Vida (Combustível, Celular, Internet, Imóvel, Saúde)
            awk '/^### Combustível$/{p=1} p{if(/^## 14\./) exit; print}' "t_dados_refined.md" > t_servicos.md
            if [ $(wc -c < t_servicos.md) -gt 20 ]; then
                pandoc t_servicos.md -f markdown -t latex \
                    | sed 's/\\label{[^}]*}//g' \
                    | sed 's/\\section{/\\subsubsection{/g; s/\\subsection{/\\subsubsection{/g' >> "$BASE/$tex_file"
            fi

            rm -f t_dados_refined.md t_dist.md t_content.md t_raw_dossier.md t_title.md t_clima.md t_solo.md t_full_content.md t_social.md t_servicos.md
        fi
    done
                apply_glossary "$BASE/$tex_file"
                apply_links "$BASE/$tex_file"
                echo "\include{capitulos/dept_${dept_id_raw}}" >> "$LISTA_DEP"
                done

echo "\chapter*{Referências Bibliográficas}" > "$APENDICE"
echo "\addcontentsline{toc}{chapter}{Referências Bibliográficas}" >> "$APENDICE"
echo "\small" >> "$APENDICE"
sort -u "$RAW_SOURCES" | grep "http" | sed 's/^/- /' > t_final_refs.md
pandoc t_final_refs.md -f markdown -t latex >> "$APENDICE"
rm -f "$RAW_SOURCES" t_final_refs.md t_metod.md t_pan.md

# LIMPEZA FINAL
for f in $BASE/dept_*.tex $BASE/metodologia.tex $BASE/panorama_nacional.tex $LEITORES_ALFA_TEX $APENDICE; do
    [ ! -f "$f" ] && continue
    sed -i 's/ não / não /g' "$f"
    sed -i 's/ não\./ não./g' "$f"
    sed -i 's/ não,/ não,/g' "$f"
    sed -i 's/ nao / não /g' "$f"
    sed -i 's/ nao\./ não./g' "$f"
    sed -i 's/ nao,/ não,/g' "$f"
    # Adiciona acento apenas se NÃO for um comando LaTeX (protege o início da linha ^\ e qualquer \)
    sed -i '/^\\[a-zA-Z]/ ! s/Diagnostico/Diagnóstico/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/populacao/população/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/Populacao/População/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/classificacao/classificação/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/Classificacao/Classificação/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/estrategico/estratégico/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/Estrategico/Estratégico/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/estrategica/estratégica/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/Estrategica/Estratégica/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/Tecnica/Técnica/g' "$f"
    sed -i '/^\\[a-zA-Z]/ ! s/Recomendacao/Recomendação/g' "$f"
    sed -i 's/autossuficiencia/autossuficiência/g' "$f"
    sed -i 's/Brasileiros/Estrangeiros/g' "$f"
    # Corrige duplicação "estrangeiros estrangeiros" causada por substituições em cascata
    sed -i 's/estrangeiros estrangeiros/estrangeiros/g' "$f"
    sed -i 's/Estrangeiros estrangeiros/Estrangeiros/g' "$f"
    # Insere allowbreak em barras de texto (ex: cidade/regiao), mas ignora comandos LaTeX ou caminhos
    sed -i '/mapas\// ! s/\([^\\]\)\//\1\/\\allowbreak /g' "$f"
    sed -i "s/′/'/g" "$f"
    sed -i "s/″/''/g" "$f"
    sed -i "s/–/--/g" "$f"
    # Subscripts Unicode → LaTeX math mode
    sed -i 's/₂/\$_2\$/g; s/₃/\$_3\$/g; s/₄/\$_4\$/g; s/₅/\$_5\$/g' "$f"
    # (acento de nomes de cidades aplicado após remoção de datas, no bloco abaixo)
    # Remove linhas com # solitário (heading vazio em Markdown que vira # inválido no LaTeX)
    sed -i '/^# *$/d' "$f"
    # Remove referências de data de acesso
    sed -i 's/ *(acesso em [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])//g' "$f"
    sed -i 's/,\? *acesso em [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]//g' "$f"
    # Remove data de referência do score GSS (ex: "GSS 6.5 em 2026-03-05" → "GSS 6.5")
    sed -i 's/\(GSS [0-9]\.[0-9]\) em [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/\1/g' "$f"
    # Adiciona acento em palavras comuns que ficam sem acento após processamento
    sed -i '/^\\[a-zA-Z]/ ! s/Referencia/Referência/g' "$f"
    # Nomes de cidades com acento (eram no-op antes)
    sed -i 's/Asuncion/Asunción/g' "$f"
    sed -i 's/Concepcion/Concepción/g' "$f"
    sed -i 's/Encarnacion/Encarnación/g' "$f"
done

# Remoção de artefatos editoriais nos capítulos gerados
echo "Removendo artefatos editoriais (Notas/Cálculo/Fontes)..."
python3 scripts/fix_tex_artifacts.py livro_latex/capitulos/dept_*.tex

# Correções de formatação: subsubsection{} vazio, footnotes repetidas, listas técnicas
echo "Corrigindo formatação (headings, footnotes, listas)..."
python3 scripts/fix_tex_formatting.py

# Integração dos dados departamentais detalhados nos capítulos (antes dos distritos)
echo "Integrando dados departamentais detalhados nos capítulos..."
python3 tarefas_enxame/gerar_apendice_latex.py
python3 scripts/integrate_apendice.py

# Correção de tabelas largas (longtable 8+ colunas → resizebox+tabular)
echo "Corrigindo tabelas largas para papel A5..."
python3 scripts/fix_wide_tables.py

# COMPILAÇÃO DO PDF (2 passadas para sumário e referências cruzadas corretos)
echo "Compilando PDF..."
cd livro_latex && \
    pdflatex -interaction=nonstopmode main.tex > /tmp/pdflatex_pass1.log 2>&1 && \
    pdflatex -interaction=nonstopmode main.tex > /tmp/pdflatex_pass2.log 2>&1 && \
    echo "PDF gerado: $(pdfinfo main.pdf | grep Pages)" || \
    echo "ERRO na compilação — ver /tmp/pdflatex_pass1.log"
cd ..

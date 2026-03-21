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

clean_content() {
    grep -vE "http|Fontes:|Regra aplicada|Onda [0-9]|Fase POP|NOTA:|Matriz de Evidencias|Evidencias" | \
    grep -vE "^[[:space:]•*-]*[0-9]\)" | \
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


# 1. Metodologia
clean_content < METODOLOGIA_RELOCACAO.md > t_metod.md
pandoc t_metod.md -f markdown -t latex -o "$BASE/metodologia.tex"

# 2. Panorama Nacional
grep -vE "Data:|GSS medio|Mediana|http" tarefas_enxame/entregaveis_livro/CAPITULOS_LIVRO.md | clean_content > t_pan.md
echo -e "\n## Ranking Nacional\n" >> t_pan.md
# Limpeza do Ranking preservando a estrutura
cat tarefas_enxame/entregaveis_livro/RANK_NACIONAL.md | sed -E 's/[0-9]{2}_//g' | sed 's/Distrito_Capital/Distrito Capital/g' | tr '_' ' ' >> t_raw_rank.md
clean_content < t_raw_rank.md >> t_pan.md
pandoc t_pan.md -f markdown -t latex -o "$BASE/panorama_nacional.tex"
rm -f t_raw_rank.md
apply_glossary "$BASE/panorama_nacional.tex"
apply_links "$BASE/panorama_nacional.tex"

# 3. Expansão Editorial - Leituras Alfa
if [ -f "$LEITORES_ALFA_MD" ]; then
    pandoc "$LEITORES_ALFA_MD" -f markdown -t latex --top-level-division=chapter -o "$LEITORES_ALFA_TEX"
else
    cat > "$LEITORES_ALFA_TEX" <<'EOF'
\chapter{Expansão Editorial: Leituras Alfa}
\label{cap:leitores-alfa}

Este capítulo prepara a próxima etapa editorial do livro a partir das leituras feitas com o público-alvo.
EOF
fi

# 4. Departamentos
for dept_dir in $(ls -d Departamentos/*/ | sort); do
    dept_id_raw=$(basename "$dept_dir")
    dept_num=$(echo "$dept_id_raw" | cut -d'_' -f1 | sed 's/^0//') # Remove zero à esquerda para o ifnum do LaTeX
    [ -z "$dept_num" ] && dept_num=0
    
    dept_name=$(clean_geo "$dept_id_raw")
    tex_file="dept_${dept_id_raw}.tex"
    
    # Adiciona o mapa grande do departamento com o NOME real e label para link
    echo "\chapter{${dept_name}}\label{dept:${dept_name}}" > "$BASE/$tex_file"
    echo "\mapaparaguai{${dept_num}}{${dept_name}}" >> "$BASE/$tex_file"
    echo "\vfill" >> "$BASE/$tex_file"

    for dist_dir in $(ls -d "${dept_dir}"*/ | sort); do
        dados_file="${dist_dir}DADOS.md"
        if [ -f "$dados_file" ]; then
            raw_dist_name=$(basename "$dist_dir")
            dist_name=$(clean_geo "$raw_dist_name")
            grep -E "http" "$dados_file" | sed 's/^[[:space:]*•-]*//' >> "$RAW_SOURCES"

            # Extração de coordenadas para o Mini-Mapa
            raw_coords=$(grep "**Coordenadas:**" "$dados_file" | head -1)
            lat_long=$(convert_coords "$raw_coords")
            lat=$(echo "$lat_long" | awk '{print $1}')
            long=$(echo "$lat_long" | awk '{print $2}')

            # Parsing GSS
            nA=$(grep "\- A:" "$dados_file" | sed -E 's/.*A: ([0-9]\.[0-9]).*/\1/')
            jA=$(grep "\- A:" "$dados_file" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$jA" ] && jA="-"
            nB=$(grep "\- B:" "$dados_file" | sed -E 's/.*B: ([0-9]\.[0-9]).*/\1/')
            jB=$(grep "\- B:" "$dados_file" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$jB" ] && jB="-"
            nC=$(grep "\- C:" "$dados_file" | sed -E 's/.*C: ([0-9]\.[0-9]).*/\1/')
            jC=$(grep "\- C:" "$dados_file" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$jC" ] && jC="-"
            nD=$(grep "\- D:" "$dados_file" | sed -E 's/.*D: ([0-9]\.[0-9]).*/\1/')
            jD=$(grep "\- D:" "$dados_file" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$nD" ] && nD="0.0"
            [ -z "$jD" ] && jD="-"
            nE=$(grep "\- E:" "$dados_file" | sed -E 's/.*E: ([0-9]\.[0-9]).*/\1/')
            jE=$(grep "\- E:" "$dados_file" | grep "(" | sed -E 's/.*\((.*)\).*/\1/')
            [ -z "$jE" ] && jE="-"
            valGSS=$(grep "GSS:" "$dados_file" | tail -n 1 | grep -oE "[0-9]\.[0-9]")
            classif=$(grep -A 1 "Classificacao:" "$dados_file" | tail -n 1 | sed 's/- //')

            echo "\newpage" >> "$BASE/$tex_file"
            
            # EXTRAÇÃO DO BLOCO COMPLETO (DIAGNÓSTICO + PRÓS/CONTRAS)
            # Captura de "Diagnostico Integrado" até antes da "Pontuacao GSS" (Seção 6 ou 7 conforme DADOS.md)
            awk '/### Diagnostico Integrado/,/## [67]\./ { if($0 !~ /## [67]\./ && $0 !~ /### Diagnostico/) print }' "$dados_file" | clean_content > t_full_content.md
            # Converte para LaTeX e remove labels automáticos que quebram o comando
            full_text=$(pandoc t_full_content.md -f markdown -t latex | sed 's/\\label{[^}]*}//g')
            
            # MAPA COM TIKZ
            if [[ ! -z "$lat" ]] && [[ ! -z "$long" ]]; then
                map_cmd="\mapaConteudo{${lat}}{${long}}"
            else
                map_cmd="\includegraphics[width=0.33\textwidth]{mapas/paraguai_base.pdf}"
            fi

            # CHAMADA DO COMANDO PADRONIZADO (CONTEÚDO COMPLETO SURFANDO NO WRAPFIG)
            echo "\secaoDiagnostico{${dist_name}}{${map_cmd}}{${full_text}}" >> "$BASE/$tex_file"
            
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

            awk '/## 7\./,/## [68]\./ { if($0 !~ /## [0-9]+\./) print }' "$dados_file" | clean_content > t_content.md
            if [ $(wc -c < t_content.md) -gt 5 ]; then
                echo -e "\n### Vulnerabilidades e Mitigação\n" > t_dist.md
                cat t_content.md >> t_dist.md
                pandoc t_dist.md -f markdown -t latex | sed "s/\\\\label{/\\\\label{vuln-${raw_dist_name}-/g" >> "$BASE/$tex_file"
            fi

            (awk '/### 1\./,/### 2\./ { if($0 !~ /### [0-9]+\./) print }' "$dados_file"; echo ""; \
             awk '/### 2\./,/### 3\./ { if($0 !~ /### [0-9]+\./) print }' "$dados_file"; echo ""; \
             awk '/### 3\./,/### 4\./ { if($0 !~ /### [0-9]+\./) print }' "$dados_file"; echo ""; \
             awk '/### 4\./,/### 5\./ { if($0 !~ /### [0-9]+\./) print }' "$dados_file"; echo ""; \
             awk '/### 5\./,/## 7\./ { if($0 !~ /## [67]\./ && $0 !~ /### [0-9]\./) print }' "$dados_file") > t_raw_dossier.md
            
            if [ $(wc -c < t_raw_dossier.md) -gt 20 ]; then
                echo -e "### Dossiê de Campo\n" > t_title.md
                    pandoc t_title.md -f markdown -t latex | sed "s/\\\\label{/\\\\label{dossie-${raw_dist_name}-/g" >> "$BASE/$tex_file"
                    dossier_to_desc t_raw_dossier.md >> "$BASE/$tex_file"
                fi
                rm -f t_dist.md t_content.md t_raw_dossier.md t_title.md t_diag.md t_rest.md
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
    # Insere allowbreak em barras de texto (ex: cidade/regiao), mas ignora comandos LaTeX ou caminhos
    sed -i '/mapas\// ! s/\([^\\]\)\//\1\/\\allowbreak /g' "$f"
    sed -i "s/′/'/g" "$f"
    sed -i "s/″/''/g" "$f"
    sed -i "s/–/--/g" "$f"
    # Protege caminhos de arquivos e nomes próprios
    sed -i 's/Asuncion/Asuncion/g' "$f"
    sed -i 's/Concepcion/Concepcion/g' "$f"
    sed -i 's/Encarnacion/Encarnacion/g' "$f"
done

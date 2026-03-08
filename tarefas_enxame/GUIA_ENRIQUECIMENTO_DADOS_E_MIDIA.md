# Guia de Execução - Enriquecimento de Dados e Mídia

Objetivo: substituir conteúdo baseado apenas em links por conteúdo textual consolidado em `DADOS.md` e mídia local copiada no projeto.

## Escopo por distrito
1. Ler links oficiais já listados em `DADOS.md` e `MEDIA.md`.
2. Extrair dados relevantes e registrar no `DADOS.md` com:
- valor/indicador
- fonte
- data da fonte
- data de acesso
3. Baixar ao menos 3 imagens relevantes para o distrito.
4. Salvar mídia local em `media/` dentro do diretório do distrito.
5. Atualizar `MEDIA.md` com:
- caminho local relativo da imagem
- link da fonte original
- legenda curta

## Estrutura obrigatória de mídia local
- `Departamentos/<dep>/<distrito>/media/`
- arquivos sugeridos:
  - `mapa_01.<ext>`
  - `infra_01.<ext>`
  - `risco_01.<ext>`

## Critério de pronto (DoD)
- `DADOS.md` contém conteúdo factual (não só lista de links) em todos os blocos 1..5.
- `DADOS.md` contém notas A-E e GSS recalculado com base no conteúdo final.
- `MEDIA.md` contém ao menos 3 mídias locais com link da origem.
- arquivos de mídia existem no diretório `media/`.

## Política de fontes
- Priorizar fontes oficiais (gov.py, ine.gov.py, meteorologia.gov.py, etc.).
- Sempre registrar data explícita da fonte e data de acesso.
- Se link quebrado, substituir por nova fonte oficial equivalente e registrar ajuste.

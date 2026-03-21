# Enxame de Agentes - Backlog Paralelo

## Objetivo
Executar em paralelo a criacao de estrutura, pesquisa e populacao de dados por distrito do Paraguai.

## Arquivo principal
- `TAREFAS_ENXAME.csv`: tarefas atomicas por distrito e por fase.
- `GUIA_EXECUCAO_AGENTE.md`: instrucoes operacionais para reduzir tokens e padronizar entrega.
- `PROMPT_BASE_ENXAME.md`: prompt pronto para repassar aos agentes.
- `TAREFAS_LEITORES_ALFA.csv`: backlog complementar criado a partir das leituras do publico alvo, com tarefas de pais, departamento e localidade.
- `pacotes_leitores_alfa_19/`: pacotes prontos para execucao por agentes, com 1 pacote de pais e 18 pacotes departamentais.
- `README_PACOTES_LEITORES_ALFA.md`: ordem de execucao e regras dos pacotes alfa.

## Fases por distrito
- `estrutura` (task_id `STR-*`)
- `pesquisa` (task_id `RES-*`, depende de `STR-*`)
- `popular` (task_id `POP-*`, depende de `RES-*`)

## Regras de execucao
- Cada agente deve puxar apenas tarefas com `status=todo`.
- Nao executar tarefa com dependencia pendente.
- Ao finalizar, atualizar `status` da tarefa para `done`.
- Se houver bloqueio de fonte, usar `status=blocked` e descrever motivo em log externo.

## Criterios minimos de qualidade por tarefa
- `estrutura`: arquivos presentes e com titulo do distrito correto.
- `pesquisa`: pelo menos 1 fonte oficial por categoria:
  1. geografia/militar
  2. populacao/infraestrutura
  3. riscos naturais
  4. recursos/autossuficiencia
  5. ambiente sociopolitico
- `popular`: formula GSS aplicada corretamente e texto de mitigacao acionavel.

## Sugestao de paralelismo
- Onda 1: todos `STR-*` pendentes.
- Onda 2: todos `RES-*` com `STR-*` concluido.
- Onda 3: todos `POP-*` com `RES-*` concluido.

## Observacao
O status `needs_validation` indica que existe conteudo preliminar no distrito, mas ainda sem validacao completa por fontes oficiais.

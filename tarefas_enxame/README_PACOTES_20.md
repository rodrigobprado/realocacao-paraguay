# Pacotes de Trabalho (20 agentes)

## Arquivos
- `PACOTES_20_MAP.csv`: mapa completo tarefa -> pacote.
- `PACOTES_20_RESUMO.csv`: contagem por pacote (total, prioridade e fase).
- `pacotes_20/pacote_XX.csv`: lista de tarefas de cada agente.

## Regra de distribuição
- Algoritmo: round-robin em 20 pacotes.
- Ordenação antes da distribuição:
  1. prioridade (`P1` antes de `P2`, depois `P3`)
  2. fase (`estrutura` -> `pesquisa` -> `popular`)
  3. ordenação alfabética por linha de tarefa

## Como usar no enxame
- Agente 01 recebe `pacotes_20/pacote_01.csv`
- Agente 02 recebe `pacotes_20/pacote_02.csv`
- ...
- Agente 20 recebe `pacotes_20/pacote_20.csv`

## Execução sugerida
- Cada agente processa suas tarefas na ordem `seq_in_package`.
- Respeitar `depends_on` antes de iniciar tarefa.
- Atualizar status no arquivo mestre ao concluir.

# Pacotes de Equivalencia ao Livro (24)

Data: 2026-03-05

Arquivos:
- `TAREFAS_EQUIVALENCIA_LIVRO.csv` (backlog mestre)
- `PACOTES_EQUIVALENCIA_24_MAP.csv` (mapeamento completo)
- `PACOTES_EQUIVALENCIA_24_RESUMO.csv` (resumo por pacote)
- `pacotes_equivalencia_24/pacote_XX.csv` (execucao distribuida)

Regra de execucao:
1. Processar `seq_in_package` em ordem.
2. Respeitar `depends_on`; se dependente pendente, marcar `blocked` e seguir.
3. Encerrar pacote somente com tarefas `done` ou `blocked`.

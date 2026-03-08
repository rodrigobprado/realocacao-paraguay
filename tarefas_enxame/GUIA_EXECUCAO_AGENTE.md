# Guia Rápido de Execução (Baixo Consumo de Tokens)

## Objetivo
Executar tarefas do enxame com máxima objetividade, consistência e rastreabilidade.

## Arquivos de entrada
- `tarefas_enxame/TAREFAS_ENXAME.csv` (mestre)
- `tarefas_enxame/pacotes_20/pacote_XX.csv` (execução geral)
- `tarefas_enxame/pacotes_validacao/pacote_validacao_XX.csv` (validação)

## Regra de ouro para economizar tokens
- Não explicar contexto longo.
- Não repetir metodologia inteira em cada resposta.
- Reportar apenas: tarefa executada, arquivos alterados, status final e bloqueio (se houver).

## Fluxo por tarefa
1. Ler linha da tarefa (`task_id`, `phase`, `path`, `depends_on`).
2. Verificar dependência:
   - Se dependência não concluída: marcar `blocked` e parar.
3. Executar conforme `phase`.
4. Validar critério mínimo da tarefa (`definition_of_done`).
5. Atualizar status para `done` (ou `blocked`).

## Instrução por fase
### `estrutura`
- Garantir pasta do distrito.
- Criar `DADOS.md` e `MEDIA.md` se ausentes.
- Usar títulos corretos do distrito.

### `pesquisa`
- Coletar fontes oficiais (URL + data) para 5 blocos:
  1. geografia/militar
  2. população/infraestrutura
  3. riscos naturais
  4. recursos/autossuficiência
  5. ambiente sociopolítico
- Priorizar: INE, órgãos oficiais paraguaios, mapas e documentos governamentais.

### `popular`
- Preencher `DADOS.md` com notas A-E e cálculo GSS.
- Incluir vulnerabilidades e mitigação acionável.
- Preencher `MEDIA.md` com mapas e referências visuais úteis.

## Política de qualidade mínima
- Não deixar valores “estimados” sem marcar explicitamente.
- Sempre incluir data de referência da fonte.
- Se houver incerteza crítica, marcar `blocked` com motivo curto.

## Formato de resposta do agente (obrigatório)
Use exatamente este formato, sem texto extra:

```
TASK: <task_id>
STATUS: done|blocked
FILES:
- <arquivo1>
- <arquivo2>
NOTES: <1 frase objetiva>
```

## Modelo de nota curta
- `NOTES: Fontes oficiais de 2024-2026 adicionadas; GSS recalculado.`
- `NOTES: Dependência RES-xx não concluída; tarefa bloqueada.`

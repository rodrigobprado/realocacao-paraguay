# Pacotes de Validacao (needs_validation)

## Escopo
Somente tarefas com status `needs_validation` extraidas de `TAREFAS_ENXAME.csv`.

## Arquivos
- `TAREFAS_NEEDS_VALIDATION.csv`
- `PACOTES_VALIDACAO_MAP.csv`
- `PACOTES_VALIDACAO_RESUMO.csv`
- `pacotes_validacao/pacote_validacao_XX.csv`

## Regra de distribuicao
- Round-robin em N pacotes (definido automaticamente para manter ~6 tarefas por pacote).
- Ordenacao previa por linha para previsibilidade.

## Objetivo de cada agente
1. Revisar `DADOS.md` e `MEDIA.md` do distrito.
2. Substituir estimativas por dados com fonte oficial (URL + data).
3. Recalcular GSS se houver ajuste nas notas A-E.
4. Registrar vulnerabilidades e mitigacoes alinhadas aos dados confirmados.

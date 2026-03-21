# Pacotes Leitores Alfa

## Estrutura
- `ALF_PKG_01`: tarefas de pais.
- `ALF_PKG_02` a `ALF_PKG_19`: um pacote por departamento, contendo a tarefa departamental primeiro e depois todas as tarefas de localidade daquele departamento.

## Ordem de Execucao
- Execute `ALF_PKG_01` antes de qualquer outro pacote.
- Depois execute os pacotes departamentais em ordem ou em paralelo, desde que o pacote de pais já esteja concluido.
- Dentro de cada pacote, siga `seq_in_package` sem pular dependencias.

## Observacao
- Esse recorte foi montado para reduzir bloqueios entre agentes: cada pacote departamental fecha sua arvore de dependencia local, o que permite trabalho independente e revisao localizada.

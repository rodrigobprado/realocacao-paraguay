# Referência de Formatação - Guia Estratégico Paraguai 2026

Este documento preserva as definições técnicas da "Versão Editorial v1.0".

## Componentes Estéticos Principais:
1.  **Comando `\secaoDiagnostico`**: Localizado no preâmbulo de `livro_latex/main.tex`. Controla o título em largura total, o mapa flutuante (wrapfig) e o texto surround.
2.  **Lógica de Extração**: Localizada em `generate_latex.sh`. Utiliza `awk` para separar o Diagnóstico Integrado das listas de Por que sim/não, permitindo que ambos contornem a imagem juntos.
3.  **Hiperlinks Seguros**: Controlados pelo script `scripts/apply_safe_links.py`. Resolve o problema de recursividade em nomes de cidades/departamentos.
4.  **Glossário Automático**: Inserido via `apply_glossary` no script Bash, adicionando footnotes explicativas apenas em siglas não descritas.

## Para replicar esta formatação em novos dados:
1.  Garanta que o `DADOS.md` do distrito possua o cabeçalho `### Diagnostico Integrado`.
2.  Execute `./generate_latex.sh`.
3.  Compile o `main.tex` três vezes para processar sumário, links e notas de rodapé.

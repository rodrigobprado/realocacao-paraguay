# Instruções para Tradução do Livro

## Estrutura de Diretórios

```
livro_latex/
├── capitulos/          ← Versão original em português (não modificar)
├── traducao/
│   ├── GLOSSARIO_TRADUCAO.md   ← Este arquivo + glossário
│   ├── INSTRUCOES_TRADUCAO.md  ← Instruções
│   ├── es/capitulos/           ← Tradução espanhol
│   ├── en/capitulos/           ← Tradução inglês
│   ├── de/capitulos/           ← Tradução alemão
│   └── fr/capitulos/           ← Tradução francês
├── main.tex            ← main em português
├── main_es.tex         ← main em espanhol (a criar)
├── main_en.tex         ← main em inglês (a criar)
├── main_de.tex         ← main em alemão (a criar)
└── main_fr.tex         ← main em francês (a criar)
```

## Prioridade de Tradução

1. **Espanhol** — máxima prioridade; idioma do Paraguai e de toda América Latina
2. **Inglês** — mercado internacional amplo
3. **Alemão** — comunidade menonita paraguaia + mercado europeu
4. **Francês** — mercado europeu e francófono

## Fluxo de Trabalho Recomendado

### Fase 1 — Finalização do original (português)
- [ ] Todos os campos das fichas preenchidos
- [ ] Capítulos novos integrados (migração, prefácio, mapa de decisão)
- [ ] Revisão final de ortografia e formatação
- [ ] PDF final aprovado

### Fase 2 — Tradução Espanhol (prioridade 1)
- [ ] Traduzir prefácio.tex → es/capitulos/prefacio_es.tex
- [ ] Traduzir metodologia.tex → es/capitulos/metodologia_es.tex
- [ ] Traduzir panorama_nacional.tex → es/capitulos/panorama_nacional_es.tex
- [ ] Traduzir migracao_legal.tex → es/capitulos/migracion_legal_es.tex
- [ ] Traduzir mapa_decisao.tex → es/capitulos/mapa_decision_es.tex
- [ ] Traduzir comparativo_paises.tex → es/capitulos/comparativo_paises_es.tex
- [ ] Traduzir todos os dept_*.tex → es/capitulos/dept_*.tex
- [ ] Adaptar main_es.tex (seções em espanhol)
- [ ] Revisão por falante nativo de espanhol paraguaio
- [ ] Compilar PDF espanhol

### Fase 3 — Tradução Inglês
- Similar à Fase 2, mas adaptar termos para contexto anglófono
- Adicionar explicações de contexto cultural paraguaio para leitores não-latino-americanos
- Revisão por falante nativo de inglês

### Fase 4 — Tradução Alemão e Francês
- Adaptar seções culturais para o contexto europeu
- Enfatizar aspectos legais e fiscais (mais relevantes para investidores europeus)

## Ferramentas de Tradução Recomendadas

1. **Primeira passagem**: DeepL ou GPT-4/Claude para tradução automática
2. **Revisão terminológica**: usar o GLOSSARIO_TRADUCAO.md como referência
3. **Revisão nativa**: contratar revisor nativo para cada idioma (essencial)
4. **Consistência**: usar o script `verificar_consistencia_traducao.py` (a criar)

## Elementos que NÃO devem ser traduzidos

- Nomes de departamentos e distritos paraguaios
- Nomes de órgãos governamentais paraguaios (manter sigla + explicação em parênteses)
- Nomes de rios, reservatórios e accidentes geográficos
- Termos em guarani (explicar entre parênteses)
- "Ruta PY01", "Ruta PY07" etc.
- Coordenadas GPS (23°18'S 56°45'W)

## Adaptações por Idioma

### Para Inglês
- Adicionar nota introdutória explicando o sistema de departamentos/distritos
- Adicionar conversão de hectares para acres nas tabelas de terra
- Converter todas as temperaturas para Fahrenheit (ou adicionar paralelo)
- Explicar o sistema elétrico paraguaio (voltagem, frequência)

### Para Alemão
- Seção especial sobre comunidades menonitas (Filadelfia, Loma Plata, Neuland)
- Enfatizar conexões históricas alemãs no Paraguai (Nueva Germania etc.)
- Adaptar formato de valores monetários (ponto decimal, separador de milhar)

### Para Francês
- Adaptar o tom para o estilo formal francês
- Adicionar contexto sobre acordos bilaterais França-Paraguai
- Formato de datas: DD/MM/AAAA

## Script de Extração de Strings

Para extrair todos os strings traduzíveis automaticamente:

```bash
# Extrair textos de todos os .tex (excluindo comandos LaTeX)
python3 extrair_strings_traducao.py
```

O script gera `strings_para_traducao.json` com todos os parágrafos e textos
sem comandos LaTeX, prontos para tradução via API.

# Leitores Alfa - Pacote ALF_PKG_10 (08 Misiones)

Data de consolidacao: 2026-03-20

Este arquivo consolida o pacote ALF_PKG_10 para o departamento 08_Misiones. A leitura departamental esta ancorada em `LEITORES_ALFA_DEP_08_Misiones.md`, `RANK_08_Misiones.md` e `SINT_08_Misiones.md`. Onde ha fonte oficial com extracao possivel, o pacote fecha o item; onde a serie nao ficou confiavel neste ciclo, a pendencia permanece explicitada.

## 1. Departamento: 08_Misiones

### Historico, geografia, populacao, economia e vocacao
- Misiones combina nodos urbanos relevantes, base agropecuaria e corredores de mobilidade associados a PY01 e PY04.
- Populacao oficial: 111.142 habitantes no Censo 2022 do INE.
- Vocacao economica: pecuaria, arroz, soja, mel e servicos associados aos polos urbanos de San Ignacio, San Juan Bautista e Ayolas.

### Concessionaria de energia e tarifas
- Concessionaria: ANDE.
- Tarifa nacional lida no pliego oficial da ANDE; nao ha tabela regional por distrito para este pacote.

### Estudo de solo
- Pendente para outra etapa: nao foi localizado estudo unico e consolidado de solo por distrito em fonte oficial aberta neste ciclo.

### Saude, ensino, seguranca e infraestrutura
- Hospitais/centros de saude: maior concentracao em San Ignacio, San Juan Bautista e Ayolas.
- Universidades: a oferta do CONES se concentra nas cidades-polo do departamento.
- Presidios/unidades prisionais: inventario ainda nao consolidado em base unica.
- Bases militares/navais/aereas: inventario oficial departamental nao consolidado.
- Portos e aerodromos: DINAC oferece referencia nacional de aerodromos; o departamento exige leitura combinada com hidrologia e mobilidade local.
- Sistema integrado de vigilancia: remeter ALF-PAIS-05.

### Terra rural
- Tamanho minimo legal: remeter ALF-PAIS-06.
- Valor medio de terra rural: as fichas locais trazem faixas e proxies, mas sem base oficial unica por distrito.

## 2. Localidades do pacote

O pacote cobre as 10 localidades abaixo:

- Ayolas
- San Ignacio
- San Juan Bautista
- San Miguel
- San Patricio
- Santa Maria
- Santa Rosa
- Santiago
- Villa Florida
- Yabebyry

## 3. Ficha climatica de San Juan Bautista (capital departamental)

Dados climatologicos extraidos da NASA POWER Climatology API, periodo 2001-2020, coordenadas -26.67°S / -57.15°W. Acesso em 2026-03-20.

**Irradiância solar global — ALLSKY_SFC_SW_DWN (kWh/m²/dia):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 6.72 | 6.24 | 5.35 | 4.27 | 3.26 | 2.73 | 3.11 | 3.77 | 4.48 | 5.37 | 6.41 | 6.79 |

Média anual: 4.87 kWh/m²/dia. Mínimo: Jun (2.73) | Máximo: Dez (6.79).

**Precipitação — PRECTOTCORR (mm/mês):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 136 | 119 | 133 | 164 | 143 | 88 | 72 | 62 | 93 | 181 | 184 | 168 |

Média anual: ~1.545 mm/ano. Estação chuvosa Out-Nov; seca Jul-Ago (mínimo em Ago).

**Inclinação solar recomendada:** 27° Norte (anual); 37° no inverno (Jun-Ago); 17° no verão (Nov-Jan). Base: latitude -26.67°S.

## 4. Sintese operacional

### O que o pacote confirma
- Misiones apresenta estrutura territorial com alta dependência de polos urbanos centrais e forte sensibilidade a corredores rodoviários.
- A leitura departamental reforça San Ignacio como nó logístico e San Juan Bautista como centro institucional.
- O pacote fica amarrado ao dossiê local e ao ranking departamental já existentes no repositório.

### O que ainda falta consolidar
- Pendente para outra etapa: serie mensal completa de solar e pluviometria por localidade em formato de candle.
- Pendente para outra etapa: validar a serie climatica com boletins mensais do DMH antes de qualquer interpolacao.
- Pendente para outra etapa: idade mediana por localidade.
- Pendente para outra etapa: IDH, indice de saude, indice de violencia e demais indices sociais padronizados por distrito/localidade.
- Pendente para outra etapa: internet, celular, combustiveis, eletropostos e gas encanado com inventario unico.
- Pendente para outra etapa: custo medio formal de moradia, terra, comercio e servicos.
- Pendente para outra etapa: poluicao luminosa e inventario comercial consolidado.
- Pendente para outra etapa: inventario oficial completo de saude, delegacias, presidios e infraestrutura estrategica.

## 5. Referencias-base do pacote
- `LEITORES_ALFA_DEP_08_Misiones.md`
- `RANK_08_Misiones.md`
- `SINT_08_Misiones.md`

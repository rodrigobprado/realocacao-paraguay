# Leitores Alfa - Pacote ALF_PKG_12 (10 Alto Parana)

Data de consolidacao: 2026-03-20

Este arquivo consolida o pacote ALF_PKG_12 para o departamento 10_Alto_Parana. A leitura departamental esta ancorada em `LEITORES_ALFA_DEP_10_Alto_Parana.md`, `RANK_10_Alto_Parana.md` e `SINT_10_Alto_Parana.md`. Onde ha fonte oficial com extracao possivel, o pacote fecha o item; onde a serie nao ficou confiavel neste ciclo, a pendencia permanece explicitada.

## 1. Departamento: 10_Alto_Parana

### Historico, geografia, populacao, economia e vocacao
- Alto Paraná combina fronteira internacional, comércio transfronteiriço, polos urbanos densos e áreas rurais produtivas.
- O departamento é ancorado por Ciudad del Este, Hernandarias, Presidente Franco e Minga Guazú, que concentram infraestrutura, serviços e circulação de mercadorias.
- Vocação econômica: comércio, logística, serviços, energia, agronegócio e cadeias associadas à fronteira.

### Concessionaria de energia e tarifas
- Concessionaria: ANDE.
- Tarifa nacional lida no pliego oficial da ANDE; nao ha tabela regional por distrito para este pacote.

### Estudo de solo
- Pendente para outra etapa: nao foi localizado estudo unico e consolidado de solo por distrito em fonte oficial aberta neste ciclo.

### Saude, ensino, seguranca e infraestrutura
- Hospitais/centros de saude: forte concentracao em Ciudad del Este, Hernandarias e Presidente Franco.
- Universidades: maior densidade nas áreas metropolitanas do departamento.
- Presidios/unidades prisionais: inventario ainda nao consolidado em base unica.
- Bases militares/navais/aereas: inventario oficial departamental nao consolidado.
- Portos e aerodromos: o Aeroporto Guarani e a fronteira fluvial/rodoviaria tornam o departamento estrategico.
- Sistema integrado de vigilancia: remeter ALF-PAIS-05.

### Terra rural
- Tamanho minimo legal: remeter ALF-PAIS-06.
- Valor medio de terra rural: as fichas locais trazem faixas e proxies, mas sem base oficial unica por distrito.

## 2. Localidades do pacote

O pacote cobre as 22 localidades abaixo:

- Ciudad del Este
- Doctor Raul Pena
- Domingo Martinez de Irala
- Hernandarias
- Iruna
- Itakyry
- Juan Emilio OLeary
- Juan Leon Mallorquin
- Los Cedrales
- Mbaracayu
- Minga Guazu
- Minga Pora
- Nacunday
- Naranjal
- Presidente Franco
- San Alberto
- San Cristobal
- Santa Fe del Parana
- Santa Rita
- Santa Rosa del Monday
- Tavapy
- Yguazu

## 3. Ficha climatica de Ciudad del Este (capital departamental)

Dados climatologicos extraidos da NASA POWER Climatology API, periodo 2001-2020, coordenadas -25.51°S / -54.61°W. Acesso em 2026-03-20.

**Irradiância solar global — ALLSKY_SFC_SW_DWN (kWh/m²/dia):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 6.52 | 5.97 | 5.45 | 4.50 | 3.33 | 2.93 | 3.24 | 4.04 | 4.60 | 5.28 | 6.33 | 6.55 |

Média anual: 4.89 kWh/m²/dia. Mínimo: Jun (2.93) | Máximo: Dez (6.55).

**Precipitação — PRECTOTCORR (mm/dia):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 4.73 | 4.56 | 3.78 | 4.14 | 5.26 | 3.59 | 2.75 | 2.26 | 4.02 | 6.80 | 5.29 | 5.76 |

Média anual: ~1.610 mm/ano. Estação chuvosa Out-Dez; seca Jul-Ago (mínimo em Ago).

**Inclinação solar recomendada:** 26° Norte (anual); 36° no inverno (Jun-Ago); 16° no verão (Nov-Jan). Base: latitude -25.51°S.

## 4. Sintese operacional

### O que o pacote confirma
- Alto Paraná continua como o principal eixo de fronteira comercial do Paraguai.
- Ciudad del Este domina o hub de comércio e suprimentos, enquanto Hernandarias e Presidente Franco reforçam a cintura urbana estratégica.
- Santa Rosa del Monday e San Alberto lideram o ranking de GSS do departamento.
- A leitura do pacote permanece consistente com o capítulo do livro e com o ranking departamental já publicado.

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
- `LEITORES_ALFA_DEP_10_Alto_Parana.md`
- `RANK_10_Alto_Parana.md`
- `SINT_10_Alto_Parana.md`

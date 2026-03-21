# Leitores Alfa - Pacote ALF_PKG_03 (01 Concepcion)

Data de consolidacao: 2026-03-20

Este pacote fecha a leitura editorial de `01_Concepcion` e organiza os 14 distritos cobertos no CSV `ALF_PKG_03`. O foco principal foi alinhar o dossie departamental, registrar o ranking existente e explicitar o que ainda falta em fonte oficial aberta.

## 1. Departamento: 01_Concepcion

### Historico, geografia, populacao, economia e vocacao
- Concepcion e o eixo logístico-militar do norte paraguaio, com porto, aeroporto em modernizacao e estruturas de defesa interna.
- Populacao oficial do departamento/distrito capital: a base do INE e os DADOS.md ja consolidam o recorte demografico e territorial.
- Vocacao economica: pecuaria, grãos, comercio regional, logística fluvial e rodoviaria.

### Concessionaria de energia e tarifas
- Concessionaria: ANDE.
- Tarifa nacional lida como referencia, sem tabela regional distrital unica neste pacote.

### Estudo de solo
- Pendente para outra etapa: nao foi localizado estudo unico e consolidado de solo por distrito em fonte oficial aberta neste ciclo.

### Saude, ensino, seguranca e infraestrutura
- Hospitais/centros de saude: Concepcion e Horqueta concentram a malha principal.
- Universidades: oferta habilitada pelo CONES nas cidades-polo.
- Presidios/unidades prisionais: inventario ainda nao consolidado em base unica.
- Bases militares/navais/aereas: CODI, Regimento de Infantaria N° 10 e aeroporto ANC aparecem como referencias centrais.
- Portos e aerodromos: porto de Concepcion e o aeroporto ANC estruturam a leitura do departamento.
- Sistema integrado de vigilancia: remeter ALF-PAIS-05.

### Terra rural
- Tamanho minimo legal: remeter ALF-PAIS-06.
- Valor medio de terra rural: as fichas locais trazem faixas e proxies, mas sem base oficial unica por distrito.

## 2. Localidades do pacote

O pacote cobre 14 localidades:

- Arroyito
- Azotey
- Belen
- Concepcion
- Horqueta
- Itacua
- Loreto
- Paso_Barreto
- Paso_Horqueta
- San_Alfredo
- San_Carlos_del_Apa
- San_Lazaro
- Sargento_Jose_Felix_Lopez
- Yby_Yau

## 3. Ficha climatica de Concepcion (capital departamental)

Dados climatológicos extraídos da NASA POWER Climatology API, período 2001-2020, coordenadas -23.40°S / -57.43°W. Acesso em 2026-03-20.

**Irradiância solar global — ALLSKY_SFC_SW_DWN (kWh/m²/dia):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 6.68 | 6.07 | 5.58 | 4.63 | 3.47 | 3.00 | 3.30 | 4.09 | 4.68 | 5.49 | 6.34 | 6.61 |

Média anual: 4.99 kWh/m²/dia. Mínimo: Jun (3.00) | Máximo: Jan (6.68).

**Precipitação — PRECTOTCORR (mm/mês):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 157 | 151 | 120 | 139 | 116 | 71 | 48 | 31 | 73 | 151 | 204 | 167 |

Média anual: ~1.427 mm/ano. Estação chuvosa Out-Mai; seca Jun-Set (mínimo em Ago).

**Inclinação solar recomendada:** 23° Norte (anual); 33° no inverno (Jun-Ago); 13° no verão (Nov-Jan). Base: latitude -23.40°S.

## 4. Sintese operacional

### O que o pacote confirma
- Concepcion segue como o departamento mais sensivel do norte em termos de fronteira seca, logística e segurança.
- Horqueta e Yby Yau sao eixos operacionais fortes; Arroyito, Belen e Loreto sustentam a base de continuidade territorial.
- A leitura departamental fica amarrada ao capitulo ja existente em `dept_01_Concepcion.tex`.
- Lacuna de solar/pluviometria da capital departamental fechada com dados NASA POWER Climatology API (2001-2020).

### O que ainda falta consolidar
- Pendente para outra etapa: serie mensal por localidade (demais 13 distritos além da capital) em formato de candle.
- Pendente para outra etapa: validar a serie climatica com boletins mensais do DMH antes de qualquer interpolacao.
- Pendente para outra etapa: idade mediana por localidade.
- Pendente para outra etapa: IDH, indice de saude, indice de violencia e demais indices sociais padronizados por distrito/localidade.
- Pendente para outra etapa: internet, celular, combustiveis, eletropostos e gas encanado com inventario unico.
- Pendente para outra etapa: custo medio formal de moradia, terra, comercio e servicos.
- Pendente para outra etapa: poluicao luminosa e inventario comercial consolidado.
- Pendente para outra etapa: inventario oficial completo de saude, delegacias, presidios e infraestrutura estrategica.

## 5. Referencias-base do pacote
- `LEITORES_ALFA_DEP_01_Concepcion.md`
- `RANK_01_Concepcion.md`
- `SINT_01_Concepcion.md`

# Leitores Alfa - Pacote ALF_PKG_04 (02 San Pedro)

Data de consolidacao: 2026-03-20

Este arquivo consolida o pacote ALF_PKG_04, que cobre o dossie departamental de 02 San Pedro e as 22 localidades do pacote. A base factual principal esta nos DADOS.md e MEDIA.md de cada localidade, com sinteses complementares em `SINT_02_San_Pedro.md` e `RANK_02_San_Pedro.md`.

## 1. Departamento: 02_San_Pedro

### Historico, geografia, populacao, economia e vocacao
- San Pedro combina eixo rodoviario, base agropecuaria e densidade rural variada. A leitura departamental consolidada em `LEITORES_ALFA_DEP_02_San_Pedro.md` descreve a estrutura territorial, a populacao distrital e a vocacao produtiva de suporte ao norte do pais.
- Populacao e distribuicao territorial: consolidadas no INE via Censo 2022 e nos DADOS.md distritais.
- Indicadores demograficos consolidados no INE: 254.908 pessoas de 15+ anos, mediana de idade de 26 anos em 2025, fecundidade de 2,90 filhos por mulher e 8,4 anos de estudo em media no departamento.
- Economia e vocacao: base agropecuaria, logistica rodoviaria e nucleos urbanos de servicos em torno da capital departamental e dos eixos PY03 e corredores secundarios.
- Indicadores locais do INE: as tabelas distritais agora fecham anos de estudo para as localidades do pacote; idade mediana permanece consolidada no nível departamental, e a nomenclatura de Itacurubi segue como ressalva de validação.

### Concessionaria de energia e tarifas
- Concessionaria: ANDE, com tarifa nacional no pliego vigente.
- Pendente para outra etapa: nao existe tabela regional por distrito. Valores de tarifa permanecem nacionais, nao departamentais.

### Estudo de solo
- Pendente para outra etapa: estudo de solo departamental consolidado nao foi fechado em fonte unica neste ciclo.
- Uso pratico: as fichas locais ja registram aptidao agricola, relevo e condicionantes hidricas para decisao territorial.

### Saude, ensino, seguranca e infraestrutura
- Hospitais e centros de saude: base local consolidada nos DADOS.md de cada distrito, com dependencias de San Estanislao e San Pedro de Ycuamandiyu em varios pontos.
- Universidades: referencia nacional do CONES, com extracao por sede ainda parcial.
- Presidios: inventario distrital consolidado apenas de forma parcial; a leitura local mantém a lacuna aberta.
- Bases militares, portos, aeroportos e aerodromos: referencia departamental complementar nos DADOS.md e na leitura de geografia estrategica.
- Sistema integrado de vigilancia: referencia nacional no sistema 911; leitura local mantem lacuna por distrito.
- Escolaridade e alfabetizacao: a tabela distrital do INE no Censo 2022 fecha os anos de estudo e o alfabetismo por distrito, reduzindo a lacuna para o nivel local.

### Terra rural
- Tamanho minimo legal: referencia nacional e regime de fronteira devem ser lidos por localidade.
- Valor medio de terra rural: as fichas locais trazem proxies e faixas estimadas, mas sem base oficial unica.

## 2. Localidades do pacote

O pacote cobre as 22 localidades abaixo, cada uma com DADOS.md e MEDIA.md proprios:

- 25_de_Diciembre
- Antequera
- Capiibary
- Chore
- General_Elizardo_Aquino
- General_Resquin
- Guayaibi
- Itacurubi
- Itacurubi_del_Rosario
- Liberacion
- Lima
- Nueva_Germania
- San_Estanislao
- San_Pablo
- San_Pedro_de_Ycuamandiyu
- San_Vicente_Pancholo
- Santa_Rosa_del_Aguaray
- Tacuati
- Union
- Villa_del_Rosario
- Yataity_del_Norte
- Yrybucua

## 3. Ficha climatica de San Pedro de Ycuamandiyu (capital departamental)

Dados climatológicos extraídos da NASA POWER Climatology API, período 2001-2020, coordenadas -24.10°S / -57.08°W. Acesso em 2026-03-20.

**Irradiância solar global — ALLSKY_SFC_SW_DWN (kWh/m²/dia):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 6.64 | 6.13 | 5.48 | 4.54 | 3.38 | 2.87 | 3.21 | 3.93 | 4.62 | 5.45 | 6.37 | 6.67 |

Média anual: 4.93 kWh/m²/dia. Mínimo: Jun (2.87) | Máximo: Dez (6.67).

**Precipitação — PRECTOTCORR (mm/mês):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 136 | 152 | 114 | 142 | 140 | 80 | 59 | 37 | 83 | 166 | 196 | 168 |

Média anual: ~1.471 mm/ano. Estação chuvosa Out-Mai; seca Jun-Set (mínimo em Ago).

**Inclinação solar recomendada:** 24° Norte (anual); 34° no inverno (Jun-Ago); 14° no verão (Nov-Jan). Base: latitude -24.10°S.

## 4. Sintese operacional

### O que o pacote confirma
- O departamento possui forte base agropecuaria e corredores rodoviarios que organizam a vida economica e logistica.
- A parte de maior qualidade territorial tende a se concentrar nas localidades com melhor conectividade, melhor resiliencia hidrica e maior continuidade de servicos.
- A leitura de GSS do conjunto mostra dispersao relevante entre nucleos mais seguros e nucleos mais expostos.
- A leitura demografica local agora está fechada para anos de estudo por localidade e para idade mediana no nivel departamental; restam apenas as conferências nominais e setoriais sem tabela pública única.

### O que ainda falta consolidar
- Lacuna de solar/pluviometria da capital departamental fechada com dados NASA POWER (2001-2020).
- Pendente para outra etapa: serie mensal das 21 localidades restantes além da capital.
- Pendente para outra etapa: validar essa serie com boletins climatologicos mensais do DMH antes de qualquer interpolacao.
- Pendente para outra etapa: IDH e alguns indices sociais padronizados por distrito/localidade quando houver base oficial.
- Pendente para outra etapa: custo medio formal de moradia, terra, internet, celular e combustivel por distrito.
- Pendente para outra etapa: inventario unico de postos de saude, hospitais, delegacias, presidos, correios e comercio local.
- Pendente para outra etapa: indices de poluicao luminosa, violencia padronizada e custo de serviços ainda sem base aberta unica.

## 5. Referencias-base do pacote
- `LEITORES_ALFA_DEP_02_San_Pedro.md`
- `RANK_02_San_Pedro.md`
- `SINT_02_San_Pedro.md`

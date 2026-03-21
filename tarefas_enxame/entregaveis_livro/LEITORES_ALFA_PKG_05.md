# Leitores Alfa - Pacote ALF_PKG_05 (03 Cordillera)

Data de consolidacao: 2026-03-20

Este pacote fecha a leitura editorial de `03_Cordillera` e organiza os 19 distritos cobertos no CSV `ALF_PKG_05`. O foco principal foi alinhar o dossie departamental, registrar o ranking existente e explicitar o que ainda falta em fonte oficial aberta.

## 1. Departamento: 03_Cordillera

### Historico, geografia, populacao, economia e vocacao
- Cordillera funciona como transicao entre a area metropolitana e o interior produtivo, com forte peso de servicos, turismo e residencias de alto valor em alguns municipios.
- Populacao oficial: consolidada no INE Censo 2022 para o recorte departamental.
- Vocacao economica: agropecuaria, turismo, servicos, comercio local e produção artesanal.

### Concessionaria de energia e tarifas
- Concessionaria: ANDE.
- Tarifa nacional lida como referencia, sem tabela regional distrital unica neste pacote.

### Estudo de solo
- Pendente para outra etapa: nao foi localizado estudo unico e consolidado de solo por distrito em fonte oficial aberta neste ciclo.

### Saude, ensino, seguranca e infraestrutura
- Hospitais/centros de saude: Caacupe, San Bernardino e Arroyos y Esteros concentram a malha principal.
- Universidades: oferta habilitada pelo CONES nas cidades-polo.
- Presidios/unidades prisionais: inventario ainda nao consolidado em base unica.
- Bases militares/navais/aereas: inventario oficial departamental nao consolidado neste ciclo.
- Portos e aerodromos: leitura departamental prioriza mobilidade rodoviaria e conexoes metropolitanas.
- Sistema integrado de vigilancia: remeter ALF-PAIS-05.

### Terra rural
- Tamanho minimo legal: remeter ALF-PAIS-06.
- Valor medio de terra rural: as fichas locais trazem faixas e proxies, mas sem base oficial unica por distrito.

## 2. Localidades do pacote

O pacote cobre 19 localidades:

- Altos
- Arroyos_y_Esteros
- Caacupe
- Caraguatay
- Emboscada
- Eusebio_Ayala
- General_Aquino
- Isla_Pucu
- Itacurubi_de_la_Cordillera
- Loma_Grande
- Mbocayaty_del_Yhaguy
- Nueva_Colombia
- Primero_de_Marzo
- Piribebuy
- San_Bernardino
- San_Jose_de_los_Arroyos
- Santa_Elena
- Tobati
- Valenzuela

## 3. Ficha climatica de Caacupe (capital departamental)

Dados climatológicos extraídos da NASA POWER Climatology API, período 2001-2020, coordenadas -25.38°S / -57.15°W. Acesso em 2026-03-20.

**Irradiância solar global — ALLSKY_SFC_SW_DWN (kWh/m²/dia):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 6.76 | 6.20 | 5.42 | 4.44 | 3.36 | 2.83 | 3.21 | 3.93 | 4.61 | 5.49 | 6.42 | 6.78 |

Média anual: 4.95 kWh/m²/dia. Mínimo: Jun (2.83) | Máximo: Dez (6.78).

**Precipitação — PRECTOTCORR (mm/mês):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 127 | 140 | 133 | 148 | 152 | 78 | 66 | 41 | 77 | 171 | 193 | 175 |

Média anual: ~1.500 mm/ano. Estação chuvosa Out-Mai; seca Jun-Set (mínimo em Ago).

**Inclinação solar recomendada:** 25° Norte (anual); 35° no inverno (Jun-Ago); 15° no verão (Nov-Jan). Base: latitude -25.38°S.

## 4. Sintese operacional

### O que o pacote confirma
- Cordillera segue como departamento de alta continuidade territorial, forte componente residencial e boa conectividade regional.
- Altos e San Bernardino puxam o perfil de maior valor e continuidade; Caacupe e Piribebuy concentram peso institucional e turístico.
- A leitura departamental fica amarrada ao capitulo ja existente em `dept_03_Cordillera.tex`.

### O que ainda falta consolidar
- Lacuna de solar/pluviometria da capital fechada com dados NASA POWER (2001-2020).
- Pendente para outra etapa: serie mensal das 18 localidades restantes além da capital.
- Pendente para outra etapa: validar a serie climatica com boletins mensais do DMH antes de qualquer interpolacao.
- Pendente para outra etapa: idade mediana por localidade.
- Pendente para outra etapa: IDH, indice de saude, indice de violencia e demais indices sociais padronizados por distrito/localidade.
- Pendente para outra etapa: internet, celular, combustiveis, eletropostos e gas encanado com inventario unico.
- Pendente para outra etapa: custo medio formal de moradia, terra, comercio e servicos.
- Pendente para outra etapa: poluicao luminosa e inventario comercial consolidado.
- Pendente para outra etapa: inventario oficial completo de saude, delegacias, presidios e infraestrutura estrategica.

## 5. Referencias-base do pacote
- `LEITORES_ALFA_DEP_03_Cordillera.md`
- `RANK_03_Cordillera.md`
- `SINT_03_Cordillera.md`

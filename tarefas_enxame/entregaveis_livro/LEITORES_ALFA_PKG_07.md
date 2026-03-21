# Leitores Alfa - Pacote ALF_PKG_07 (05 Caaguazu)

Data de consolidacao: 2026-03-20

Este pacote fecha a leitura editorial de `05_Caaguazu` e organiza os 22 distritos cobertos no CSV `ALF_PKG_07`. O foco principal foi alinhar o dossie departamental, registrar o ranking existente e explicitar o que ainda falta em fonte oficial aberta.

## 1. Departamento: 05_Caaguazu

### Historico, geografia, populacao, economia e vocacao
- Caaguazu e o coracão logístico do Paraguai, com o cruzamento das Rutas PY02 e PY08 em Coronel Oviedo, polo industrial de Caaguazu e forte base agropecuaria.
- Populacao oficial: consolidada no INE Censo 2022 para o recorte departamental.
- Vocacao economica: agroindustria (soja, milho, trigo, cana), logística rodoviária e comercio regional.

### Concessionaria de energia e tarifas
- Concessionaria: ANDE.
- Tarifa nacional lida como referencia, sem tabela regional distrital unica neste pacote.

### Estudo de solo
- Pendente para outra etapa: nao foi localizado estudo unico e consolidado de solo por distrito em fonte oficial aberta neste ciclo.
- Uso pratico: latossolo vermelho de alta fertilidade e aptidao para graos e silvicultura registrados nos DADOS.md distritais.

### Saude, ensino, seguranca e infraestrutura
- Hospitais/centros de saude: Coronel Oviedo concentra o Novo Hospital Geral (referencia regional interior) e IPS.
- Universidades: oferta habilitada pelo CONES nas cidades-polo (Coronel Oviedo, Caaguazu).
- Presidios/unidades prisionais: inventario ainda nao consolidado em base unica.
- Bases militares/navais/aereas: inventario oficial departamental nao consolidado neste ciclo.
- Sistema integrado de vigilancia: remeter ALF-PAIS-05.

### Terra rural
- Tamanho minimo legal: remeter ALF-PAIS-06.
- Valor medio de terra rural: US$ 5.000-10.000/ha nas fichas locais; sem base oficial unica por distrito.

## 2. Localidades do pacote

O pacote cobre 22 localidades:

- Caaguazu
- Carayao
- Coronel_Oviedo
- Doctor_Cecilio_Baez
- Doctor_Eulogio_Estigarribia
- Doctor_Juan_Manuel_Frutos
- Jose_Domingo_Ocampos
- La_Pastora
- Mariscal_Francisco_Solano_Lopez
- Nueva_Londres
- Nueva_Toledo
- RI_Tres_Corrales
- Raul_Arsenio_Oviedo
- Repatriacion
- San_Joaquin
- San_Jose_de_los_Arroyos
- Santa_Rosa_del_Mbutuy
- Simon_Bolivar
- Tembiapora
- Tres_de_Febrero
- Vaqueria
- Yhu

## 3. Ficha climatica de Coronel Oviedo (capital departamental)

Dados climatológicos extraídos da NASA POWER Climatology API, período 2001-2020, coordenadas -25.44°S / -56.44°W. Acesso em 2026-03-20.

**Irradiância solar global — ALLSKY_SFC_SW_DWN (kWh/m²/dia):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 6.74 | 6.20 | 5.50 | 4.48 | 3.35 | 2.88 | 3.21 | 3.96 | 4.59 | 5.43 | 6.43 | 6.81 |

Média anual: 4.96 kWh/m²/dia. Mínimo: Jun (2.88) | Máximo: Dez (6.81).

**Precipitação — PRECTOTCORR (mm/mês):**

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 131 | 136 | 131 | 152 | 172 | 90 | 75 | 52 | 92 | 187 | 190 | 166 |

Média anual: ~1.573 mm/ano. Estação chuvosa Out-Mai; seca Jun-Set (mínimo em Ago).

**Inclinação solar recomendada:** 25° Norte (anual); 35° no inverno (Jun-Ago); 15° no verão (Nov-Jan). Base: latitude -25.44°S.

## 4. Sintese operacional

### O que o pacote confirma
- Caaguazu e o departamento mais logisticamente central do interior paraguaio, com Coronel Oviedo como no do trafico nacional.
- A base agropecuaria e agroindustrial e forte, com alta resiliencia produtiva no corredor PY02/PY08.
- Lacuna de solar/pluviometria da capital fechada com dados NASA POWER (2001-2020).

### O que ainda falta consolidar
- Pendente para outra etapa: serie mensal das 21 localidades restantes além da capital.
- Pendente para outra etapa: validar a serie climatica com boletins mensais do DMH.
- Pendente para outra etapa: IDH, indice de saude, indice de violencia e demais indices sociais padronizados.
- Pendente para outra etapa: internet, celular, combustiveis, eletropostos e gas encanado com inventario unico.
- Pendente para outra etapa: custo medio formal de moradia, terra, comercio e servicos por distrito.
- Pendente para outra etapa: poluicao luminosa e inventario comercial consolidado.
- Pendente para outra etapa: inventario oficial completo de saude, delegacias, presidios e infraestrutura estrategica.

## 5. Referencias-base do pacote
- `LEITORES_ALFA_DEP_05_Caaguazu.md`
- `RANK_05_Caaguazu.md`
- `SINT_05_Caaguazu.md`

# Leitores Alfa - Pacote ALF_PKG_06 (04 Guaira)

Data de consolidacao: 2026-03-20

Este pacote fecha a leitura editorial de `04_Guaira` e organiza os 18 distritos cobertos no CSV `ALF_PKG_06`. O foco principal foi alinhar o dossie departamental, registrar o ranking existente e explicitar o que ainda falta em fonte oficial aberta.

## 1. Departamento: 04_Guaira

### Historico, geografia, populacao, economia e vocacao
- Guaira combina turismo, servicos, agricultura e um eixo urbano forte em Villarrica.
- Populacao oficial: consolidada no INE Censo 2022 para o recorte departamental.
- Vocacao economica: agropecuaria, turismo, comercio local e producao artesanal.

### Concessionaria de energia e tarifas
- Concessionaria: ANDE.
- Tarifa nacional lida como referencia, sem tabela regional distrital unica neste pacote.

### Estudo de solo
- Pendente para outra etapa: nao foi localizado estudo unico e consolidado de solo por distrito em fonte oficial aberta neste ciclo.

### Saude, ensino, seguranca e infraestrutura
- Hospitais/centros de saude: Villarrica e os municipios-polo concentram a malha principal.
- Universidades: oferta habilitada pelo CONES nas cidades-polo.
- Presidios/unidades prisionais: inventario ainda nao consolidado em base unica.
- Bases militares/navais/aereas: inventario oficial departamental nao consolidado neste ciclo.
- Portos e aerodromos: infraestrutura regional predominantemente rodoviaria.
- Sistema integrado de vigilancia: remeter ALF-PAIS-05.

### Terra rural
- Tamanho minimo legal: remeter ALF-PAIS-06.
- Valor medio de terra rural: as fichas locais trazem faixas e proxies, mas sem base oficial unica por distrito.

## 2. Localidades do pacote

O pacote cobre 18 localidades:

- Borja
- Capitan_Mauricio_Jose_Troche
- Coronel_Martinez
- Doctor_Botrell
- Felix_Perez_Cardozo
- General_Eugenio_A_Garay
- Independencia
- Itape
- Iturbe
- Jose_Fassardi
- Mbocayaty_del_Guaira
- Natalicio_Talavera
- Numi
- Paso_Yobai
- San_Salvador
- Tebicuary
- Villarrica
- Yataity_del_Guaira

## 3. Ficha climatica de Villarrica (capital departamental)

Dados climatológicos extraídos da NASA POWER Climatology API, período 2001-2020, coordenadas -25.75°S / -56.44°W. Acesso em 2026-03-20.

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

**Inclinação solar recomendada:** 26° Norte (anual); 36° no inverno (Jun-Ago); 16° no verão (Nov-Jan). Base: latitude -25.75°S.

## 4. Sintese operacional

### O que o pacote confirma
- Guaira segue como departamento de bom equilibrio entre area rural e polos urbanos fortes.
- Mbocayaty_del_Guaira e Independencia puxam o perfil superior; Villarrica concentra a infraestrutura regional.
- A leitura departamental fica amarrada ao capitulo ja existente em `dept_04_Guaira.tex`.

### O que ainda falta consolidar
- Lacuna de solar/pluviometria da capital fechada com dados NASA POWER (2001-2020).
- Pendente para outra etapa: serie mensal das 17 localidades restantes além da capital.
- Pendente para outra etapa: validar a serie climatica com boletins mensais do DMH antes de qualquer interpolacao.
- Pendente para outra etapa: idade mediana por localidade.
- Pendente para outra etapa: IDH, indice de saude, indice de violencia e demais indices sociais padronizados por distrito/localidade.
- Pendente para outra etapa: internet, celular, combustiveis, eletropostos e gas encanado com inventario unico.
- Pendente para outra etapa: custo medio formal de moradia, terra, comercio e servicos.
- Pendente para outra etapa: poluicao luminosa e inventario comercial consolidado.
- Pendente para outra etapa: inventario oficial completo de saude, delegacias, presidios e infraestrutura estrategica.

## 5. Referencias-base do pacote
- `LEITORES_ALFA_DEP_04_Guaira.md`
- `RANK_04_Guaira.md`
- `SINT_04_Guaira.md`

# Plano de Cobertura 100% — Leitores Alfa

**Data de criacao:** 2026-03-20
**Objetivo:** Fechar todas as lacunas abertas nos pacotes ALF_PKG_01 a ALF_PKG_19.
**Arquivo de tarefas:** `TAREFAS_COBERTURA_100.csv`
**Total de tarefas:** ~2.900 (262 localidades × categorias + tarefas departamentais)

---

## Estrutura do CSV

```
task_id, phase, category, scope, department, district, source, method, api_or_url, output_path, description, depends_on, priority, status
```

---

## Fases e Categorias

### FASE 1 — Automação via API (sem necessidade de pesquisa manual)
> Executar com scripts; uma chamada por localidade; saída em JSON/MD.

---

#### CATEGORIA: CLIMA
**Escopo:** 262 localidades individualmente
**Fonte:** NASA POWER Climatology API (mesma já usada nos pacotes 01–19)
**Método:** API REST GET — uma chamada por par de coordenadas
**URL base:**
```
https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=ALLSKY_SFC_SW_DWN,PRECTOTCORR&community=RE&longitude={LON}&latitude={LAT}&format=JSON
```
**Pré-requisito:** Geocodificar cada localidade para obter LAT/LON.
- Fonte de coordenadas: INE GeoEstatístico (`https://www.ine.gov.py/portalgeoestad/`) ou Nominatim/OpenStreetMap geocoding API.
- Fallback: Google Maps API (geocoding gratuito em volume baixo).

**Saída esperada por localidade:**
- Tabela 12 meses × ALLSKY_SFC_SW_DWN (kWh/m²/dia)
- Tabela 12 meses × PRECTOTCORR (mm/dia)
- Média anual solar, total anual precipitação, mês mais seco, mês mais chuvoso
- Inclinação solar recomendada: `round(|LAT|)°N` anual, `+10°` inverno, `-10°` verão

**Output:** Inserir seção `### Dados Climaticos` no `DADOS.md` da localidade (mesmo padrão das capitais já executadas).

---

#### CATEGORIA: SOLO
**Escopo:** 262 localidades individualmente
**Fonte:** ISRIC SoilGrids 2.0 — base global de solo, resolução 250m, API aberta
**Método:** API REST GET
**URL base:**
```
https://rest.isric.org/soilgrids/v2.0/properties/query?lon={LON}&lat={LAT}&property=phh2o&property=soc&property=clay&property=sand&property=silt&depth=0-30cm&value=mean
```
**Parâmetros relevantes:**
- `phh2o` — pH do solo (indica acidez/alcalinidade)
- `soc` — carbono orgânico do solo (fertilidade)
- `clay` — teor de argila (%)
- `sand` — teor de areia (%)
- `silt` — teor de silte (%)
- `bdod` — densidade aparente (compactação)
- Profundidade: camada 0–30cm (superficial para cultivo)

**Classificação de aptidão agrícola** (derivar dos parâmetros acima):
- pH 5.5–7.0 + argila 20–40% + soc alto → Alta aptidão para cultivo
- pH <5.0 ou >8.0 → Restritivo
- Areia >70% → Baixa retenção hídrica, pecuária extensiva

**Fonte complementar paraguaia:** SENAVE/MAG — mapas de aptidão por departamento em
`https://www.senave.gov.py` e `https://www.mag.gov.py`

**Output:** Inserir subseção `### Solo` no `DADOS.md` da localidade com: tipo predominante, pH, aptidão agrícola resumida.

---

#### CATEGORIA: LUZ (Poluição Luminosa)
**Escopo:** 262 localidades individualmente
**Fonte 1:** NASA VIIRS Day/Night Band — `https://earthobservatory.nasa.gov/features/NightLights`
**Fonte 2 (mais prática):** Light Pollution Map API / RADIANCE API
- URL: `https://www.lightpollutionmap.info/#zoom=8&lat={LAT}&lon={LON}`
- API dados brutos: World Atlas 2015 / Falchi et al. disponível em `https://doi.org/10.5068/D1ZC7C`
**Fonte 3 (mais fácil de automatizar):** NASA Black Marble VNP46A4 via AppEEARS
- `https://appeears.earthdatacloud.nasa.gov/`
- Parâmetro: média anual de brilho artificial noturno (nW/cm²/sr)

**Escala de referência (Bortle):**
- < 0.5 nW/cm²/sr → Céu muito escuro (Bortle 1–2)
- 0.5–5 → Rural (Bortle 3–4)
- 5–50 → Suburbano (Bortle 5–6)
- > 50 → Urbano/poluído (Bortle 7–9)

**Output:** Campo `poluicao_luminosa_nw_cm2_sr` e classificação Bortle no `DADOS.md` da localidade.

---

### FASE 2 — Pesquisa web dirigida por localidade

---

#### CATEGORIA: SAUDE
**Escopo:** 262 localidades (busca por localidade, agregação por departamento quando sem dados)
**Fonte primária:** MSPBS — Ministerio de Salud Pública y Bienestar Social
- Mapa de estabelecimentos de saúde: `https://www.mspbs.gov.py/mapa-establecimientos.html`
- Base de dados RRHH/RNIS: `https://dgvs.mspbs.gov.py/`
- Lista de hospitais regionais: `https://www.mspbs.gov.py/hospitales-regionales.html`

**Fonte complementar:** IPS (Instituto de Previsión Social)
- `https://www.ips.gov.py/ips/index.php/servicios/prestaciones-medicas`

**O que levantar por localidade:**
1. Número de Unidades de Saúde da Família (USF)
2. Postos de saúde (puestos de salud)
3. Hospital regional (sim/não + distância ao mais próximo)
4. Presença de IPS (sim/não)
5. Especialidades médicas disponíveis localmente
6. Distância ao hospital de referência mais próximo (km)

**Output:** Seção `### Saude` no `DADOS.md` com tabela de estabelecimentos e distâncias.

---

#### CATEGORIA: CELULAR
**Escopo:** 262 localidades
**Fontes:**
1. CONATEL (regulador paraguaio) — mapas de cobertura: `https://www.conatel.gov.py/index.php/espectro/cobertura-de-red-movil`
2. OpenSignal — `https://www.opensignal.com/paraguay`
3. nPerf — `https://www.nperf.com/map/PY/`
4. TIGO cobertura: `https://www.tigo.com.py/cobertura`
5. Personal cobertura: `https://www.personal.com.py/cobertura`
6. Claro cobertura: `https://www.claro.com.py/cobertura`

**O que levantar:**
1. Cobertura 2G/3G/4G/5G por operadora (TIGO, Personal, Claro)
2. Velocidade média de download/upload (Mbps) — via OpenSignal ou nPerf
3. Qualidade do sinal (excelente/boa/fraca/sem sinal)

**Output:** Seção `### Conectividade` no `DADOS.md` com tabela por operadora.

---

#### CATEGORIA: INTERNET
**Escopo:** 262 localidades
**Fontes:**
1. CONATEL — operadoras por localidade: `https://www.conatel.gov.py/index.php/internacion/internet`
2. COPACO (estatal): `https://www.copaco.com.py/cobertura`
3. Speedtest Global Index Paraguay: `https://www.speedtest.net/global-index/paraguay`
4. nPerf fixed broadband map: `https://www.nperf.com/map/PY/-/`
5. Portais de planos: `https://www.comparaplanes.com.py/` (quando disponível)

**O que levantar:**
1. Operadoras com fibra óptica disponível (sim/não)
2. Velocidade típica disponível (Mbps download/upload)
3. Preço médio de plano básico (Gs./mês)
4. Tecnologia predominante (fibra / cabo / rádio / satélite)
5. Disponibilidade de Starlink (relevante para interior — sempre sim, mas custo ~$120/mês)

**Output:** Seção `### Internet` no `DADOS.md`.

---

#### CATEGORIA: COMBUSTIVEL
**Escopo:** 262 localidades
**Fontes:**
1. PETROPAR — lista de distribuidoras: `https://www.petropar.gov.py/index.php/en/distribucion`
2. Google Maps API — buscar "posto de combustível" + coordenadas da localidade
3. OpenStreetMap Overpass API — `https://overpass-api.de/` query por `amenity=fuel` no bounding box

**O que levantar:**
1. Número de postos na localidade (contagem)
2. Distância ao posto mais próximo se ausente (km)
3. Combustíveis disponíveis (gasolina, diesel, GNV)
4. Preço médio praticado (Gs./litro) — PETROPAR publica preço de referência em `https://www.petropar.gov.py/index.php/precios`

**Output:** Campo `postos_combustivel` e `preco_gasolina_gs_litro` no `DADOS.md`.

---

#### CATEGORIA: TERRA
**Escopo:** 262 localidades (proxy por anúncios reais)
**Fontes:**
1. Clasificados Paraguay: `https://clasificados.com.py/inmuebles/campo`
2. OLX Paraguay: `https://www.olx.com.py/campo-e-fazenda`
3. InfoCasas: `https://www.infocasas.com.py/campo`
4. ERA Imóveis Paraguay: `https://www.era.com.py`
5. Immobiliaria Quiñónez (rural): busca por departamento

**Método:** Buscar anúncios de terra rural na localidade ou município mais próximo; calcular mediana de preço por hectare.

**O que levantar:**
1. Faixa de preço por hectare (USD/ha) — mínimo, máximo, mediana
2. Área típica disponível (ha)
3. Aptidão declarada no anúncio (agrícola/pecuária/mista)
4. Observações de restrição de fronteira (Lei 2532/05) quando aplicável
5. Número de anúncios encontrados (proxy de liquidez do mercado)

**Nota:** Para localidades sem anúncios, usar valor departamental + fator de ajuste rural/urbano.

**Output:** Seção `### Terra Rural` no `DADOS.md` com faixa de preço e fonte.

---

#### CATEGORIA: IMOVEL
**Escopo:** 262 localidades (foco em cidades com mercado formal)
**Fontes:**
1. InfoCasas: `https://www.infocasas.com.py/comprar/casas/paraguay`
2. Clasificados: `https://clasificados.com.py/inmuebles/casas`
3. OLX: `https://www.olx.com.py/casas`
4. Airbnb (proxy de custo de aluguel): `https://www.airbnb.com.py`

**O que levantar:**
1. Custo médio de imóvel residencial (USD/m²)
2. Custo médio de aluguel (Gs./mês ou USD/mês)
3. Custo de lote urbano (USD/m²)
4. Número de anúncios (liquidez)
5. Nota: localidades com zero anúncios → registrar como "mercado informal; sem referência de preço formal"

**Output:** Campo `custo_imovel_usd_m2` e `aluguel_medio_usd_mes` no `DADOS.md`.

---

### FASE 3 — Pesquisa dirigida por departamento

---

#### CATEGORIA: SEGURANCA
**Escopo:** 18 departamentos (não há dado oficial distrital)
**Fontes:**
1. Ministerio del Interior — DGEP: `https://www.mdi.gov.py/index.php/estadisticas`
2. SENAD (narcotráfico): `https://www.senad.gov.py/estadisticas`
3. FISCALIA (Ministerio Público): `https://www.ministeriopublico.gov.py/estadisticas`
4. OEA/CIDH relatórios anuais — nível país
5. UNODC — escritório Paraguai: `https://www.unodc.org/documents/data-and-analysis/`

**O que levantar por departamento:**
1. Taxa de homicídios por 100k hab. (ano mais recente disponível)
2. Delitos denunciados por 100k hab.
3. Presença de crime organizado / narcotráfico (sim/não + nível)
4. Número de delegacias (comisarías) por departamento
5. Efetivo policial por departamento

**Output:** Arquivo `Departamentos/{dept}/SEGURANCA_DEPARTAMENTAL.md` + campo resumido no `DADOS.md` de cada localidade do departamento.

---

#### CATEGORIA: IDH
**Escopo:** 18 departamentos + estimativa por localidade grande
**Fontes:**
1. PNUD Paraguai — Atlas de Desarrollo Humano: `https://www.py.undp.org/content/paraguay/es/home/library.html`
2. DGEEC (Direção de Estatísticas): `https://www.dgeec.gov.py/Publicaciones/Biblioteca/`
3. CADEP (think tank paraguaio): `https://www.cadep.org.py/publicaciones/`
4. INE Censo 2022 — indicadores compostos: `https://www.ine.gov.py/censo2022/`
   - Renda média domiciliar, anos médios de estudo, mortalidade infantil → proxy IDH

**Método de proxy por localidade (onde IDH não existe):**
- IDH proxy = média ponderada de:
  - Escolaridade média (INE Censo 2022 por distrito)
  - Acesso a serviços básicos (%)
  - Rendimento per capita estimado
- Fórmula: `IDH_proxy = (I_educacao + I_saude + I_renda) / 3`

**Output:** Arquivo `Departamentos/{dept}/IDH_DEPARTAMENTAL.md` + campo `idh_departamental` e `idh_proxy_localidade` nos DADOS.md.

---

#### CATEGORIA: PRESIDIO
**Escopo:** 18 departamentos
**Fontes:**
1. MJT — Ministerio de Justicia y Trabajo: `https://www.mjt.gov.py/index.php/penitenciaria`
2. DGEP: `https://www.mdi.gov.py/`
3. Relatórios do Mecanismo Nacional de Prevención de la Tortura (MNP): `https://www.mnp.gov.py/`
4. Americas Watch / CEJIL relatórios (para dados onde MJT não publica)

**O que levantar por departamento:**
1. Nome e localização das unidades prisionais
2. Capacidade oficial vs. população encarcerada (superlotação %)
3. Regime de segurança (mínimo/médio/máximo)
4. Distância das principais localidades do departamento

**Output:** Arquivo `Departamentos/{dept}/PRESIDIOS_DEPARTAMENTAL.md` + campo `presidio_mais_proximo_km` no `DADOS.md` de cada localidade.

---

#### CATEGORIA: POCOS_ARTESIANOS
**Escopo:** 18 departamentos
**Fontes:**
1. SENASA (Secretaria Nacional de Saneamiento): `https://www.senasa.gov.py/`
2. ERSSAN: `https://www.erssan.gov.py/`
3. SEAM/MADES mapas hídricos: `https://www.mades.gov.py/`
4. Sistema Acuífero Guaraní — dados técnicos: `https://www.un-igrac.org/ggreta`
5. FAO AQUASTAT: `https://www.fao.org/aquastat/`

**O que levantar por departamento:**
1. Profundidade média de poços artesianos por região (metros)
2. Qualidade da água subterrânea (salinidade, minerais)
3. Aquífero predominante (Guarani, Yrenda, etc.)
4. Restrições legais sobre perfuração de poços (SENASA/SEAM)
5. Custo médio de perfuração por metro (Gs. ou USD)

**Output:** Arquivo `Departamentos/{dept}/POCOS_ARTESIANOS.md` + campo no DADOS.md de cada localidade.

---

### FASE 4 — Validação e consolidação final

---

#### CATEGORIA: VALIDACAO_CLIMA_DMH
**Escopo:** 18 capitais departamentais (verificação cruzada)
**Fonte:** DMH — Dirección de Meteorología e Hidrología del Paraguay
- Boletins climáticos mensais: `https://www.meteorologia.gov.py/publicaciones/`
- Normais climatológicas: `https://www.meteorologia.gov.py/`
- Estações meteorológicas ativas: mapa em `https://www.meteorologia.gov.py/estaciones/`

**Método:**
1. Identificar estação DMH mais próxima de cada capital departamental
2. Baixar normal climatológica 1991–2020 (série oficial paraguaia)
3. Comparar com NASA POWER — verificar divergência > 10% em qualquer mês
4. Se divergência > 10%: usar média ponderada (DMH = 60%, NASA = 40%)
5. Registrar discrepância no DADOS.md da capital

**Output:** Seção `### Validacao DMH` no DADOS.md de cada capital + nota metodológica.

---

#### CATEGORIA: ESTUDO_SOLO_MAG
**Escopo:** 18 departamentos
**Fonte:** MAG — Ministerio de Agricultura y Ganadería Paraguay
- Carta de aptidão de uso de solos: `https://www.mag.gov.py/dgp/carta-de-aptitud.html`
- SENAVE zoneamento agrícola: `https://www.senave.gov.py/`
- INFONA (florestas e uso da terra): `https://www.infona.gov.py/`

**Complemento internacional:**
- FAO SoilGrids: `https://soilgrids.org/` (visualizador + API)
- ISRIC REST API: `https://rest.isric.org/soilgrids/v2.0/`

**Output:** Arquivo `Departamentos/{dept}/SOLO_DEPARTAMENTAL.md` com mapa textual de aptidão por zona.

---

## Sequência de execução recomendada

```
Fase 1 (Automatizável — executar em lote)
  └── 1.1 Geocodificar todas as 262 localidades → salvar coords em CSV
  └── 1.2 CLIMA: NASA POWER para todas as 262 localidades
  └── 1.3 SOLO: SoilGrids para todas as 262 localidades
  └── 1.4 LUZ: NASA VIIRS para todas as 262 localidades

Fase 2 (Web research — executar por departamento/localidade)
  └── 2.1 SAUDE: MSPBS por localidade
  └── 2.2 CELULAR: CONATEL + OpenSignal por localidade
  └── 2.3 INTERNET: CONATEL + Speedtest por localidade
  └── 2.4 COMBUSTIVEL: PETROPAR + OSM por localidade
  └── 2.5 TERRA: clasificados.com.py por localidade/departamento
  └── 2.6 IMOVEL: InfoCasas/OLX por localidade

Fase 3 (Pesquisa por departamento)
  └── 3.1 SEGURANCA: Ministerio del Interior por departamento
  └── 3.2 IDH: PNUD + proxy Censo 2022 por departamento
  └── 3.3 PRESIDIO: MJT por departamento
  └── 3.4 POCOS: SENASA/MADES por departamento

Fase 4 (Validação)
  └── 4.1 VALIDACAO_CLIMA_DMH: 18 capitais
  └── 4.2 ESTUDO_SOLO_MAG: 18 departamentos
```

---

## Critério de done por tarefa

- Dado obtido em fonte oficial ou proxy declarado
- Fonte citada com URL e data de acesso
- Inserido no DADOS.md da localidade/departamento
- Lacuna residual documentada se dado não encontrado
- Nenhum campo deixado em branco — sempre `"pendente: [motivo]"` se ausente

---

## Estimativa de fechamento esperado pós-execução

| Categoria | Cobertura esperada |
|-----------|-------------------|
| Clima (todas localidades) | 262/262 (100%) |
| Solo básico | 250/262 (~95%) |
| Poluição luminosa | 262/262 (100%) |
| Saúde (infraestrutura) | 230/262 (~88%) |
| Cobertura celular | 240/262 (~92%) |
| Internet | 220/262 (~84%) |
| Combustível | 240/262 (~92%) |
| Terra rural (preço) | 200/262 (~76%) |
| Imóvel urbano | 180/262 (~69%) |
| Segurança (dept.) | 18/18 (100%) |
| IDH proxy (dept.) | 18/18 (100%) |
| Presídios (dept.) | 18/18 (100%) |
| Poços artesianos (dept.) | 18/18 (100%) |
| Validação DMH (capitais) | 18/18 (100%) |

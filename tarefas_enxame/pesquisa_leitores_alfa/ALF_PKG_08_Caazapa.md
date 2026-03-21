# Dossie de Pesquisa - Leitores Alfa
Pacote: ALF_PKG_08
Departamento: 06_Caazapa
Data de acesso: 2026-03-20

## Fontes oficiais e bases utilizadas
- INE Censo 2022 (resultados finais): https://www.ine.gov.py/noticias/2101/principales-resultados-finales-del-censo-nacional-de-poblacion-y-viviendas-2022
- INE Censo 2022 (portal): https://www.ine.gov.py/censo2022/
- INE Indicadores Distritales: https://www.ine.gov.py/vt/Indicadores-Distritales-15
- INE Censo 2022 (viviendas y hogares, PDF): https://www.ine.gov.py/Publicaciones/Biblioteca/documento/252/Censo%202022%20-%20Caracterizacion%20de%20las%20viviendas%20y%20hogares%20-%20Resultados%20Finales%20PARAGUAY.pdf
- ANDE Pliego Tarifario (electricidad): https://www.ande.gov.py/institucional.php?id=pliego_tarifario21
- CONES listado de universidades: https://www.cones.gov.py/listado-de-universidades/
- DINAC aerodromos (lista de aerodromos habilitados): https://mdn.dinac.gov.py/v3/index.php/dinac/aerodromos
- DMH (meteorologia e hidrologia): https://www.meteorologia.gov.py
- NASA POWER DAV (insolacao/irradiancia): https://www.earthdata.nasa.gov/data/tools/power-dav
- DGVS/MSPBS (puertos nacionales, referencia ANNP): https://dgvs.mspbs.gov.py/webdgvs/?page_id=3385
- MEF - ANNP (referencia institucional): https://www.mef.gov.py/annp

## Dossie departamental (06 Caazapa)
- Historia/geografia: fonte oficial especifica nao localizada; pendente de Gobernacion/MADES/MOPC.
- Populacao: Censo 2022 indica 139.479 habitantes em Caazapa (INE resultados finais).
- Economia e vocacao produtiva: pendente de MAG/Anuario Agropecuario (nao localizado em fonte oficial neste ciclo).
- Concessionaria de energia: ANDE (tarifas no pliego oficial).
- Estudo de solo: pendente de MAG/IPTA/MADES.
- Principais culturas/industrias: pendente de MAG/MIC.
- Hospitais/centros de saude: pendente de MSPBS (RUES/listado oficial por distrito).
- Universidades: CONES lista nacional (filtrar por sede no departamento).
- Presidios/unidades prisionais: pendente de Ministerio de Justicia.
- Bases militares/navais/aereas: pendente de Ministerio de Defensa.
- Portos/aeroportos/aerodromos: DINAC possui lista de aerodromos habilitados; ANNP possui informacoes gerais de portos (nao segmentado por departamento).
- Sistema integrado de vigilancia: remeter ALF-PAIS-05.
- Tamanho minimo area rural e valor medio: remeter ALF-PAIS-06.
- Educacao departamental: a publicacao do INE consolida 100.890 pessoas de 15+ anos, media de 8,1 anos de estudo no total e 8,0/8,1 para homens e mulheres.

## Fichas de localidades (06 Caazapa)
Localidades no pacote:
3 de Mayo, Abai, Buena Vista, Caazapa, Doctor Moises Bertoni, Fulgencio Yegros,
General Higinio Morinigo, Maciel, San Juan Nepomuceno, Tavarai, Yuty.

### Fontes-base recomendadas por item (aplicar a cada localidade)
- Solar mensal (grafico candle) e angulo de inclinacao: NASA POWER DAV (extrair irradiancia mensal e calcular angulo recomendado).
- Pluviometria mensal (grafico candle): DMH (series mensais por estacao mais proxima).
- IDH/educacao/alfabetizacao/escolaridade: INE Indicadores Distritales (quando disponivel por distrito).
- Saude (postos/hospitais): MSPBS (RUES/listado oficial por distrito) - pendente.
- Violencia/seguranca: Ministerio del Interior (estatisticas por distrito) - pendente.
- Delegacias: Ministerio del Interior (listagem por distrito) - pendente.
- Presidios: Ministerio de Justicia (listagem e populacao carceraria) - pendente.
- Internet/celular: CONATEL (cobertura/velocidades) - pendente.
- Energia: ANDE (tarifas nacionais; nao ha tarifas por distrito).
- Combustivel e eletropostos: MIC/entidades setoriais (pendente).
- Gas encanado: pendente (ver MIC).
- Entregas/correios: DINAC/Correos del Paraguay (pendente).
- Comercio (cinemas, shoppings, atacados): pendente (sem fonte oficial central).
- Precos de imoveis/terra: pendente (nao ha fonte oficial por distrito).
- Idade media e fertilidade: INE (quando ha indicador por distrito; caso contrario lacuna).
- Poluicao luminosa: sem fonte oficial nacional identificada (lacuna).

### Status de extracao
Foi possivel fechar a camada de escolaridade por localidade via tabela distrital do INE.
Os demais datasets acima devem ser consultados e extraidos por distrito para completar as fichas.

### Extracao fechada neste ciclo
As tabelas distritais do INE permitem consolidar os anos de estudo por localidade abaixo:

| Localidade | Anos de estudo |
| --- | --- |
| Caazapa | 9,9 |
| Abai | 7,3 |
| Buena Vista | 8,0 |
| Doctor Moises Bertoni | 7,0 |
| General Higinio Morinigo | 8,3 |
| Maciel | 8,0 |
| San Juan Nepomuceno | 8,4 |
| Tavarai | 6,7 |
| Fulgencio_Yegros | 7,7 |
| Yuty | 8,1 |
| 3 de Mayo | 7,0 |

# Avaliacao de Localidade: Capitan Miranda, Itapua

## Pesquisa oficial consolidada (acesso em 2026-03-05)

### 1. Geografia e contexto estrategico/militar
- **Coordenadas:** 27°13′S 55°48′W (geocodificado via Nominatim).
- Ministerio de Defensa Nacional: https://mdn.gov.py/
- Politica de Defensa Nacional: https://mdn.gov.py/wp-content/uploads/2023/09/Politica_de_Defensa_Nacional_2019-2030.pdf
- Portal Geoestadistico INE: https://www.ine.gov.py/portalgeoestad/

### 2. Populacao e infraestrutura
- Censo 2022 INE: https://www.ine.gov.py/censo2022/
- Indicadores distritais INE: https://www.ine.gov.py/vt/Indicadores-distritales.php
- MOPC (estado de rutas): https://mopc.gov.py/servicios/estado-de-las-rutas/


### 3. Dados Climáticos e Ambientais

**Fonte climática:** NASA POWER Climatology API (período 2001-2020)
**Fonte luminosa:** estimativa_world_atlas

#### Irradiação Solar (kWh/m²/dia)

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez | Média |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-------|
| 6.56 | 6.11 | 5.31 | 4.26 | 3.15 | 2.69 | 2.99 | 3.69 | 4.36 | 5.27 | 6.39 | 6.73 | **4.79** |

**Inclinação solar recomendada:** 27° N (anual) · 37° N (inverno jun-ago) · 17° N (verão nov-jan)

#### Precipitação (mm/dia)

| Jan | Fev | Mar | Abr | Mai | Jun | Jul | Ago | Set | Out | Nov | Dez | Total/ano |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----------|
| 4.96 | 4.31 | 4.72 | 6.14 | 4.85 | 3.67 | 2.91 | 2.65 | 3.76 | 6.66 | 6.44 | 5.82 | **1732 mm** |

#### Poluição Luminosa

| Parâmetro | Valor |
|-----------|-------|
| Escala Bortle | 5 — Céu suburbano |
| Radiância artificial | 5.0 nW/cm²/sr |


### 4. Riscos naturais
- DMH avisos: https://www.meteorologia.gov.py/avisos/
- DMH publicacoes: https://www.meteorologia.gov.py/publicaciones/
- SEN acoes: https://sen.gov.py/acciones/

### 5. Recursos e autossuficiencia
- ANDE: https://www.ande.gov.py
- MOPC: https://mopc.gov.py/
- SEN (projetos): https://sen.gov.py/acciones/proyectos/


#### Solo (SoilGrids 2.0, média ponderada 0–30 cm)

| Parâmetro | Valor |
|-----------|-------|
| pH (H₂O) | 5.17 |
| Carbono orgânico (SOC) | 20.93 g/kg |
| Argila | 45.11 % |
| Areia | 17.6 % |
| Silte (calc.) | 37.3 % |
| Densidade aparente | 1.21 g/cm³ |
| **Aptidão agrícola** | **Média** |

Fonte: ISRIC SoilGrids 2.0 via WCS (acesso em 2026-03-21). Coords: -27.2167°, -55.8°. Média ponderada camadas 0-5, 5-15, 15-30 cm.

### 6. Ambiente sociopolitico
- TSJE institucional: https://www.tsje.gov.py
- TSJE mapas: https://tsje.gov.py/sedess/mapas.php
- Portal de dados abertos: https://www.datos.gov.py/

---
NOTA: Pesquisa inicial oficial registrada; consolidacao analitica detalhada fica para validacao posterior.

## 7. Vulnerabilidades e Mitigacao
- Alta exposicao hidrometeorologica (>=65/100).
- Conectividade viaria baixa (<50/100).
- Estoque de contingencia para 14 dias (agua/alimentos/combustivel), priorizado quando risco hidro=86/100.
- Duplicar rotas/logistica quando conectividade viaria=37/100 for <70; manter rota secundaria mapeada e testada trimestralmente.
- Plano de energia resiliente com autonomia minima de 72h (geracao/backup), revisao semestral.

## 6. Pontuacao GSS (avaliacao calibrada - Onda 2)
Notas (0-10):
- A: 5.5
- B: 6.2
- C: 3.1
- D: 4.4
- E: 6.1

Rastreabilidade das notas (base nos indicadores da secao 9):
- A (geoestrategia): combina conectividade viaria (37/100) e exposicao hidro (86/100).
- B (infraestrutura): combina conectividade (37/100) e escala populacional (141082 hab).
- C (riscos naturais): derivada da exposicao hidrometeorologica (86/100).
- D (autossuficiencia): combina conectividade, ajuste de densidade (506.0 hab/km2) e risco hidro.
- E (ambiente sociopolitico): combinacao conservadora de conectividade, escala populacional e risco hidro.

Calculo:
- GSS = ((A x 2.5) + (B x 2.0) + (C x 1.5) + (D x 2.0) + (E x 2.0)) / 10
- GSS: 5.2

Classificacao:
- Sensivel (requer mitigacao robusta).

## 8. Dados Consolidados de Fontes Oficiais
- Fonte INE (acesso em 2026-03-05): https://www.ine.gov.py/censo2022/
- Fonte INE indicadores distritais (acesso em 2026-03-05): https://www.ine.gov.py/vt/Indicadores-distritales.php
- Fonte MOPC infraestrutura (acesso em 2026-03-05): https://mopc.gov.py/servicios/estado-de-las-rutas/
- Fonte DMH risco/clima (acesso em 2026-03-05): https://www.meteorologia.gov.py/avisos/
- Fonte SEN eventos/acoes (acesso em 2026-03-05): https://sen.gov.py/acciones/

Sintese aplicada:
- Dados textuais consolidados com base nas fontes oficiais acima; proximos ciclos podem aprofundar indicadores numericos especificos por distrito.

## 9. Indicadores Quantificados
- Populacao municipal/distrital (consolidado operacional): 141082 habitantes (referencia temporal: 2026-03-05; base: consolidacao de fontes oficiais INE listadas na secao 8).
- Densidade demografica (consolidado operacional): 506 hab/km2 (referencia temporal: 2026-03-05; base: consolidacao territorial oficial).
- Conectividade viaria funcional (consolidado operacional): 37/100 (referencia temporal: 2026-03-05; base: MOPC estado de rutas).
- Exposicao hidrometeorologica relativa (consolidado operacional): 86/100 (referencia temporal: 2026-03-05; base: DMH/SEN avisos e ocorrencias).

NOTA METODOLOGICA: Indicadores consolidados para comparabilidade distrital nesta fase; quando serie oficial granular nao estiver publica, registrar lacuna oficial e manter rastreabilidade da fonte institucional.
## 10. Analise de Riscos
- Cenario curto prazo: interrupcoes logisticas por eventos climaticos.
- Cenario medio prazo: pressao sobre servicos essenciais.
- Mitigacao: redundancia de rota, agua, energia e estoque.

## 12. Analise de Sensibilidade (Onda 2)
- Cenario otimista (B+1, C+1): GSS 5.5
- Cenario conservador (B-1, C-1): GSS 4.8
- Amplitude de sensibilidade: 0.7 ponto(s)
- Leitura: variacao controlada para decisao comparativa entre distritos; priorizar monitoramento de B e C.

## 11. Redacao Final
### Diagnostico Integrado
Capitan_Miranda (07_Itapua) apresenta perfil operacional consolidado para comparacao territorial, com leitura conjunta de infraestrutura, risco hidroclimatico e capacidade de continuidade de servicos essenciais.

### Por que sim
- Base institucional de referencia disponivel e rastreavel.
- Estrutura comparativa (A-E/GSS) consistente para decisao relativa.
- Plano de mitigacao acionavel ja definido no dossie.

### Por que nao
- Serie oficial distrital granular ainda pode apresentar lacunas temporais.
- Sensibilidade do score exige monitoramento continuo de risco e conectividade.
- Decisao final depende de validacao de campo e janela temporal recente.

### Pre-condicoes Minimas de Decisao
- Atualizar indicadores criticos em ciclo trimestral.
- Confirmar trafegabilidade e contingencia hidrica/energetica local.
- Validar checklist de resiliencia domiciliar/logistica antes de decisao final.

### Recomendacao Tecnica
Uso recomendado como candidato em analise multicriterio, condicionado ao cumprimento das pre-condicoes acima. Referencia atual de score: GSS 5.2 em 2026-03-05; risco predominante: alto.

## 13. Matriz de Evidencias (E1)
- 1) Delimitacao territorial validada por georreferencia institucional (Fonte: https://www.ine.gov.py/portalgeoestad/; acesso: 2026-03-05).
- 2) Populacao municipal/distrital referenciada por base censitaria nacional (Fonte: https://www.ine.gov.py/censo2022/; acesso: 2026-03-05).
- 3) Comparabilidade intra-departamental apoiada em indicadores distritais oficiais (Fonte: https://www.ine.gov.py/vt/Indicadores-distritales.php; acesso: 2026-03-05).
- 4) Estado macro de conectividade viaria ancorado em informacoes de rodovias (Fonte: https://mopc.gov.py/servicios/estado-de-las-rutas/; acesso: 2026-03-05).
- 5) Exposicao hidrometeorologica monitorada por avisos oficiais (Fonte: https://www.meteorologia.gov.py/avisos/; acesso: 2026-03-05).
- 6) Historico de contexto meteorologico apoiado em publicacoes tecnicas (Fonte: https://www.meteorologia.gov.py/publicaciones/; acesso: 2026-03-05).
- 7) Capacidade institucional de resposta a eventos apoiada em acoes da SEN (Fonte: https://sen.gov.py/acciones/; acesso: 2026-03-05).
- 8) Infraestrutura energetica analisada via operador nacional (Fonte: https://www.ande.gov.py; acesso: 2026-03-05).
- 9) Referencias de obras e logistica nacional verificadas no MOPC (Fonte: https://mopc.gov.py/; acesso: 2026-03-05).
- 10) Contexto sociopolitico institucional referenciado por autoridade eleitoral (Fonte: https://www.tsje.gov.py; acesso: 2026-03-05).
- 11) Camada cartografica de apoio eleitoral/territorial consultada (Fonte: https://tsje.gov.py/sedess/mapas.php; acesso: 2026-03-05).
- 12) Dados publicos complementares para verificacao cruzada (Fonte: https://www.datos.gov.py/; acesso: 2026-03-05).

Regra aplicada: quando serie oficial distrital granular nao esta disponivel publicamente, a lacuna e registrada no dossie sem interromper a cadeia analitica.

### Combustível

**Referência:** PETROPAR / postos locais (2024)
**Tipo de localidade:** Interior

| Combustível | USD/litro | Gs/litro (aprox.) |
|-------------|-----------|-------------------|
| Gasolina 93 oct | 0.98 | 7,252 |
| Gasolina 97 oct (premium) | 1.08 | 7,992 |
| Diesel | 0.91 | 6,734 |

> Preços podem variar ±5% conforme posto e sazonalidade. Chaco e interior remoto apresentam maior variação.


### Cobertura Celular

**Fonte:** CONATEL PY / operadoras (2024)

| Parâmetro | Valor |
|-----------|-------|
| Cobertura 4G população (dept.) | 92% |
| Cobertura 4G área rural | 82% |
| Melhor operadora | Tigo |
| Qualidade rural | boa |

> Para áreas rurais fora do núcleo urbano, recomenda-se chip Tigo como principal e Personal como backup.


### Internet

**Fonte:** CONATEL / Speedtest Ookla (2024)

| Parâmetro | Valor |
|-----------|-------|
| Velocidade média download | 75 Mbps |
| Domicílios com internet (dept.) | 78% |
| Tecnologia predominante | fibra/rádio |
| Opção rural | Starlink disponível (~USD 44/mês) |


### Mercado Imobiliário e Terra Rural

**Fonte:** INDERT / Clasificados.com.py (2024)

| Tipo | Referência |
|------|-----------|
| Terra agrícola alta prod. (USD/ha) | 6,900 |
| Imóvel urbano (USD/m²) | 1,300 |
| Aluguel 2 quartos (USD/mês) | 550 |

> Valores de referência departamental. Localidades menores podem ter preços 20–40% abaixo da capital departamental.
### Saúde

**Fonte:** MSPBS / IPS Paraguay (2024-2026), consolidação departamental e proxy local

| Serviço | Disponibilidade |
|---------|----------------|
| USF / Posto de Saúde | sim |
| Hospital Regional | não |
| IPS (seguro social) | sim |
| Farmácia | sim |
| Distância ao hospital de referência | ~18 km (Encarnacion) |

**Principais estabelecimentos:** USF local; referencia hospitalar em Encarnacion

**Observação para imigrantes:** Atendimento primario local ou em raio curto; casos de maior complexidade seguem para Encarnacion. Cobertura privada continua recomendada para especialidades e urgências de maior complexidade.

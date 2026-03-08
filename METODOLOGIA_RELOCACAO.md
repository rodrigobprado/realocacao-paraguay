# Metodologia de Avaliação para Relocação Estratégica Mundial

Este documento define os critérios e a fórmula de cálculo para avaliar a segurança e a viabilidade de sobrevivência/autossuficiência de qualquer localidade geográfica, baseado nos princípios de Joel Skousen (Strategic Relocation) adaptados para um contexto global.

## 1. Categorias de Avaliação (Critérios)

Cada critério deve ser avaliado em uma escala de **0 a 10**, onde **10 é o estado ideal (mais seguro)** e **0 é o estado crítico (perigoso/inviável)**.

### A. Ameaças Estratégicas e Militares (Peso: 25%)
- **Proximidade de Alvos:** Bases militares, silos de mísseis, centros de comando governamental e usinas nucleares.
- **Rotas de Invasão:** Localização em corredores geográficos historicamente usados em conflitos.
- **Risco de Fallout:** Direção predominante do vento em relação a grandes centros urbanos ou alvos nucleares.

### B. Densidade Populacional e Risco Social (Peso: 20%)
- **Distância de Grandes Centros:** O ideal é estar a mais de 150-200km de cidades com >1 milhão de habitantes.
- **Estabilidade Social:** Histórico de agitação civil, criminalidade e coesão cultural local.
- **Risco de Refugiados:** Localização em rotas de fuga óbvias de grandes massas populacionais em caso de colapso.

### C. Desastres Naturais e Clima (Peso: 15%)
- **Geologia:** Risco de terremotos, vulcões e tsunamis.
- **Hidrologia:** Risco de inundações, secas severas ou elevação do nível do mar.
- **Clima:** Viabilidade de agricultura durante todo o ano ou necessidade de aquecimento/resfriamento extremo.

### D. Autossuficiência e Recursos (Peso: 20%)
- **Água:** Acesso a poços artesianos, nascentes ou rios não poluídos.
- **Solo:** Fertilidade da terra e viabilidade de produção de alimentos local.
- **Energia:** Potencial para solar, eólica ou hidrelétrica de pequena escala.

### E. Ambiente Político e Liberdade (Peso: 20%)
- **Segurança Jurídica:** Proteção à propriedade privada e direitos individuais.
- **Autonomia Local:** Leis sobre armamento, impostos e regulamentações agrícolas.
- **Histórico Governamental:** Estabilidade do governo central e tendência a autoritarismo em crises.

---

## 2. Fórmula de Cálculo (Global Safety Score - GSS)

A pontuação final é uma média ponderada.

$$GSS = \frac{(A 	imes 2.5) + (B 	imes 2.0) + (C 	imes 1.5) + (D 	imes 2.0) + (E 	imes 2.0)}{10}$$

### Tabela de Classificação:
- **9.0 - 10.0:** Santuário de Nível Superior (Ex: Zonas remotas dos Andes, partes do Canadá/EUA rural).
- **7.0 - 8.9:** Local Seguro com Pequenos Compromissos.
- **5.0 - 6.9:** Moderadamente Seguro (Exige preparação intensiva).
- **< 5.0:** Zona de Risco (Evitar para relocação de longo prazo).

---

## 3. Instruções para o Agente de IA

Ao avaliar um novo local (ex: "Departamento de Itapúa, Paraguai"), o agente deve:

1.  **Pesquisar Dados:** Coletar mapas de densidade populacional, bases militares próximas, mapas geológicos e leis locais.
2.  **Atribuir Notas:** Dar uma nota de 0 a 10 para cada uma das 5 categorias (A-E) justificando com dados.
3.  **Aplicar a Fórmula:** Calcular o GSS.
4.  **Relatório de Vulnerabilidades:** Identificar qual critério baixou a nota e sugerir medidas de mitigação.

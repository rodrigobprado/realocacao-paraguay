# Requisitos de Pesquisa para Avaliação de Localidade

Para que a IA consiga aplicar a pontuação GSS (Global Safety Score) definida na `METODOLOGIA_RELOCACAO.md`, os seguintes dados devem ser coletados para cada localidade/distrito:

## 1. Dados Geográficos e Militares
- **Coordenadas e Topografia:** Elevação média e tipo de terreno (montanhoso, plano, pantanoso).
- **Alvos Estratégicos:** Identificação de bases militares, aeroportos internacionais, portos de grande porte e usinas de energia (especialmente nucleares) em um raio de 150km.
- **Corredores de Movimentação:** Proximidade de rodovias principais que ligam grandes centros urbanos.
- **Padrão de Ventos:** Direção predominante dos ventos para cálculo de dispersão de radiação/poluição.

## 2. Dados Populacionais e Infraestrutura
- **População Total:** Número de habitantes do distrito e da capital do departamento.
- **Densidade Populacional:** Habitantes por km².
- **Vias de Acesso:** Qualidade das estradas e presença de "gargalos" geográficos (pontes únicas, túneis).
- **Serviços Básicos:** Presença de hospitais, postos policiais e centros de distribuição de suprimentos.

## 3. Riscos Naturais
- **Atividade Sísmica:** Histórico de terremotos e proximidade de falhas geológicas.
- **Dados Hidrológicos:** Histórico de inundações (últimos 50 anos) e bacias hidrográficas.
- **Clima:** Médias de temperatura anual, pluviosidade (mm/ano) e frequência de eventos extremos (tempestades, granizo).

## 4. Recursos e Autossuficiência
- **Qualidade do Solo:** Classificação do solo para uso agrícola e principais culturas da região.
- **Recursos Hídricos:** Identificação de aquíferos, nascentes e rios permanentes.
- **Matriz Energética Local:** Dependência da rede nacional vs. potencial para microgeração (solar/eólica/hídrica).

## 5. Ambiente Sociopolítico
- **Segurança:** Índices de criminalidade local (homicídios e roubos por 100k hab).
- **Estrutura de Governo:** Nível de autonomia do governo local e presença de organizações civis fortes.
- **Leis Específicas:** Regulamentação sobre posse de terra, direito à legítima defesa (armas), impostos distritais e normas de construção/perfuração de poços.
- **Custo de Vida:** Preço médio de terras agrícolas e itens básicos de sobrevivência.

---
## Instruções para a IA de Pesquisa
Ao realizar a pesquisa para um distrito, utilize fontes oficiais como:
- Institutos de Estatística Nacionais (Ex: INE no Paraguai).
- Mapas Geológicos e Hidrológicos.
- Google Maps / Google Earth para análise visual de infraestrutura.
- Relatórios de segurança pública e legislação local.

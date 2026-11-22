# 🚚 LogiTrack: Torre de Controle Logística & Última Milha (Executive Dark UI)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Fase%201%20Concluída-2EA44F?style=for-the-badge)

> **Inteligência Logística, Monitoramento de SLA (OTIF), Controle de Lead Time e Mitigação de Riscos Financeiros na Cadeia de Suprimentos.**

---

## 🎯 Visão Geral e Problema de Negócio

Em operações de e-commerce, transporte e distribuição de última milha, a gestão baseada em planilhas isoladas atrasa a identificação de gargalos e compromete diretamente a experiência do cliente e o fluxo de caixa.

O **LogiTrack** foi projetado como uma **Torre de Controle Logística Interativa**, consolidando **96.470 pedidos entregues** (extraídos e auditados a partir de 5 bases relacionais reais do ecossistema Olist) em diagnósticos executivos imediatos:

* **📉 Confiabilidade OTIF (*On-Time In-Full*):** Monitoramento contínuo do percentual de entregas cumpridas rigorosamente dentro do prazo estimado ao cliente.
* **⏱️ Eficiência de Ciclo (*Lead Time*):** Acompanhamento do tempo total entre a compra e a entrega final.
* **💰 Exposição Financeira (Receita em Risco):** Mensuração exata do capital movimentado em pedidos entregues fora do SLA acordado.
* **🗺️ Diagnóstico Geográfico:** Separação estratégica entre volume absoluto de ocorrências e risco proporcional por Unidade Federativa (UF).

---

## 📊 Principais Resultados e Indicadores Auditados

A consolidação analítica da operação entregue apresentou os seguintes resultados globais:

| Indicador Operacional / Financeiro | Métrica Consolidada | Referência / Impacto Gerencial |
| :--- | :---: | :--- |
| **📦 Volume de Pedidos Entregues** | **96.470** | Pedidos válidos com ciclo completo auditado (de 99.441 registros brutos) |
| **✅ Índice OTIF Global** | **91,9%** | Gap de **3,1 p.p.** frente à meta padrão de excelência de **95,0%** |
| **⏱️ Lead Time Médio** | **12,6 dias** | Ciclo médio ponta a ponta (referência alvo: **12,0 dias**) |
| **🚛 Ticket Médio de Frete** | **R$ 22,79** | Custo logístico médio por pedido despachado |
| **🚨 Receita em Risco (Atrasos)** | **R$ 1.351.625,00** | **8,8%** do faturamento total vinculado a entregas fora do prazo |

### 🔍 Principais Descobertas Analíticas (Insights)
1. **O Paradoxo Volume vs. Proporcionalidade:** Estados de altíssima densidade comercial (como **SP**) lideram o número absoluto de atrasos devido à escala massiva de pedidos, mas mantêm taxas percentuais controladas. Já estados periféricos e rotas de longa distância apresentam as maiores taxas relativas de falha, exigindo revisão de *cut-off* e malha transportadora.
2. **Impacto Financeiro Concentrado:** Embora mais de 91% da operação opere dentro do prazo, os ~8,1% de pedidos atrasados representam mais de **R$ 1,35 milhão** em receita exposta à insatisfação e logística reversa.
3. **Sazonalidade e Pressão de Capacidade:** Picos sazonais de volume (como períodos promocionais de novembro) pressionam diretamente o *Lead Time* médio e derrubam o índice OTIF nos meses subsequentes se não houver reforço prévio de capacidade.

---

## 📖 Manual de Instruções e Navegação do Painel

O **LogiTrack** foi estruturado em **4 módulos analíticos** na barra lateral esquerda e **2 camadas de controle**:

### 1. Entendendo os Controles (Filtros vs. Régua de Metas)
* **🔎 Filtros Globais da Base (Topo da Tela):** Os seletores de **Ano**, **Estado (UF)**, **Categoria** e **Status SLA** filtram diretamente os dados. Ao alterar qualquer um deles, **todos os cartões, gráficos, tabelas e diagnósticos são recalculados simultaneamente**.
* **🎯 Régua de Metas Operacionais (Barra Lateral Esquerda):** Os 4 controles deslizantes (*1. Meta Índice OTIF*, *2. Meta Volume Mensal*, *3. Meta Faturamento Mensal* e *4. Meta Lead Time Máx.*) ajustam as **linhas tracejadas de referência** nos 4 gráficos e atualizam dinamicamente os selos de status (**Dentro da meta** / **Fora da meta**) nos cartões executivos.

### 2. Módulos Disponíveis na Barra Lateral
* **📊 Resumo Executivo:**
  * **4 Cartões de KPI** com selos automáticos de conformidade.
  * **Aba 1 (`Tendências & 4 KPIs Gráficos`):** Grade 2x2 interativa com evolução mensal de OTIF (%), Volume de Pedidos, Faturamento (R$) e Lead Time (dias).
  * **Aba 2 (`Tabelas Dinâmicas`):** Rankings lado a lado de **Categorias** e **Estados (UF)** com seletor de quantidade (`Top 10`, `Top 15`, `Top 25`, `Todos`) e ordenação customizável.
  * **Aba 3 (`Diagnóstico & Insights`):** Cartões automatizados destacando **Pontos Positivos**, **Pontos de Melhoria** e **Alertas Críticos** conforme o recorte filtrado.
  * **Aba 4 (`Exportação Gerencial`):** Download imediato dos dados filtrados em **CSV**, **Excel (`.xlsx`)** e **Resumo Executivo (`.txt`)**.
* **🚚 Operação & SLA (OTIF):** Gráfico de rosca (*No Prazo vs. Atrasado*) e histograma de distribuição do *Lead Time* em dias.
* **🗺️ Regionais e Rotas:** Comparativo visual entre Top 10 Estados em volume absoluto de atrasos vs. Top 10 Estados em taxa percentual de falha, seguido da matriz completa das 27 UFs.
* **🚨 Riscos e Qualidade:** Auditoria de integridade das 5 tabelas relacionais, identificação do pior outlier logístico e listagem dos **Top 20 Pedidos Críticos** de maior impacto financeiro.

---

## 📂 Arquitetura do Repositório

```
Torre_Logistica_LockTrack/
├── archive/                                  # Bases relacionais (Olist Supply Chain Dataset)
│   ├── olist_customers_dataset.csv           # Cadastro geográfico de clientes (UF e Cidade)
│   ├── olist_order_items_dataset.csv         # Itens, preços e valores de frete por pedido
│   ├── olist_orders_dataset.csv              # Ciclo de vida e timestamps logísticos dos pedidos
│   ├── olist_products_dataset.csv            # Catálogo e atributos técnicos dos produtos
│   └── product_category_name_translation.csv # Dicionário de tradução de categorias
├── app.py                                    # Aplicação principal Streamlit (Executive Dark UI)
├── requirements.txt                          # Dependências (streamlit, pandas, plotly, openpyxl)
└── README.md                                 # Documentação técnica e manual do usuário
````

## 🚀 Como Executar Localmente
- 1. Clone o repositório:
````
git clone [https://github.com/LuizAmeida/Torre_Logistica_LockTrack.git](https://github.com/LuizAmeida/Torre_Logistica_LockTrack.git)
cd Torre_Logistica_LockTrack
````

2. Instale as dependências:
````
pip install -r requirements.txt
````

3. Execute a aplicação:
````
streamlit run app.py
````

## 🗺️ Roadmap de Evolução (Fases 2 e 3)
- ✅ Fase 1 — Torre de Controle & Diagnóstico Descritivo (Atual): Modelagem relacional ETL, cálculo de KPIs logísticos/financeiros, dashboard interativo em nuvem e exportação gerencial.

- 🔜 Fase 2 — Inteligência Preditiva & Machine Learning: Desenvolvimento de modelo de classificação supervisionada para prever o risco de atraso no momento da expedição, permitindo atuação preventiva antes da quebra do SLA.

- 🔮 Fase 3 — Engenharia de Dados em Nuvem & Alertas Automatizados: Migração dos dados para banco relacional em nuvem (PostgreSQL), atualização automatizada via pipelines e disparo de alertas operacionais via Webhook/WhatsApp para rotas críticas.

- 👨‍💻 Autor

Luiz Edglei Marques de Almeida

Operações Logísticas e Gestão de Estoque (15 anos de experiência) & Analista de Dados em Formação (TripleTen | Ciência da Computação)

Unindo sólida vivência prática em gestão de inventário, cadeia de suprimentos e auditoria de processos com análise de dados em Python, SQL e Business Intelligence.

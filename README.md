# 🚚 LogiTrack: Torre de Controle Logística & Última Milha

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído%20(Fase%201)-2EA44F?style=for-the-badge)

> **Inteligência Logística, Confiabilidade OTIF e Mitigação de Riscos na Cadeia de Suprimentos.**

---

## 🎯 Visão Geral e Problema de Negócio

Em operações de e-commerce e distribuição de última milha, a visibilidade fragmentada por planilhas desconectadas atrasa a tomada de decisão e compromete diretamente a experiência do cliente e o fluxo de caixa.

O **LogiTrack** foi desenvolvido para atuar como uma **Torre de Controle Analítica**, transformando quase 100 mil registros operacionais reais (Dataset Olist) em diagnósticos executivos acionáveis para gestores de logística, operações e finanças:

* **📉 Confiabilidade OTIF (*On-Time In-Full*):** Monitoramento preciso do percentual de pedidos entregues dentro do prazo prometido.
* **💰 Impacto Financeiro Direto:** Mensuração exata da receita exposta em rotas críticas e pedidos com atraso.
* **🗺️ Diagnóstico Geográfico:** Separação estratégica entre volume absoluto de ocorrências e risco proporcional por estado.

---

## 📊 Principais Resultados e Insights Obtidos

A auditoria analítica da operação consolidou os seguintes indicadores-chave:

| Indicador Operacional / Financeiro | Métrica Consolidada | Impacto Gerencial |
| :--- | :---: | :--- |
| **📦 Volume Total de Pedidos** | **98.666** | Escala operacional auditada na cadeia de suprimentos |
| **💵 Faturamento Total** | **R$ 15.843.550,00** | Receita bruta movimentada no período analisado |
| **✅ Índice OTIF Global** | **92,1%** | Taxa geral de cumprimento de prazo de entrega |
| **⏱️ Lead Time Médio** | **12,5 dias** | Ciclo médio entre aprovação e entrega ao cliente final |
| **🚛 Custo Médio de Frete** | **R$ 19,99** | Ticket médio logístico por pedido despachado |
| **🚨 Receita em Risco (Atrasos)** | **R$ 1.351.669,00** | Capital exposto em entregas fora do SLA acordado |

### 🔍 O Paradoxo do Volume vs. Proporcionalidade
* **Volume Absoluto (SP):** São Paulo concentra o maior número absoluto de atrasos devido à sua escala massiva (~41 mil pedidos), mas mantém uma taxa percentual saudável (~5,6%).
* **Risco Proporcional (AL, RJ, BA):** Estados periféricos e rotas de longa distância apresentam as maiores taxas relativas de falha, exigindo renegociação de SLAs com transportadoras regionais e estudo de centros de distribuição avançados.

---

## 🛠️ Arquitetura e Recursos do Painel

* **Filtros Dinâmicos Multidimensionais:** Segmentação instantânea por Estado (UF), Categoria de Produto e Status de Entrega.
* **Visualização Executiva:** Gráficos comparativos de faturamento por categoria, dispersão de frete x prazo e mapas de calor de atraso.
* **Exportação Gerencial Integrada:** Geração imediata de relatórios filtrados em **Excel (`.xlsx`)**, **CSV (`.csv`)** e resumos executivos em **TXT (`.txt`)** diretamente pela interface.

---

## 📂 Estrutura do Repositório

````
Torre_Logistica_LockTrack/
├── archive/                                  # Bases de dados relacionais (Olist Dataset)
│   ├── olist_customers_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_products_dataset.csv
│   └── product_category_name_translation.csv
├── app.py                                    # Aplicação principal da Torre de Controle (Streamlit)
├── requirements.txt                          # Dependências e bibliotecas do projeto
└── README.md                                 # Documentação executiva do projeto
````

## 🚀 Como Executar Localmente
1. Clone o repositório:
````
git clone [https://github.com/LuizAmeida/Torre_Logistica_LockTrack.git](https://github.com/LuizAmeida/Torre_Logistica_LockTrack.git)
cd Torre_Logistica_LockTrack
````
2. Instale as dependências:
````
pip install -r requirements.txt
````

3. Inicie o servidor Streamlit:
````
streamlit run app.py
````

## 🗺️ Roadmap de Evolução do Projeto
**O LogiTrack foi estruturado em três fases evolutivas para acompanhar a maturidade tecnológica da operação:**

- ✅ Fase 1 — Torre de Controle & Diagnóstico (Atual): Consolidação da base relacional, cálculo de KPIs logísticos/financeiros (OTIF, Lead Time, Receita em Risco) e painel interativo com exportação gerencial.

- 🔜 Fase 2 — Inteligência Preditiva (Machine Learning): Implementação de modelos de classificação para prever a probabilidade de atraso de um pedido no momento da expedição, permitindo atuação preventiva antes da quebra do SLA.

- 🔮 Fase 3 — Automação em Nuvem & Alertas em Tempo Real: Integração via APIs/Webhooks com bancos de dados em nuvem e disparo automático de alertas operacionais para rotas críticas.

## 👨‍💻 Autor
- Luiz Almeida

Profissional em logística, com transição de carreira para a área de Dados.
15 anos de experiência em gestão de estoques, auditoria de inventário e cadeia logística, unindo vivência prática de operação com Python, SQL, Power BI e automação de processos.







import io
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO EXECUTIVO (DARK UI)
# ==============================================================================
st.set_page_config(
    page_title="LogiTrack | Torre de Controle Logística",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado para o tema escuro corporativo, cartões de KPI e caixas de insights
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B1120;
        color: #F8FAFC;
    }
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
    
    /* Cabeçalho Superior */
    .exec-header {
        background: linear-gradient(90deg, #0F172A 0%, #1E293B 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 20px;
    }
    .exec-title {
        font-size: 1.55rem;
        font-weight: 700;
        color: #F8FAFC;
        margin: 0;
    }
    .exec-subtitle {
        font-size: 0.9rem;
        color: #94A3B8;
        margin-top: 4px;
    }

    /* Cartões de KPI com Selos de Meta */
    .kpi-card {
        background-color: #111827;
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        height: 100%;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.15;
        margin-bottom: 8px;
    }
    .kpi-meta {
        font-size: 0.78rem;
        color: #64748B;
        margin-bottom: 10px;
    }
    .badge-ok {
        display: inline-block;
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .badge-alert {
        display: inline-block;
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.35);
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .badge-info {
        display: inline-block;
        background-color: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 3px 10px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    /* Cartões de Insights (Positivos, Melhorias e Alertas) */
    .insight-card-pos {
        background-color: #111827;
        border-left: 4px solid #10B981;
        border-top: 1px solid #1E293B;
        border-right: 1px solid #1E293B;
        border-bottom: 1px solid #1E293B;
        border-radius: 10px;
        padding: 16px;
        height: 100%;
    }
    .insight-card-warn {
        background-color: #111827;
        border-left: 4px solid #F59E0B;
        border-top: 1px solid #1E293B;
        border-right: 1px solid #1E293B;
        border-bottom: 1px solid #1E293B;
        border-radius: 10px;
        padding: 16px;
        height: 100%;
    }
    .insight-card-crit {
        background-color: #111827;
        border-left: 4px solid #EF4444;
        border-top: 1px solid #1E293B;
        border-right: 1px solid #1E293B;
        border-bottom: 1px solid #1E293B;
        border-radius: 10px;
        padding: 16px;
        height: 100%;
    }
    .insight-title {
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .insight-text {
        font-size: 0.85rem;
        color: #CBD5E1;
        line-height: 1.5;
    }

    /* Estilização das abas horizontais */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0F172A;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #1E293B;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #38BDF8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. CARREGAMENTO E PREPARAÇÃO DOS DADOS (ETL COM CACHE)
# ==============================================================================
@st.cache_data(show_spinner="Carregando e consolidando bases logísticas...")
def carregar_dados():
    orders = pd.read_csv("archive/olist_orders_dataset.csv")
    items = pd.read_csv("archive/olist_order_items_dataset.csv")
    customers = pd.read_csv("archive/olist_customers_dataset.csv")
    products = pd.read_csv("archive/olist_products_dataset.csv")
    translation = pd.read_csv("archive/product_category_name_translation.csv")

    orders = orders[orders["order_status"] == "delivered"].copy()

    cols_data = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in cols_data:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    orders = orders.dropna(
        subset=["order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp"]
    )

    # Engenharia de Atributos Logísticos
    orders["lead_time_dias"] = (
        orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400.0

    orders["dias_diferenca_sla"] = (
        orders["order_delivered_customer_date"] - orders["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400.0

    orders["no_prazo"] = orders["order_delivered_customer_date"] <= orders["order_estimated_delivery_date"]
    orders["status_sla"] = orders["no_prazo"].map({True: "No Prazo (OTIF)", False: "Atrasado"})

    orders["ano"] = orders["order_purchase_timestamp"].dt.year
    orders["mes_num"] = orders["order_purchase_timestamp"].dt.month
    orders["ano_mes"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

    # Cruzamento com Clientes
    df_merged = pd.merge(
        orders,
        customers[["customer_id", "customer_state", "customer_city"]],
        on="customer_id",
        how="left",
    )

    # Agregação de Itens por Pedido
    itens_agg = (
        items.groupby("order_id", as_index=False)
        .agg(
            valor_produtos=("price", "sum"),
            valor_frete=("freight_value", "sum"),
            qtd_itens=("order_item_id", "count"),
            product_id=("product_id", "first"),
        )
    )
    itens_agg["faturamento_total"] = itens_agg["valor_produtos"] + itens_agg["valor_frete"]

    df_merged = pd.merge(df_merged, itens_agg, on="order_id", how="inner")

    # Cruzamento com Produtos e Tradução
    produtos_cat = pd.merge(
        products[["product_id", "product_category_name"]],
        translation,
        on="product_category_name",
        how="left",
    )
    produtos_cat["categoria"] = (
        produtos_cat["product_category_name_english"]
        .fillna(produtos_cat["product_category_name"])
        .fillna("Outros / Não Classificado")
        .str.replace("_", " ")
        .str.title()
    )

    df_final = pd.merge(
        df_merged,
        produtos_cat[["product_id", "categoria"]],
        on="product_id",
        how="left",
    )
    df_final["categoria"] = df_final["categoria"].fillna("Outros / Não Classificado")

    return df_final, orders, items, customers, products


df_raw, orders_raw, items_raw, customers_raw, products_raw = carregar_dados()

# ==============================================================================
# 3. BARRA LATERAL (NAVEGAÇÃO + 4 METAS DE REFERÊNCIA COM LEGENDAS)
# ==============================================================================
with st.sidebar:
    st.markdown("### 🚚 LogiTrack")
    st.caption("TORRE DE CONTROLE & ÚLTIMA MILHA")
    st.divider()

    pagina_selecionada = st.radio(
        "NAVEGAÇÃO ANALÍTICA",
        options=[
            "📊 Resumo Executivo",
            "🚚 Operação & SLA (OTIF)",
            "🗺️ Regionais e Rotas",
            "🚨 Riscos e Qualidade",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.markdown("#### 🎯 Régua de Metas (Referência Visual)")
    st.caption(
        "Estes controles ajustam as **linhas de meta** nos 4 gráficos e os **selos de status** dos cartões "
        "(não filtram a base de pedidos)."
    )

    # Controle 1 -> Gráfico 1 (OTIF)
    meta_otif = st.slider(
        "1. Meta Índice OTIF (%)",
        min_value=80.0,
        max_value=99.0,
        value=95.0,
        step=0.5,
        help="Define a meta mínima de entregas no prazo exibida no Gráfico 1 e no Cartão 1.",
    )
    st.caption("↳ Atualiza a linha de meta no Gráfico 1 (OTIF).")

    # Controle 2 -> Gráfico 2 (Volume Mensal)
    meta_volume_mensal = st.slider(
        "2. Meta Volume Mensal (pedidos)",
        min_value=500,
        max_value=8000,
        value=4500,
        step=250,
        help="Define a capacidade mensal esperada de pedidos exibida no Gráfico 2 e no Cartão 3.",
    )
    st.caption("↳ Atualiza a linha de meta no Gráfico 2 (Pedidos).")

    # Controle 3 -> Gráfico 3 (Faturamento Mensal)
    meta_faturamento_mensal = st.slider(
        "3. Meta Faturamento Mensal (R$)",
        min_value=100000,
        max_value=1200000,
        value=700000,
        step=50000,
        help="Define a meta mensal de receita logística exibida no Gráfico 3.",
    )
    st.caption("↳ Atualiza a linha de meta no Gráfico 3 (Faturamento).")

    # Controle 4 -> Gráfico 4 (Lead Time)
    meta_lead_time = st.slider(
        "4. Meta Lead Time Máx. (dias)",
        min_value=5.0,
        max_value=20.0,
        value=12.0,
        step=0.5,
        help="Define o prazo máximo médio aceitável de entrega exibido no Gráfico 4 e no Cartão 2.",
    )
    st.caption("↳ Atualiza a linha de meta no Gráfico 4 (Lead Time).")

    st.divider()
    st.caption("Desenvolvido por **Luiz Almeida**")
    st.caption("Dados: Olist Supply Chain Dataset")

# ==============================================================================
# 4. CABEÇALHO SUPERIOR E BARRA DE FILTROS GLOBAIS DA BASE
# ==============================================================================
st.markdown(
    """
    <div class="exec-header">
        <div class="exec-title">Torre de Controle Logística — Inteligência Operacional</div>
        <div class="exec-subtitle">Monitoramento de Confiabilidade OTIF, Lead Time, Custos de Frete e Receita Exposta em Atrasos</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("🔎 **Filtros Globais da Base:** Alterar os campos abaixo recalcula todos os cartões, gráficos, tabelas e insights simultaneamente.")
with st.container():
    col_f1, col_f2, col_f3, col_f4 = st.columns([1.1, 1.3, 1.6, 1.2])

    anos_disponiveis = sorted(df_raw["ano"].unique().tolist())
    with col_f1:
        anos_sel = st.multiselect("📅 Ano", options=anos_disponiveis, default=anos_disponiveis)

    ufs_disponiveis = sorted(df_raw["customer_state"].dropna().unique().tolist())
    with col_f2:
        ufs_sel = st.multiselect("📍 Estado (UF)", options=ufs_disponiveis, default=[], placeholder="Todos os estados")

    cats_disponiveis = sorted(df_raw["categoria"].dropna().unique().tolist())
    with col_f3:
        cats_sel = st.multiselect("📦 Categoria", options=cats_disponiveis, default=[], placeholder="Todas as categorias")

    with col_f4:
        status_sel = st.selectbox("⏱️ Status SLA", options=["Todos", "No Prazo (OTIF)", "Atrasado"])

df = df_raw.copy()
if anos_sel:
    df = df[df["ano"].isin(anos_sel)]
if ufs_sel:
    df = df[df["customer_state"].isin(ufs_sel)]
if cats_sel:
    df = df[df["categoria"].isin(cats_sel)]
if status_sel != "Todos":
    df = df[df["status_sla"] == status_sel]

if df.empty:
    st.warning("Nenhum pedido encontrado para a combinação de filtros selecionada. Ajuste os filtros acima.")
    st.stop()

# ==============================================================================
# 5. CÁLCULO DOS KPIS CONSOLIDADOS E FUNÇÃO DE CARTÃO HTML
# ==============================================================================
total_pedidos = len(df)
qtd_meses_ativos = max(1, df["ano_mes"].nunique())
media_pedidos_mes = total_pedidos / qtd_meses_ativos
faturamento_total = df["faturamento_total"].sum()
media_faturamento_mes = faturamento_total / qtd_meses_ativos
otif_atual = (df["no_prazo"].mean()) * 100.0
lead_time_medio = df["lead_time_dias"].mean()
frete_medio = df["valor_frete"].mean()
pedidos_atrasados = df[~df["no_prazo"]]
receita_risco = pedidos_atrasados["faturamento_total"].sum()
pct_risco = (receita_risco / faturamento_total * 100) if faturamento_total > 0 else 0.0


def render_kpi_card(titulo, valor_str, meta_str, status_ok, texto_badge, neutro=False):
    if neutro:
        badge_class = "badge-info"
    else:
        badge_class = "badge-ok" if status_ok else "badge-alert"

    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{titulo}</div>
        <div class="kpi-value">{valor_str}</div>
        <div class="kpi-meta">{meta_str}</div>
        <span class="{badge_class}">{texto_badge}</span>
    </div>
    """


# ==============================================================================
# PÁGINA 1: RESUMO EXECUTIVO (COMPLETO COM 4 GRÁFICOS, 2 TABELAS E INSIGHTS)
# ==============================================================================
if pagina_selecionada == "📊 Resumo Executivo":
    # Linha 1: 4 Cartões de KPI conectados às metas da barra lateral
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            render_kpi_card(
                "ÍNDICE OTIF GLOBAL",
                f"{otif_atual:.1f}%",
                f"Meta SLA: {meta_otif:.1f}%",
                otif_atual >= meta_otif,
                "Dentro da meta" if otif_atual >= meta_otif else "Fora da meta",
            ),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            render_kpi_card(
                "LEAD TIME MÉDIO",
                f"{lead_time_medio:.1f} dias",
                f"Meta Máx.: {meta_lead_time:.1f} dias",
                lead_time_medio <= meta_lead_time,
                "Dentro do prazo" if lead_time_medio <= meta_lead_time else "Acima do limite",
            ),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            render_kpi_card(
                "VOLUME DE PEDIDOS",
                f"{total_pedidos:,}".replace(",", "."),
                f"Média: {media_pedidos_mes:,.0f}/mês (Meta: {meta_volume_mensal:,})".replace(",", "."),
                media_pedidos_mes >= meta_volume_mensal,
                "Acima da meta mensal" if media_pedidos_mes >= meta_volume_mensal else "Abaixo da meta mensal",
            ),
            unsafe_allow_html=True,
        )
    with c4:
        val_risco_fmt = f"R$ {receita_risco:,.0f}".replace(",", ".")
        st.markdown(
            render_kpi_card(
                "RECEITA EM RISCO (ATRASOS)",
                val_risco_fmt,
                f"{pct_risco:.1f}% do faturamento | Frete: R$ {frete_medio:.2f}",
                pct_risco <= 5.0,
                "Risco Controlado" if pct_risco <= 5.0 else "Atenção Financeira",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Sub-abas Horizontais
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📈 Tendências & 4 KPIs Gráficos",
            "📊 Tabelas Dinâmicas (Categorias & Estados)",
            "💡 Diagnóstico & Insights",
            "📥 Exportação Gerencial",
        ]
    )

    # --------------------------------------------------------------------------
    # SUB-ABA 1: OS 4 GRÁFICOS DE KPIS (GRADE 2x2 COM METAS E LEGENDAS)
    # --------------------------------------------------------------------------
    with tab1:
        st.caption(
            "📌 **Legenda dos Gráficos:** As linhas contínuas/barras representam o **desempenho real realizado** mês a mês; "
            "as **linhas tracejadas vermelhas** representam as metas ajustadas no painel lateral esquerdo."
        )

        mensal = (
            df.groupby("ano_mes", as_index=False)
            .agg(
                pedidos=("order_id", "count"),
                faturamento=("faturamento_total", "sum"),
                otif=("no_prazo", lambda x: x.mean() * 100),
                lead_time=("lead_time_dias", "mean"),
            )
            .sort_values("ano_mes")
        )

        # Linha Superior de Gráficos (Gráfico 1 e Gráfico 2)
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            fig_otif = go.Figure()
            fig_otif.add_trace(
                go.Scatter(
                    x=mensal["ano_mes"],
                    y=mensal["otif"],
                    mode="lines+markers+text",
                    name="OTIF Realizado (%)",
                    line=dict(color="#00D4FF", width=3),
                    marker=dict(size=7, color="#00D4FF"),
                    text=[f"{v:.1f}%" for v in mensal["otif"]],
                    textposition="top center",
                    textfont=dict(size=9, color="#E2E8F0"),
                )
            )
            fig_otif.add_hline(
                y=meta_otif,
                line_dash="dash",
                line_color="#F87171",
                annotation_text=f"Meta OTIF ({meta_otif:.1f}%)",
                annotation_font_color="#F87171",
            )
            fig_otif.update_layout(
                title="1. Evolução Mensal da Confiabilidade OTIF (%)",
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font=dict(color="#F8FAFC"),
                yaxis=dict(range=[60, 105], showgrid=True, gridcolor="#1E293B", title="OTIF (%)"),
                xaxis=dict(showgrid=False, title="Mês"),
                margin=dict(l=20, r=20, t=50, b=20),
                height=350,
            )
            st.plotly_chart(fig_otif, use_container_width=True)

        with col_g2:
            fig_vol = px.bar(
                mensal,
                x="ano_mes",
                y="pedidos",
                title="2. Volume Mensal de Pedidos Entregues",
                text="pedidos",
                color_discrete_sequence=["#6366F1"],
            )
            fig_vol.update_traces(textposition="outside", textfont=dict(size=9, color="#CBD5E1"))
            fig_vol.add_hline(
                y=meta_volume_mensal,
                line_dash="dash",
                line_color="#F87171",
                annotation_text=f"Meta Volume ({meta_volume_mensal:,})".replace(",", "."),
                annotation_font_color="#F87171",
            )
            fig_vol.update_layout(
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font=dict(color="#F8FAFC"),
                yaxis=dict(showgrid=True, gridcolor="#1E293B", title="Pedidos"),
                xaxis=dict(showgrid=False, title="Mês"),
                margin=dict(l=20, r=20, t=50, b=20),
                height=350,
            )
            st.plotly_chart(fig_vol, use_container_width=True)

        # Linha Inferior de Gráficos (Gráfico 3 e Gráfico 4)
        col_g3, col_g4 = st.columns(2)

        with col_g3:
            fig_fat = go.Figure()
            fig_fat.add_trace(
                go.Scatter(
                    x=mensal["ano_mes"],
                    y=mensal["faturamento"],
                    mode="lines+markers",
                    fill="tozeroy",
                    fillcolor="rgba(16, 185, 129, 0.15)",
                    line=dict(color="#10B981", width=3),
                    marker=dict(size=6, color="#10B981"),
                    name="Faturamento Realizado (R$)",
                )
            )
            fig_fat.add_hline(
                y=meta_faturamento_mensal,
                line_dash="dash",
                line_color="#F87171",
                annotation_text=f"Meta Receita (R$ {meta_faturamento_mensal:,.0f})".replace(",", "."),
                annotation_font_color="#F87171",
            )
            fig_fat.update_layout(
                title="3. Evolução do Faturamento Logístico Mensal (R$)",
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font=dict(color="#F8FAFC"),
                yaxis=dict(showgrid=True, gridcolor="#1E293B", title="Faturamento (R$)"),
                xaxis=dict(showgrid=False, title="Mês"),
                margin=dict(l=20, r=20, t=50, b=20),
                height=350,
            )
            st.plotly_chart(fig_fat, use_container_width=True)

        with col_g4:
            fig_lt = go.Figure()
            fig_lt.add_trace(
                go.Scatter(
                    x=mensal["ano_mes"],
                    y=mensal["lead_time"],
                    mode="lines+markers+text",
                    name="Lead Time Realizado (dias)",
                    line=dict(color="#F59E0B", width=3),
                    marker=dict(size=7, color="#F59E0B"),
                    text=[f"{v:.1f}d" for v in mensal["lead_time"]],
                    textposition="top center",
                    textfont=dict(size=9, color="#FDE68A"),
                )
            )
            fig_lt.add_hline(
                y=meta_lead_time,
                line_dash="dash",
                line_color="#F87171",
                annotation_text=f"Meta Prazo ({meta_lead_time:.1f}d)",
                annotation_font_color="#F87171",
            )
            fig_lt.update_layout(
                title="4. Evolução do Lead Time Médio de Entrega (dias)",
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font=dict(color="#F8FAFC"),
                yaxis=dict(showgrid=True, gridcolor="#1E293B", title="Dias"),
                xaxis=dict(showgrid=False, title="Mês"),
                margin=dict(l=20, r=20, t=50, b=20),
                height=350,
            )
            st.plotly_chart(fig_lt, use_container_width=True)

    # --------------------------------------------------------------------------
    # SUB-ABA 2: AS DUAS TABELAS COM FILTRO DE QUANTIDADE (CATEGORIAS & ESTADOS)
    # --------------------------------------------------------------------------
    with tab2:
        col_t1, col_t2 = st.columns(2)

        # --- TABELA 1: CATEGORIAS COM SELETOR DE QUANTIDADE ---
        with col_t1:
            st.markdown("#### 📦 Ranking de Categorias por Faturamento")
            col_c_opt1, col_c_opt2 = st.columns([1.2, 1])
            with col_c_opt1:
                qtd_cat_opcao = st.selectbox(
                    "Quantidade de Categorias a exibir:",
                    options=["Top 10", "Top 15", "Top 25", "Todas as Categorias"],
                    index=1,
                    key="filtro_qtd_cat",
                )
            with col_c_opt2:
                ord_cat = st.selectbox(
                    "Ordenar Categorias por:",
                    options=["Maior Faturamento", "Maior Volume de Pedidos", "Pior OTIF (%)"],
                    key="ord_cat",
                )

            pareto_cat = (
                df.groupby("categoria", as_index=False)
                .agg(
                    pedidos=("order_id", "count"),
                    faturamento=("faturamento_total", "sum"),
                    otif_pct=("no_prazo", lambda x: round(x.mean() * 100, 1)),
                    lead_time=("lead_time_dias", lambda x: round(x.mean(), 1)),
                )
            )
            pareto_cat["participacao_pct"] = (pareto_cat["faturamento"] / faturamento_total) * 100

            if ord_cat == "Maior Faturamento":
                pareto_cat = pareto_cat.sort_values("faturamento", ascending=False)
            elif ord_cat == "Maior Volume de Pedidos":
                pareto_cat = pareto_cat.sort_values("pedidos", ascending=False)
            else:
                pareto_cat = pareto_cat.sort_values("otif_pct", ascending=True)

            mapa_qtd_cat = {"Top 10": 10, "Top 15": 15, "Top 25": 25, "Todas as Categorias": len(pareto_cat)}
            pareto_cat_exibir = pareto_cat.head(mapa_qtd_cat[qtd_cat_opcao])

            st.dataframe(
                pareto_cat_exibir,
                column_config={
                    "categoria": st.column_config.TextColumn("Categoria"),
                    "pedidos": st.column_config.NumberColumn("Pedidos", format="%d"),
                    "faturamento": st.column_config.NumberColumn("Faturamento", format="R$ %.2f"),
                    "participacao_pct": st.column_config.ProgressColumn(
                        "Part. Receita",
                        format="%.1f%%",
                        min_value=0,
                        max_value=float(pareto_cat["participacao_pct"].max()) if not pareto_cat.empty else 100.0,
                    ),
                    "otif_pct": st.column_config.NumberColumn("OTIF (%)", format="%.1f%%"),
                    "lead_time": st.column_config.NumberColumn("Lead Time", format="%.1fd"),
                },
                hide_index=True,
                use_container_width=True,
                height=440,
            )

        # --- TABELA 2: ESTADOS (UF) COM SELETOR DE QUANTIDADE ---
        with col_t2:
            st.markdown("#### 🗺️ Performance Logística por Estado (UF)")
            col_u_opt1, col_u_opt2 = st.columns([1.2, 1])
            with col_u_opt1:
                qtd_uf_opcao = st.selectbox(
                    "Quantidade de Estados (UF) a exibir:",
                    options=["Todos os Estados (27 UFs)", "Top 5 Estados", "Top 10 Estados", "Top 15 Estados"],
                    index=0,
                    key="filtro_qtd_uf",
                )
            with col_u_opt2:
                ord_uf = st.selectbox(
                    "Ordenar Estados por:",
                    options=["Maior Volume de Pedidos", "Maior Faturamento", "Maior Taxa de Atraso (%)", "Receita em Risco"],
                    key="ord_uf",
                )

            uf_resumo = (
                df.groupby("customer_state", as_index=False)
                .agg(
                    pedidos=("order_id", "count"),
                    faturamento=("faturamento_total", "sum"),
                    otif_pct=("no_prazo", lambda x: round(x.mean() * 100, 1)),
                    taxa_atraso=("no_prazo", lambda x: round((~x).mean() * 100, 1)),
                    lead_time=("lead_time_dias", lambda x: round(x.mean(), 1)),
                    receita_risco=("faturamento_total", lambda s: s[~df.loc[s.index, "no_prazo"]].sum()),
                )
            )

            if ord_uf == "Maior Volume de Pedidos":
                uf_resumo = uf_resumo.sort_values("pedidos", ascending=False)
            elif ord_uf == "Maior Faturamento":
                uf_resumo = uf_resumo.sort_values("faturamento", ascending=False)
            elif ord_uf == "Maior Taxa de Atraso (%)":
                uf_resumo = uf_resumo.sort_values("taxa_atraso", ascending=False)
            else:
                uf_resumo = uf_resumo.sort_values("receita_risco", ascending=False)

            mapa_qtd_uf = {
                "Todos os Estados (27 UFs)": len(uf_resumo),
                "Top 5 Estados": 5,
                "Top 10 Estados": 10,
                "Top 15 Estados": 15,
            }
            uf_exibir = uf_resumo.head(mapa_qtd_uf[qtd_uf_opcao])

            st.dataframe(
                uf_exibir,
                column_config={
                    "customer_state": st.column_config.TextColumn("UF"),
                    "pedidos": st.column_config.NumberColumn("Pedidos", format="%d"),
                    "faturamento": st.column_config.NumberColumn("Faturamento", format="R$ %.2f"),
                    "otif_pct": st.column_config.ProgressColumn(
                        "OTIF (%)", format="%.1f%%", min_value=0, max_value=100
                    ),
                    "taxa_atraso": st.column_config.NumberColumn("Atraso (%)", format="%.1f%%"),
                    "lead_time": st.column_config.NumberColumn("Lead Time", format="%.1fd"),
                    "receita_risco": st.column_config.NumberColumn("Receita Risco", format="R$ %.2f"),
                },
                hide_index=True,
                use_container_width=True,
                height=440,
            )

    # --------------------------------------------------------------------------
    # SUB-ABA 3: DIAGNÓSTICO EXECUTIVO (INSIGHTS POSITIVOS, MELHORIAS E ALERTAS)
    # --------------------------------------------------------------------------
    with tab3:
        st.markdown("#### 🧠 Diagnóstico Automatizado da Operação (Baseado nos Filtros e Metas Atuais)")

        uf_agrup = (
            df.groupby("customer_state", as_index=False)
            .agg(
                pedidos=("order_id", "count"),
                otif=("no_prazo", lambda x: x.mean() * 100),
                atraso_pct=("no_prazo", lambda x: (~x).mean() * 100),
                risco=("faturamento_total", lambda s: s[~df.loc[s.index, "no_prazo"]].sum()),
            )
        )
        uf_relevante = uf_agrup[uf_agrup["pedidos"] >= 30] if len(uf_agrup[uf_agrup["pedidos"] >= 30]) > 0 else uf_agrup

        melhor_uf = uf_relevante.sort_values("otif", ascending=False).iloc[0]
        pior_uf = uf_relevante.sort_values("atraso_pct", ascending=False).iloc[0]
        maior_risco_uf = uf_agrup.sort_values("risco", ascending=False).iloc[0]

        col_in1, col_in2, col_in3 = st.columns(3)

        with col_in1:
            st.markdown(
                f"""
                <div class="insight-card-pos">
                    <div class="insight-title" style="color: #34D399;">✅ Pontos Positivos (Destaques)</div>
                    <div class="insight-text">
                        • <b>Confiabilidade Geral:</b> {otif_atual:.1f}% dos pedidos filtrados foram entregues rigorosamente dentro do prazo acordado.<br><br>
                        • <b>Benchmark Regional ({melhor_uf['customer_state']}):</b> O estado de <b>{melhor_uf['customer_state']}</b> apresenta a melhor eficiência operacional, atingindo <b>{melhor_uf['otif']:.1f}% de OTIF</b> em {int(melhor_uf['pedidos']):,} pedidos.<br><br>
                        • <b>Média Comercial:</b> Faturamento médio mensal de <b>R$ {media_faturamento_mes:,.2f}</b> com ticket de frete em <b>R$ {frete_medio:.2f}</b>.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_in2:
            gap_otif = max(0.0, meta_otif - otif_atual)
            st.markdown(
                f"""
                <div class="insight-card-warn">
                    <div class="insight-title" style="color: #FBBF24;">⚠️ Pontos de Melhoria (Oportunidades)</div>
                    <div class="insight-text">
                        • <b>Gap para Meta SLA:</b> Faltam <b>{gap_otif:.1f} pontos percentuais</b> para atingir a meta estipulada de {meta_otif:.1f}% de OTIF.<br><br>
                        • <b>Revisão de Malha Regional:</b> Renegociar prazos de corte (cut-off) e transportadoras parceiras nas rotas de longa distância.<br><br>
                        • <b>Padronização Operacional (POP):</b> Implementar checklists preventivos de expedição para pedidos de alto ticket antes da coleta.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_in3:
            st.markdown(
                f"""
                <div class="insight-card-crit">
                    <div class="insight-title" style="color: #F87171;">🚨 Alertas Críticos (Ação Imediata)</div>
                    <div class="insight-text">
                        • <b>Capital Exposto:</b> Existem <b>R$ {receita_risco:,.2f}</b> ({pct_risco:.1f}% da receita) vinculados a pedidos entregues fora do SLA.<br><br>
                        • <b>Gargalo Proporcional ({pior_uf['customer_state']}):</b> O estado de <b>{pior_uf['customer_state']}</b> registra a maior taxa de falha relativa (<b>{pior_uf['atraso_pct']:.1f}% de atrasos</b>).<br><br>
                        • <b>Maior Concentração Financeira ({maior_risco_uf['customer_state']}):</b> <b>{maior_risco_uf['customer_state']}</b> concentra <b>R$ {maior_risco_uf['risco']:,.2f}</b> em receita atrasada.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------------------------
    # SUB-ABA 4: EXPORTAÇÃO GERENCIAL
    # --------------------------------------------------------------------------
    with tab4:
        st.markdown("#### Exportar Base Filtrada para Auditoria e Reunião")
        col_ex1, col_ex2, col_ex3 = st.columns(3)

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        with col_ex1:
            st.download_button(
                label="📄 Baixar Relatório CSV",
                data=csv_bytes,
                file_name="logitrack_relatorio_filtrado.csv",
                mime="text/csv",
                use_container_width=True,
            )

        buffer_xlsx = io.BytesIO()
        with pd.ExcelWriter(buffer_xlsx, engine="openpyxl") as writer:
            df.head(50000).to_excel(writer, index=False, sheet_name="Dados_LogiTrack")
        with col_ex2:
            st.download_button(
                label="📊 Baixar Planilha Excel (.xlsx)",
                data=buffer_xlsx.getvalue(),
                file_name="logitrack_executivo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        resumo_txt = (
            f"RESUMO EXECUTIVO LOGITRACK\n"
            f"==========================\n"
            f"Pedidos Auditados: {total_pedidos}\n"
            f"Faturamento Total: R$ {faturamento_total:,.2f}\n"
            f"Índice OTIF Atual: {otif_atual:.2f}% (Meta: {meta_otif:.2f}%)\n"
            f"Lead Time Médio: {lead_time_medio:.2f} dias (Meta: {meta_lead_time:.2f} dias)\n"
            f"Receita em Risco (Atrasos): R$ {receita_risco:,.2f} ({pct_risco:.2f}%)\n"
        )
        with col_ex3:
            st.download_button(
                label="📝 Baixar Resumo Executivo (.txt)",
                data=resumo_txt.encode("utf-8"),
                file_name="resumo_executivo_logitrack.txt",
                mime="text/plain",
                use_container_width=True,
            )

# ==============================================================================
# PÁGINA 2: OPERAÇÃO & SLA (OTIF)
# ==============================================================================
elif pagina_selecionada == "🚚 Operação & SLA (OTIF)":
    st.subheader("🚚 Análise Profunda de Prazos, Lead Time e Cumprimento de SLA")

    col_op1, col_op2 = st.columns(2)

    with col_op1:
        sla_dist = df["status_sla"].value_counts().reset_index()
        sla_dist.columns = ["Status", "Pedidos"]
        fig_donut = px.pie(
            sla_dist,
            names="Status",
            values="Pedidos",
            hole=0.58,
            title="Proporção de Entregas: No Prazo vs. Atrasadas",
            color="Status",
            color_discrete_map={"No Prazo (OTIF)": "#10B981", "Atrasado": "#EF4444"},
        )
        fig_donut.update_traces(textinfo="percent+label", textfont_size=12)
        fig_donut.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#F8FAFC"),
            height=380,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_op2:
        fig_hist = px.histogram(
            df[df["lead_time_dias"] <= 45],
            x="lead_time_dias",
            nbins=30,
            title="Distribuição do Lead Time de Entrega (até 45 dias)",
            color_discrete_sequence=["#00D4FF"],
        )
        fig_hist.add_vline(
            x=meta_lead_time,
            line_dash="dash",
            line_color="#F87171",
            annotation_text=f"Meta ({meta_lead_time}d)",
        )
        fig_hist.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#F8FAFC"),
            xaxis=dict(title="Dias entre Compra e Entrega", showgrid=False),
            yaxis=dict(title="Quantidade de Pedidos", showgrid=True, gridcolor="#1E293B"),
            height=380,
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# ==============================================================================
# PÁGINA 3: REGIONAIS E ROTAS (PARADOXO VOLUME VS PROPORCIONALIDADE)
# ==============================================================================
elif pagina_selecionada == "🗺️ Regionais e Rotas":
    st.subheader("🗺️ Diagnóstico Geográfico: Volume Absoluto vs. Risco Proporcional")
    st.info(
        "💡 **Insight Estratégico:** Estados com grande volume (como SP) lideram em número absoluto de ocorrências "
        "pela escala, enquanto estados periféricos apresentam maior **taxa percentual de falha**, exigindo revisão de SLA."
    )

    uf_stats = (
        df.groupby("customer_state", as_index=False)
        .agg(
            total_pedidos=("order_id", "count"),
            atrasos=("no_prazo", lambda x: (~x).sum()),
            taxa_atraso_pct=("no_prazo", lambda x: round((~x).mean() * 100, 2)),
            lead_time_medio=("lead_time_dias", lambda x: round(x.mean(), 1)),
            frete_medio=("valor_frete", lambda x: round(x.mean(), 2)),
            receita_risco=("faturamento_total", lambda s: s[~df.loc[s.index, "no_prazo"]].sum()),
        )
    )

    col_r1, col_r2 = st.columns(2)

    with col_r1:
        top_abs = uf_stats.sort_values("atrasos", ascending=False).head(10)
        fig_abs = px.bar(
            top_abs,
            x="customer_state",
            y="atrasos",
            text="atrasos",
            title="Top 10 Estados — Volume Absoluto de Atrasos",
            color_discrete_sequence=["#6366F1"],
        )
        fig_abs.update_traces(textposition="outside")
        fig_abs.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#F8FAFC"),
            xaxis=dict(title="Estado (UF)", showgrid=False),
            yaxis=dict(title="Pedidos Atrasados", showgrid=True, gridcolor="#1E293B"),
            height=380,
        )
        st.plotly_chart(fig_abs, use_container_width=True)

    with col_r2:
        top_pct = uf_stats[uf_stats["total_pedidos"] >= 50].sort_values("taxa_atraso_pct", ascending=False).head(10)
        fig_pct = px.bar(
            top_pct,
            x="customer_state",
            y="taxa_atraso_pct",
            text=[f"{v:.1f}%" for v in top_pct["taxa_atraso_pct"]],
            title="Top 10 Estados — Maior Taxa Proporcional de Atraso (%)",
            color_discrete_sequence=["#EF4444"],
        )
        fig_pct.update_traces(textposition="outside")
        fig_pct.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#F8FAFC"),
            xaxis=dict(title="Estado (UF)", showgrid=False),
            yaxis=dict(title="Taxa de Atraso (%)", showgrid=True, gridcolor="#1E293B"),
            height=380,
        )
        st.plotly_chart(fig_pct, use_container_width=True)

    st.markdown("#### Matriz Completa de Performance por Estado (UF)")
    st.dataframe(
        uf_stats.sort_values("taxa_atraso_pct", ascending=False),
        column_config={
            "customer_state": "UF",
            "total_pedidos": st.column_config.NumberColumn("Total Pedidos", format="%d"),
            "atrasos": st.column_config.NumberColumn("Qtd. Atrasos", format="%d"),
            "taxa_atraso_pct": st.column_config.ProgressColumn(
                "Taxa de Atraso (%)", format="%.2f%%", min_value=0, max_value=30
            ),
            "lead_time_medio": st.column_config.NumberColumn("Lead Time (dias)", format="%.1f"),
            "frete_medio": st.column_config.NumberColumn("Frete Médio", format="R$ %.2f"),
            "receita_risco": st.column_config.NumberColumn("Receita em Risco", format="R$ %.2f"),
        },
        hide_index=True,
        use_container_width=True,
    )

# ==============================================================================
# PÁGINA 4: RISCOS E QUALIDADE DOS DADOS
# ==============================================================================
elif pagina_selecionada == "🚨 Riscos e Qualidade":
    st.subheader("🚨 Auditoria de Integridade da Base e Pedidos Críticos")

    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        st.markdown(
            render_kpi_card(
                "REGISTROS BRUTOS (ORDERS)",
                f"{len(orders_raw):,}".replace(",", "."),
                "Tabela olist_orders_dataset.csv",
                True,
                "100% Lido",
                neutro=True,
            ),
            unsafe_allow_html=True,
        )
    with col_q2:
        st.markdown(
            render_kpi_card(
                "CHAVES RELACIONAIS",
                "5 Tabelas",
                "Orders, Items, Customers, Products, Translation",
                True,
                "Integridade Validada",
            ),
            unsafe_allow_html=True,
        )
    with col_q3:
        atraso_max = df["dias_diferenca_sla"].max()
        st.markdown(
            render_kpi_card(
                "PIOR ATRASO REGISTRADO",
                f"{atraso_max:.0f} dias",
                "Acima da data estimada ao cliente",
                False,
                "Outlier Logístico",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Top 20 Pedidos Críticos (Maior Impacto Financeiro em Atraso)")
    criticos = (
        pedidos_atrasados[
            [
                "order_id",
                "customer_state",
                "categoria",
                "lead_time_dias",
                "dias_diferenca_sla",
                "faturamento_total",
            ]
        ]
        .sort_values("faturamento_total", ascending=False)
        .head(20)
    )
    st.dataframe(
        criticos,
        column_config={
            "order_id": "ID do Pedido",
            "customer_state": "UF",
            "categoria": "Categoria",
            "lead_time_dias": st.column_config.NumberColumn("Lead Time (dias)", format="%.1f"),
            "dias_diferenca_sla": st.column_config.NumberColumn("Dias de Atraso", format="%.1f"),
            "faturamento_total": st.column_config.NumberColumn("Valor Exposto", format="R$ %.2f"),
        },
        hide_index=True,
        use_container_width=True,
    )

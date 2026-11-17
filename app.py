import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import io

# Configuração da Página
st.set_page_config(
    page_title="LogiTrack - Torre de Controle Logístico",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS Corporativa Avançada
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #161b22;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        text-align: center;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    pasta = 'archive'
    
    if not os.path.exists(pasta):
        st.error(f"A pasta '{pasta}' não foi encontrada no diretório do projeto.")
        return pd.DataFrame()

    orders = pd.read_csv(os.path.join(pasta, 'olist_orders_dataset.csv'))
    order_items = pd.read_csv(os.path.join(pasta, 'olist_order_items_dataset.csv'))
    products = pd.read_csv(os.path.join(pasta, 'olist_products_dataset.csv'))
    translation = pd.read_csv(os.path.join(pasta, 'product_category_name_translation.csv'))
    customers = pd.read_csv(os.path.join(pasta, 'olist_customers_dataset.csv'))
    
    # Conversão de Datas
    date_columns = [
        'order_purchase_timestamp', 'order_approved_at', 
        'order_delivered_carrier_date', 'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]
    for col in date_columns:
        if col in orders.columns:
            orders[col] = pd.to_datetime(orders[col])
            
    # Mesclagem completa
    df_full = orders.merge(order_items, on='order_id', how='inner')
    df_full = df_full.merge(products, on='product_id', how='left')
    df_full = df_full.merge(translation, on='product_category_name', how='left')
    df_full = df_full.merge(customers, on='customer_id', how='left')
    
    # Categoria limpa
    if 'product_category_name_english' in df_full.columns:
        df_full['categoria'] = df_full['product_category_name_english'].fillna('Outros')
    else:
        df_full['categoria'] = df_full['product_category_name'].fillna('Outros')

    # Métricas Logísticas Chave
    df_full['atrasado'] = df_full['order_delivered_customer_date'] > df_full['order_estimated_delivery_date']
    df_full['otif_status'] = np.where(df_full['atrasado'], 0, 1)
    df_full['lead_time_dias'] = (df_full['order_delivered_customer_date'] - df_full['order_purchase_timestamp']).dt.total_seconds() / 86400.0
    
    df_full['atraso_dias'] = (df_full['order_delivered_customer_date'] - df_full['order_estimated_delivery_date']).dt.total_seconds() / 86400.0
    df_full['atraso_dias'] = df_full['atraso_dias'].apply(lambda x: x if x > 0 else 0)
    
    df_full['valor_total'] = df_full['price'] + df_full['freight_value']
    df_full['ano_mes'] = df_full['order_purchase_timestamp'].dt.to_period('M').astype(str)
    
    return df_full

df = carregar_dados()

if df.empty:
    st.stop()

# --- SIDEBAR PROFISSIONAL COM CHECKBOXES E CONTROLE DE ESTADO ---
st.sidebar.markdown("## 🚚 LogiTrack")
st.sidebar.markdown("**Torre de Controle Executiva**")
st.sidebar.markdown("---")

st.sidebar.markdown("### 🎛️ Filtros Operacionais (Cross-Filtering)")

# --- FILTRO DE CATEGORIAS COM CHECKBOXES ---
with st.sidebar.expander("📦 Filtrar Categorias de Produtos", expanded=True):
    todas_categorias = sorted(df['categoria'].unique())
    
    master_cat_key = "select_all_categorias"
    if master_cat_key not in st.session_state:
        st.session_state[master_cat_key] = True

    def toggle_all_categorias():
        estado_atual = st.session_state[master_cat_key]
        for cat in todas_categorias:
            st.session_state[f"cat_box_{cat}"] = estado_atual

    st.checkbox("Marcar/Desmarcar Todas", value=st.session_state[master_cat_key], key=master_cat_key, on_change=toggle_all_categorias)
    st.markdown("---")

    cat_selecionadas = []
    for cat in todas_categorias:
        box_key = f"cat_box_{cat}"
        if box_key not in st.session_state:
            st.session_state[box_key] = True  
            
        is_checked = st.checkbox(cat, key=box_key)
        if is_checked:
            cat_selecionadas.append(cat)

st.sidebar.markdown("---")

# --- FILTRO DE ESTADOS COM CHECKBOXES ---
with st.sidebar.expander("🗺️ Filtrar Estados (UFs)", expanded=False):
    todos_estados = sorted(df['customer_state'].dropna().unique())
    
    master_uf_key = "select_all_estados"
    if master_uf_key not in st.session_state:
        st.session_state[master_uf_key] = True

    def toggle_all_estados():
        estado_atual = st.session_state[master_uf_key]
        for uf in todos_estados:
            st.session_state[f"uf_box_{uf}"] = estado_atual

    st.checkbox("Marcar/Desmarcar Todos", value=st.session_state[master_uf_key], key=master_uf_key, on_change=toggle_all_estados)
    st.markdown("---")

    uf_selecionadas = []
    for uf in todos_estados:
        box_key = f"uf_box_{uf}"
        if box_key not in st.session_state:
            st.session_state[box_key] = True  
            
        is_checked = st.checkbox(uf, key=box_key)
        if is_checked:
            uf_selecionadas.append(uf)

# Aplicando Filtros globais
df_filtrado = df[df['categoria'].isin(cat_selecionadas) & df['customer_state'].isin(uf_selecionadas)]

# --- HEADER PRINCIPAL ---
st.title("🚚 LogiTrack: Torre de Controle Executiva")
st.markdown("Painel avançado de inteligência logística, auditoria OTIF, análise de perdas e planos de ação.")
st.markdown("---")

if df_filtrado.empty:
    st.warning("⚠️ Selecione pelo menos uma categoria e um estado na barra lateral para exibir os dados analíticos.")
    st.stop()

# --- KPI CARDS EXECUTIVOS ---
total_pedidos = df_filtrado['order_id'].nunique()
faturamento_total = df_filtrado['valor_total'].sum()
otif_medio = (df_filtrado.drop_duplicates(subset=['order_id'])['otif_status'].mean()) * 100
lead_time_medio = df_filtrado['lead_time_dias'].mean()
frete_medio = df_filtrado['freight_value'].mean()
faturamento_atrasado = df_filtrado[df_filtrado['atrasado']]['valor_total'].sum()

k1, k2, k3 = st.columns(3)
k1.metric("📦 Volume de Pedidos", f"{total_pedidos:,}")
k2.metric("💰 Faturamento Total", f"R$ {faturamento_total:,.2f}")
k3.metric("🎯 Índice OTIF (No Prazo)", f"{otif_medio:.1f}%")

st.markdown("")

k4, k5, k6 = st.columns(3)
k4.metric("⏱️ Lead Time Médio", f"{lead_time_medio:.1f} dias")
k5.metric("🚚 Custo Médio de Frete", f"R$ {frete_medio:,.2f}")
k6.metric("⚠️ Receita em Atraso", f"R$ {faturamento_atrasado:,.2f}")

st.markdown("---")

# --- PAINEL DE INSIGHTS ESTRATÉGICOS 100% DINÂMICOS ---
st.subheader("📋 Relatório Executivo: Diagnóstico, Pontos Fortes e Plano de Ação (Diverso por Filtro)")

if not df_filtrado.empty:
    df_order_unique = df_filtrado.drop_duplicates(subset=['order_id'])
    resumo_uf = df_order_unique.groupby('customer_state').agg(
        Total_Pedidos=('order_id', 'count'),
        Taxa_Atraso=('atrasado', 'mean')
    ).reset_index()
    resumo_uf['Taxa_Atraso'] = resumo_uf['Taxa_Atraso'] * 100
    
    top_estado_volume = df_order_unique.groupby('customer_state')['order_id'].count().idxmax() if not df_order_unique.empty else "N/A"
    
    df_atrasos = df_filtrado[df_filtrado['atrasado']].drop_duplicates(subset=['order_id'])
    if not df_atrasos.empty:
        pior_volume_uf = df_atrasos.groupby('customer_state')['order_id'].count().idxmax()
        qtd_abs_atrasos = df_atrasos.groupby('customer_state')['order_id'].count().max()
    else:
        pior_volume_uf = top_estado_volume
        qtd_abs_atrasos = 0
        
    if not resumo_uf.empty:
        pior_perc_row = resumo_uf.loc[resumo_uf['Taxa_Atraso'].idxmax()]
        pior_perc_uf = pior_perc_row['customer_state']
        pior_perc_taxa = pior_perc_row['Taxa_Atraso']
    else:
        pior_perc_uf = "N/A"
        pior_perc_taxa = 0.0
else:
    top_estado_volume, pior_volume_uf, pior_perc_uf, qtd_abs_atrasos, pior_perc_taxa = "N/A", "N/A", "N/A", 0, 0.0

col_inf1, col_inf2 = st.columns(2)

with col_inf1:
    st.info(f"""
    **🏆 Onde Estamos Bem (Pontos Fortes do Escopo Selecionado):**
    1. **Nível de Serviço no Filtro Ativo:** O OTIF atual está em **{otif_medio:.1f}%**, refletindo o comportamento das praças e categorias selecionadas.
    2. **Destaque de Escopo:** O estado de **{top_estado_volume}** concentra o maior volume de pedidos no recorte visualizado neste momento.
    3. **Controle de Custo:** O frete médio praticado no escopo é de **R$ {frete_medio:,.2f}**.
    
    **⚠️ Análise de Perdas e Gargalos (Root Cause):**
    4. **Exposição Financeira Ativa:** **R$ {faturamento_atrasado:,.2f}** imobilizados ou sob risco de estorno devido a prazos estourados no escopo atual.
    5. **O Paradoxo do Volume:** No filtro atual, **{pior_volume_uf}** apresenta o maior número absoluto de ocorrências de atraso ({qtd_abs_atrasos} pedidos).
    """)

with col_inf2:
    st.warning(f"""
    **💡 Sugestões de Melhorias e Plano de Ação (Dinâmico):**
    1. **Rota Crítica do Recorte:** O estado de **{pior_perc_uf}** apresenta a maior taxa relativa de atraso (**{pior_perc_taxa:.1f}%**) entre os filtros ativos. Exige auditoria pontual da transportadora.
    2. **Mitigação de Cauda Longa:** Monitorar pedidos no escopo atual que superem 30 dias de trânsito para evitar reclamações e churn.
    3. **Eficiência Regional:** Avaliar se as praças selecionadas demandam postos avançados de distribuição ou renegociação de SLAs contratuais.
    4. **Compliance Logístico:** Vincular bonificações e penalidades de operadores ao atingimento da meta OTIF do recorte auditado.
    """)

st.markdown("---")

# --- GRÁFICOS ANALÍTICOS (LINHA 1) ---
g1, g2 = st.columns(2)

with g1:
    st.subheader("📊 Top 10 Categorias por Receita (R$)")
    top_cat = df_filtrado.groupby('categoria')['valor_total'].sum().nlargest(10).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=top_cat, x='valor_total', y='categoria', palette='Blues_r', ax=ax)
    ax.set_xlabel("Faturamento Total (R$)", color='white', fontsize=11)
    ax.set_ylabel("Categoria de Produto", color='white', fontsize=11)
    ax.tick_params(colors='white', labelsize=10)
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#161b22')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')
    st.pyplot(fig)

with g2:
    st.subheader("📈 Evolução Mensal do Faturamento")
    evolucao = df_filtrado.groupby('ano_mes')['valor_total'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=evolucao, x='ano_mes', y='valor_total', marker='o', color='#2ecc71', linewidth=2.5, ax=ax)
    plt.xticks(rotation=45)
    ax.set_xlabel("Ano-Mês", color='white', fontsize=11)
    ax.set_ylabel("Faturamento (R$)", color='white', fontsize=11)
    ax.tick_params(colors='white', labelsize=10)
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#161b22')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')
    st.pyplot(fig)

st.markdown("---")

# --- GRÁFICOS ANALÍTICOS (LINHA 2) ---
g3, g4 = st.columns(2)

with g3:
    st.subheader("⏱️ Distribuição do Lead Time (Dias)")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(df_filtrado['lead_time_dias'].dropna(), bins=30, kde=True, color='#3498db', ax=ax)
    ax.set_xlabel("Dias da Compra até a Entrega", color='white', fontsize=11)
    ax.set_ylabel("Volume de Pedidos", color='white', fontsize=11)
    ax.tick_params(colors='white', labelsize=10)
    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#161b22')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')
    st.pyplot(fig)

with g4:
    st.subheader("📦 Status de Entrega (No Prazo vs Atrasado)")
    status_counts = df_filtrado.drop_duplicates(subset=['order_id'])['atrasado'].map({False: 'No Prazo', True: 'Atrasado'}).value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(
        status_counts, 
        labels=status_counts.index, 
        autopct='%1.1f%%', 
        colors=['#2ecc71', '#e74c3c'], 
        startangle=90, 
        textprops={'color': 'white', 'fontsize': 12}
    )
    fig.patch.set_facecolor('#0e1117')
    st.pyplot(fig)

st.markdown("---")

# --- TABELA ANALÍTICA POR ESTADO (COMPLETA E COM FILTRO INTERATIVO) ---
st.subheader("🗺️ Tabela Analítica Completa de Desempenho por Estado")
st.markdown("Visualize todos os estados atendidos, ordene por qualquer coluna ou utilize o filtro rápido abaixo.")

todos_ufs_disponiveis = sorted(df_filtrado['customer_state'].dropna().unique())
filtro_tabela_uf = st.multiselect(
    "🔍 Filtrar Estados na Tabela:",
    options=todos_ufs_disponiveis,
    default=todos_ufs_disponiveis
)

estado_perf = df_filtrado.groupby('customer_state').agg(
    Total_Pedidos=('order_id', 'nunique'),
    Faturamento_Total=('valor_total', 'sum'),
    Lead_Time_Medio=('lead_time_dias', 'mean'),
    Taxa_Atraso=('atrasado', 'mean')
).reset_index()

estado_perf['Taxa_Atraso'] = estado_perf['Taxa_Atraso'] * 100

if filtro_tabela_uf:
    estado_perf = estado_perf[estado_perf['customer_state'].isin(filtro_tabela_uf)]

estado_perf = estado_perf.sort_values(by='Total_Pedidos', ascending=False)

st.dataframe(estado_perf.style.format({
    'Faturamento_Total': 'R$ {:,.2f}',
    'Lead_Time_Medio': '{:.1f} dias',
    'Taxa_Atraso': '{:.2f}%',
    'Total_Pedidos': '{:,}'
}), use_container_width=True, height=400)

st.markdown("---")

# --- SEÇÃO DE EXPORTAÇÃO DE DADOS (XLSX, CSV, TXT) ---
st.subheader("📥 Central de Exportação de Relatórios")
st.markdown("Baixe os dados consolidados do escopo atual nos formatos corporativos abaixo:")

col_exp1, col_exp2, col_exp3 = st.columns(3)

# 1. Exportação XLSX (Excel)
with col_exp1:
    output_xlsx = io.BytesIO()
    with pd.ExcelWriter(output_xlsx, engine='openpyxl') as writer:
        estado_perf.to_excel(writer, index=False, sheet_name='Desempenho_Estados')
    xlsx_data = output_xlsx.getvalue()
    
    st.download_button(
        label="📥 Baixar Planilha (.xlsx)",
        data=xlsx_data,
        file_name="LogiTrack_Relatorio_Desempenho.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# 2. Exportação CSV
with col_exp2:
    csv_data = estado_perf.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Baixar Dados (.csv)",
        data=csv_data,
        file_name="LogiTrack_Relatorio_Desempenho.csv",
        mime="text/csv",
        use_container_width=True
    )

# 3. Exportação TXT (Relatório Textual de Indicadores)
with col_exp3:
    txt_content = f"""=== RELATÓRIO EXECUTIVO LOGITRACK ===
Volume de Pedidos Analisados: {total_pedidos:,}
Faturamento Total: R$ {faturamento_total:,.2f}
Índice OTIF Global: {otif_medio:.1f}%
Lead Time Médio: {lead_time_medio:.1f} dias
Frete Médio: R$ {frete_medio:,.2f}
Receita em Risco (Atrasada): R$ {faturamento_atrasado:,.2f}
Estado com Maior Volume de Atrasos: {pior_volume_uf}
Estado com Maior Taxa de Atraso Relativa: {pior_perc_uf} ({pior_perc_taxa:.1f}%)
=====================================
"""
    st.download_button(
        label="📋 Baixar Resumo (.txt)",
        data=txt_content,
        file_name="LogiTrack_Resumo_Executivo.txt",
        mime="text/plain",
        use_container_width=True
    )

# Rodapé
st.markdown("---")
st.markdown("👨‍💻 *LogiTrack Control Tower — Desenvolvido com Python, Streamlit e Pandas para Portfólio Executivo.*")
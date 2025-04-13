import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Sales Dashboard", layout="wide")
# st.title("📊 Sales Dashboard")
#cabecalho visual
st.markdown("""
    <h1 style='text-align: center; color: #6C63FF; font-size: 40px;'>
        🛍️ Sales Dashboard - Análise Trimestral de Vendas
    </h1>
    <p style='text-align: center; color: gray; font-size: 16px;'>
        Acompanhe métricas, visualize desempenho por categoria, região e período com insights interativos.
    </p>
""", unsafe_allow_html=True)
st.markdown("---")


# Upload do arquivo CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📌 Colunas no DataFrame:", df.columns.tolist())
    df['Date']= pd.to_datetime(df['Date'])
    df['Month']= df['Date'].dt.month

    #filtros laterais
    st.sidebar.header('🔎 Filters')

    region_filter = st.sidebar.multiselect(
        'Select Region(s):',
        options=df['Region'].unique(),
        default=df['Region'].unique()
    )

    category_filter = st.sidebar.multiselect(
        'Select Category(s):',
        options= df['Category'].unique(),
        default= df['Category'].unique()
    )
    # Mostrar dados brutos
    st.subheader("Raw Data")
    st.dataframe(df)

    # Filtro por data
    df["Date"] = pd.to_datetime(df["Date"])
    start = st.date_input("Start Date", df["Date"].min())
    end = st.date_input("End Date", df["Date"].max())

    # Filtrar DataFrame por intervalo de datas
    #df_filtered = df[(df["Date"] >= pd.to_datetime(start)) & (df["Date"] <= pd.to_datetime(end))]
    df_filtered = df[
        (df['Date'] >= pd.to_datetime(start)) &
        (df['Date'] <= pd.to_datetime(end)) &
        (df['Region'].isin(region_filter)) &
        (df['Category'].isin(category_filter))
    ]

    # ----- ANTIGA VERSÃO DAS MÉTRICAS (mantida para referência) -----
    #total_sales = df_filtered["Total"].sum()
    #avg_ticket = df_filtered["Total"].mean()
    #st.metric("Total Sales", f"${total_sales:,.2f}")
    #st.metric("Average Ticket", f"${avg_ticket:,.2f}")

    # KPIs com layout em colunas (versao antes de atualizar para ficar mais moderno)
    #total_sales = df_filtered['Total'].sum()
   # avg_ticket = df_filtered['Total'].mean()
    #total_units = df_filtered['Quantity'].sum()
    #total_orders = len(df_filtered)

    #col1, col2, col3, col4 = st.columns(4)
    #with col1:
    #    st.metric('💰 Total Sales', f'${total_sales:.2f}')
    #with col2:
    #    st.metric('🧾 Avg. Ticket', f'${avg_ticket:.2f}')
    #with col3:
    #    st.metric('📦 Units Sold', int(total_units))
    #with col4:
    #   st.metric('🛍️ Transactions', total_orders)

    # KPIs com meta e análise comparativa
    df_filtered["Month"] = pd.to_datetime(df_filtered["Date"]).dt.month

    # Total do mês atual (último mês no filtro)
    current_month = df_filtered["Month"].max()
    previous_month = current_month - 1

    total_current = df_filtered[df_filtered["Month"] == current_month]["Total"].sum()
    total_previous = df_filtered[df_filtered["Month"] == previous_month]["Total"].sum()

    # Crescimento percentual
    growth = ((total_current - total_previous) / total_previous) * 100 if total_previous != 0 else 0

    # Simulando meta
    meta = 25000  # valor fictício
    percent_meta = (total_current / meta) * 100

    # Melhor mês
    month_names = {1: "jan", 2: "fev", 3: "mar", 4: "abr", 5: "mai", 6: "jun", 7: "jul", 8: "ago", 9: "set", 10: "out",
                   11: "nov", 12: "dez"}
    best_month = df_filtered.groupby("Month")["Total"].sum().idxmax()

    st.markdown("### 📌 **Indicadores Principais**")
    col1, col2, col3 = st.columns(3)



    #Exibir os KPis com estilo
    #alterando o estilo dos KPI's
    avg_ticket = df_filtered['Total'].mean()
    total_units = df_filtered['Quantity'].sum()
    '''with col1:
        st.metric(
            label="💰 Faturamento",
            value=f"R$ {total_current:,.2f}".replace(",", "."),
            delta=f"{growth:.1f}%" if growth >= 0 else f"-{abs(growth):.1f}%",
            delta_color="normal" if growth >= 0 else "inverse"
        )
        st.caption(f"Melhor mês: {month_names[best_month]}")

        st.progress(min(percent_meta / 100, 1.0), text=f"Meta: {percent_meta:.1f}%")

    with col2:
        avg_ticket = df_filtered["Total"].mean()
        st.metric("🧾 Ticket Médio", f"R$ {avg_ticket:,.2f}".replace(",", "."))

    with col3:
        total_units = df_filtered["Quantity"].sum()
        st.metric("📦 Quantidade Vendida", int(total_units))'''

    st.markdown("### 🔢 Indicadores Principais")

    with st.container():
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**💰 Faturamento Atual**")
            st.markdown(f"<h2 style='color:#00BFA6;'>R$ {total_current:,.2f}</h2>", unsafe_allow_html=True)
            st.caption(f"Meta: {percent_meta:.1f}%")
            st.progress(min(percent_meta / 100, 1.0))

        with col2:
            st.markdown("**📦 Unidades Vendidas**")
            st.markdown(f"<h2 style='color:#4CAF50;'>{int(total_units)}</h2>", unsafe_allow_html=True)

        with col3:
            cor = "#6C63FF" if growth >= 0 else "#FF5252"
            prefixo = "+" if growth >= 0 else "-"
            st.markdown("**📈 Crescimento Mensal**")
            st.markdown(f"<h2 style='color:{cor};'>{prefixo}{abs(growth):.1f}%</h2>", unsafe_allow_html=True)

    # indicado de margem bruta
        gross_margin = df_filtered["Gross Margin"].sum()
        with st.container():
            st.markdown("### 📊 Indicador Extra")
            st.metric("💼 Margem Bruta", f"R$ {gross_margin:,.2f}".replace(",", "."))

    # === ⬇⬇⬇ INSERIR AQUI O BLOCO DE PREVISÃO DE VENDAS COM ML ⬇⬇⬇ ===

    import joblib

    # Tenta carregar e prever
    try:
        model = joblib.load('modelos/modelo_vendas.pkl')  # Caminho exato onde o modelo foi salvo
        X_pred = df_filtered[["Quantity", "Unit Price"]]

        predictions = model.predict(X_pred)
        previsao_total = predictions.sum()

        st.markdown("### 🤖 Previsão com Machine Learning")
        st.success(f"🔮 Previsão Total com base no modelo: **R$ {previsao_total:,.2f}**".replace(",", "."))

    except Exception as e:
        st.warning(f"Erro ao carregar ou prever com o modelo: {e}")

    # === ⬆⬆⬆ FIM DO BLOCO DE PREVISÃO ⬆⬆⬆ ===

    # KPi's Faturamento ao longo do tempo

    st.markdown("---")
    st.markdown("### 📅 Faturamento ao longo do tempo")

    fig4, ax4 = plt.subplots()
    df_filtered.groupby(df_filtered["Date"].dt.to_period("M"))["Total"].sum().sort_index().plot(kind="bar", ax=ax4,
                                                                                                color="#6C63FF")
    ax4.set_ylabel("Total Sales")
    ax4.set_xlabel("Mês")
    ax4.set_title("Faturamento Mensal")
    st.pyplot(fig4)

    # Ranking dos Vendedores

    st.markdown("---")
    st.markdown("### 🏆 Top Vendedores")

    top_sellers = df_filtered.groupby("Seller")["Total"].sum().sort_values(ascending=False).head(5)
    fig5, ax5 = plt.subplots()
    top_sellers.plot(kind="barh", ax=ax5, color="deepskyblue")
    ax5.set_xlabel("Faturamento Total")
    ax5.invert_yaxis()  # Coloca o maior no topo
    st.pyplot(fig5)


    # Gráfico de vendas por produto
    st.markdown('---')
    st.markdown("### 📊 Sales by Product")
    with st.container():
        fig, ax = plt.subplots()
        df_filtered.groupby("Product")["Total"].sum().plot(kind="bar", ax=ax, color="skyblue")
        ax.set_ylabel("Total Sales")
        st.pyplot(fig)

    # Gráfico de vendas por categoria
    st.markdown('---')
    st.markdown("Sales by Category")
    with st.container():
        fig2, ax2 = plt.subplots()
        df_filtered.groupby("Category")["Total"].sum().sort_values().plot(kind="barh", ax=ax2, color="coral")
        ax2.set_xlabel("Total Sales")
        st.pyplot(fig2)

    # Grafico vendas por produto
    st.markdown("---")
    st.markdown("Sales by Region")
    with st.container():
        fig3, ax3 = plt.subplots()
        df_filtered.groupby("Region")["Total"].sum().sort_values(ascending=False).plot(kind="bar", ax=ax3,
                                                                                   color="mediumseagreen")
        ax3.set_ylabel("Total Sales")
        ax3.set_title("Total Sales per Region")
        st.pyplot(fig3)





import streamlit as st
import pandas as pd
import plotly.express as px

# === Config da página ===
st.set_page_config(
    page_title="NBA Dashboard",
    layout="wide"
)

# === CSS Custom ===
st.markdown("""
<style>
body {background-color: #0F172A; color: #E2E8F0;}
h1, h2, h3 {color: #38BDF8;}
.sidebar .sidebar-content {background-color: #1E293B;}
div[data-testid="stMetricValue"] {color: #38BDF8;}
</style>
""", unsafe_allow_html=True)

# === Carregar dados ===
@st.cache_data
def load_data():
    df = pd.read_csv('../data/nba_clean.csv')
    return df

df = load_data()

# === Sidebar ===
st.sidebar.header("Filtros")

teams = sorted(df['Team'].unique())
seasons = sorted(df['Season'].unique())

selected_team = st.sidebar.selectbox("Selecione o Time:", teams)
selected_season = st.sidebar.selectbox("Selecione o Ano:", seasons)
selected_metric = st.sidebar.selectbox(
    "Selecione a Métrica:",
    ['PTS', 'AST', 'TRB', 'FG_Percent', '3P_Percent', 'FT_Percent']
)

filtered_df = df[df['Team'] == selected_team]

# === Cabeçalho ===
st.title("NBA Team Performance Dashboard")
st.markdown("Visualize e compare estatísticas de desempenho de times da NBA (2000–2023).")

# === KPIs ===
current_row = filtered_df[filtered_df['Season'] == selected_season]

colk1, colk2, colk3 = st.columns(3)
colk1.metric("Pontos", f"{float(current_row['PTS']):.1f}" if not current_row.empty else "–")
colk2.metric("Assistências", f"{float(current_row['AST']):.1f}" if not current_row.empty else "–")
colk3.metric("Rebotes", f"{float(current_row['TRB']):.1f}" if not current_row.empty else "–")

st.markdown("---")

# === Gráficos ===
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        filtered_df,
        x='Season',
        y=selected_metric,
        title=f"Evolução de {selected_metric} - {selected_team}",
        markers=True,
        template='plotly_dark',
        color_discrete_sequence=['#38BDF8']
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    season_df = df[df['Season'] == selected_season]
    fig2 = px.bar(
        season_df,
        x='Team',
        y=selected_metric,
        title=f"Comparativo entre Times ({selected_season})",
        color='Team',
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)

# === Tabela Final ===
st.markdown("### Estatísticas Resumidas")
st.dataframe(
    filtered_df[['Season', 'PTS', 'AST', 'TRB', 'FG_Percent']],
    use_container_width=True
)

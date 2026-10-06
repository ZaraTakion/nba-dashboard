"""Interactive historical NBA team statistics dashboard."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from app.data_utils import DATA_PATH, load_data


st.set_page_config(
    page_title="NBA | Temporada por temporada",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)

METRICS = {
    "Pontos por jogo": "PTS",
    "Assistências por jogo": "AST",
    "Rebotes por jogo": "TRB",
    "Roubos por jogo": "STL",
    "Tocos por jogo": "BLK",
    "Turnovers por jogo": "TOV",
    "Aproveitamento de arremessos (%)": "FG_Percent",
    "Aproveitamento de 3 pontos (%)": "3P_Percent",
    "Aproveitamento de 2 pontos (%)": "2P_Percent",
    "Aproveitamento de lances livres (%)": "FT_Percent",
}
PERCENT_METRICS = {"FG_Percent", "3P_Percent", "2P_Percent", "FT_Percent"}
ACCENT = "#57D5C8"
MUTED = "#52647C"
TEXT = "#E8EEF7"


@st.cache_data(show_spinner="Carregando estatísticas históricas…")
def get_data():
    return load_data(DATA_PATH)


try:
    data = get_data()
except (FileNotFoundError, ValueError, OSError) as error:
    st.error(f"Não foi possível carregar os dados da NBA: {error}")
    st.stop()

team_data = data.loc[~data["Is_League_Average"]].copy()
league_data = data.loc[data["Is_League_Average"]].copy()
franchises = sorted(team_data["Franchise"].unique().tolist())
seasons = sorted(team_data["Season"].unique().tolist())

st.title("NBA — temporada por temporada")
st.write(
    "Explore estatísticas médias por equipe, acompanhe uma franquia ao longo do "
    "tempo e compare seu desempenho com as demais equipes da temporada."
)
st.caption(
    f"Recorte histórico estático: {min(seasons)}–{max(seasons)}. "
    "Os dados não são atualizados em tempo real. Percentuais são exibidos como porcentagens."
)

with st.sidebar:
    st.header("Filtros")
    selected_franchise = st.selectbox("Franquia", franchises)
    selected_season = st.selectbox("Temporada", seasons, index=len(seasons) - 1)
    selected_metric_label = st.selectbox("Indicador", list(METRICS))
    selected_metric = METRICS[selected_metric_label]
    playoff_only = st.checkbox("Comparar apenas equipes marcadas com *", value=False)
    st.caption(
        "O asterisco é preservado exatamente como marcador presente na fonte. "
        "Nomes históricos são agrupados na franquia atual; o nome original aparece nos detalhes."
    )

hover_value_format = ":.1%" if selected_metric in PERCENT_METRICS else ":.1f"

season_rows = team_data.loc[team_data["Season"].eq(selected_season)].copy()
if playoff_only:
    comparison_rows = season_rows.loc[season_rows["Playoffs"]].copy()
else:
    comparison_rows = season_rows.copy()

selected_history = team_data.loc[team_data["Franchise"].eq(selected_franchise)].sort_values("Season")
selected_row = selected_history.loc[selected_history["Season"].eq(selected_season)]

if selected_row.empty:
    st.info("Não há registro dessa franquia na temporada selecionada.")
else:
    values = selected_row.iloc[0]
    kpi_columns = st.columns(3)
    for column, label, field in zip(
        kpi_columns,
        ("Pontos por jogo", "Assistências por jogo", "Rebotes por jogo"),
        ("PTS", "AST", "TRB"),
    ):
        column.metric(label, f"{values[field]:.1f}")

    st.subheader(f"{selected_franchise} em {selected_season}")
    st.caption(
        "As estatísticas principais são médias por jogo. O nome histórico e o marcador * "
        "da fonte podem ser consultados na tabela da temporada."
    )

    history_column, comparison_column = st.columns((1, 1.15), gap="large")

    with history_column:
        st.markdown("#### Evolução histórica")
        history_figure = go.Figure()
        marker_symbols = ["star" if flag else "circle" for flag in selected_history["Playoffs"]]
        history_figure.add_trace(
            go.Scatter(
                x=selected_history["Season"],
                y=selected_history[selected_metric],
                mode="lines+markers",
                name=selected_franchise,
                line={"color": ACCENT, "width": 3},
                marker={"color": ACCENT, "size": 9, "symbol": marker_symbols},
                customdata=selected_history[["Source_Team", "Playoffs"]].to_numpy(),
                hovertemplate=(
                    f"Temporada: %{{x}}<br>Valor: %{{y{hover_value_format}}}<br>"
                    "Nome na base: %{customdata[0]}<br>"
                    "Marcador *: %{customdata[1]}<extra></extra>"
                ),
            )
        )
        history_average = league_data.loc[league_data["Season"].isin(selected_history["Season"])]
        if not history_average.empty:
            history_figure.add_trace(
                go.Scatter(
                    x=history_average["Season"],
                    y=history_average[selected_metric],
                    mode="lines",
                    name="Média da liga (fonte)",
                    line={"color": MUTED, "width": 2, "dash": "dash"},
                    hovertemplate=(
                        f"Temporada: %{{x}}<br>Média da liga: "
                        f"%{{y{hover_value_format}}}<extra></extra>"
                    ),
                )
            )
        history_figure.update_layout(
            template="plotly_dark",
            height=390,
            margin={"l": 8, "r": 12, "t": 18, "b": 8},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": TEXT},
            legend={"orientation": "h", "y": 1.12, "x": 0},
            hovermode="x unified",
        )
        history_figure.update_xaxes(title="Temporada", dtick=2, gridcolor="#24344A")
        history_figure.update_yaxes(
            title=selected_metric_label,
            tickformat=".0%" if selected_metric in PERCENT_METRICS else ".1f",
            gridcolor="#24344A",
        )
        st.plotly_chart(
            history_figure,
            width="stretch",
            alt=f"Evolução histórica de {selected_metric_label.lower()} para {selected_franchise}, com temporadas e média da liga quando disponível.",
        )
        st.caption(
            f"O gráfico mostra {selected_metric_label.lower()} de {selected_franchise} "
            "por temporada; estrelas identificam linhas com * na fonte."
        )

    with comparison_column:
        st.markdown("#### Comparação entre equipes")
        comparison_rows = comparison_rows.sort_values(selected_metric, ascending=True)
        labels = comparison_rows["Franchise"].tolist()
        values_for_chart = comparison_rows[selected_metric].tolist()
        source_names = comparison_rows["Source_Team"].tolist()
        playoff_flags = comparison_rows["Playoffs"].tolist()
        colors = [ACCENT if name == selected_franchise else MUTED for name in labels]
        chart_text = ["Selecionada" if name == selected_franchise else "" for name in labels]

        comparison_figure = go.Figure(
            go.Bar(
                x=values_for_chart,
                y=labels,
                orientation="h",
                marker_color=colors,
                text=chart_text,
                textposition="outside",
                cliponaxis=False,
                customdata=list(zip(source_names, playoff_flags)),
                hovertemplate=(
                    f"Franquia: %{{y}}<br>Valor: %{{x{hover_value_format}}}<br>"
                    "Nome na base: %{customdata[0]}<br>"
                    "Marcador *: %{customdata[1]}<extra></extra>"
                ),
            )
        )
        season_average = league_data.loc[league_data["Season"].eq(selected_season)]
        if not season_average.empty:
            average_value = season_average.iloc[0][selected_metric]
            comparison_figure.add_vline(
                x=average_value,
                line_color="#F3C969",
                line_dash="dash",
                annotation_text="Média da liga",
                annotation_position="top right",
            )
        comparison_figure.update_layout(
            template="plotly_dark",
            height=max(390, 23 * len(comparison_rows) + 90),
            margin={"l": 8, "r": 56, "t": 18, "b": 8},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": TEXT},
            showlegend=False,
        )
        comparison_figure.update_xaxes(
            title=selected_metric_label,
            tickformat=".0%" if selected_metric in PERCENT_METRICS else ".1f",
            gridcolor="#24344A",
        )
        comparison_figure.update_yaxes(title=None, gridcolor="#24344A")
        st.plotly_chart(
            comparison_figure,
            width="stretch",
            alt=f"Comparação de {selected_metric_label.lower()} entre as equipes na temporada {selected_season}.",
        )
        if season_average.empty:
            st.caption(
                "A fonte não fornece uma linha de média da liga para esta temporada; "
                "por isso, nenhuma referência oficial é desenhada."
            )
        else:
            st.caption(
                "A linha pontilhada representa a média da liga publicada junto aos dados. "
                "A cor e o rótulo identificam a franquia selecionada."
            )

    st.markdown("#### Dados da temporada")
    table_rows = comparison_rows.sort_values(selected_metric, ascending=False).copy()
    table_rows.insert(
        0,
        "Seleção",
        table_rows["Franchise"].map(
            lambda name: "Franquia selecionada" if name == selected_franchise else ""
        ),
    )
    table_rows = table_rows.rename(
        columns={
            "Franchise": "Franquia",
            "Source_Team": "Nome na fonte",
            "Season": "Temporada",
            "Playoffs": "Marcador *",
            "PTS": "Pontos/jogo",
            "AST": "Assistências/jogo",
            "TRB": "Rebotes/jogo",
            "STL": "Roubos/jogo",
            "BLK": "Tocos/jogo",
            "TOV": "Turnovers/jogo",
            "FG_Percent": "Arremessos (%)",
            "3P_Percent": "3 pontos (%)",
            "2P_Percent": "2 pontos (%)",
            "FT_Percent": "Lances livres (%)",
        }
    )
    percent_display_columns = (
        "Arremessos (%)",
        "3 pontos (%)",
        "2 pontos (%)",
        "Lances livres (%)",
    )
    for column in percent_display_columns:
        if column in table_rows:
            table_rows[column] = table_rows[column].map(lambda value: f"{value:.1%}")
    visible_columns = [
        "Seleção",
        "Franquia",
        "Nome na fonte",
        "Marcador *",
        "Pontos/jogo",
        "Assistências/jogo",
        "Rebotes/jogo",
        "Arremessos (%)",
        "3 pontos (%)",
        "2 pontos (%)",
        "Lances livres (%)",
    ]
    st.dataframe(
        table_rows[visible_columns],
        hide_index=True,
        width="stretch",
    )

st.divider()
st.markdown(
    "**Fonte dos dados:** [NBA Team Stats 2000–2023 no Kaggle]"
    "(https://www.kaggle.com/datasets/bluedreamv1b3/nba-teams-stat-2000-2023). "
    "Este painel apresenta um recorte histórico e não é afiliado à NBA."
)

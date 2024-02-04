from typing import Any, Dict

import extra_streamlit_components as stx
import pandas as pd
import plotly
import plotly.graph_objects as go
import riskfolio as rp
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots


def mostrar_tab_estatisticas(df_tela):
    st.write("#### Estatísticas")
    df_stats = pd.DataFrame()
    df_stats["Menor valor"] = df_tela.min(numeric_only=True)
    df_stats["Valor médio"] = df_tela.mean(numeric_only=True)
    df_stats["Desvio padrão"] = df_tela.std(numeric_only=True)
    df_stats["Maior valor"] = df_tela.max(numeric_only=True)

    st.write(df_stats)


def mostrar_tab_graficos(df, titulo, graficos, numero_colunas, numero_linhas):
    fig = make_subplots(
        rows=numero_linhas, cols=numero_colunas, subplot_titles=graficos
    )

    col_atual = 1
    row_atual = 1

    for g in graficos:
        fig.add_trace(
            go.Bar(x=df.index, y=df[g], name=g),
            row=row_atual,
            col=col_atual,
        )
        fig.add_hline(
            y=df[g].mean(),
            line_dash="dot",
            annotation_text="Média",
            annotation_position="bottom right",
            row=row_atual,
            col=col_atual,
        )

        if col_atual == numero_colunas:
            row_atual += 1
            col_atual = 1
        else:
            col_atual += 1

    fig.update_layout(
        height=800,
        width=1200,
        title_text=titulo,
    )

    st.plotly_chart(fig)


def mostrar_tab_resultados(df):
    st.write("#### " + str(df.count().unique()[0]) + " registros retornados")
    st.write(df)


def retonar_item_filtro(
    df, coluna: str, label: str, widget: str, ajuda=None, formato=None
) -> Dict[str, Any]:
    if coluna not in df.columns:
        st.error(f"Coluna {coluna} não existe no DataFrame")
        st.stop()

    if widget is None:
        widget = "slider"

    if widget.lower() not in ["slider", "input_number"]:
        st.error(f"Widget {widget} não é slider ou input_number")
        st.stop()

    menor = float(df[coluna].min(numeric_only=True))
    maior = float(df[coluna].max(numeric_only=True))

    if widget == "slider":
        filtro_min, filtro_max = st.slider(
            label,
            menor,
            maior,
            (menor, maior),
            step=1.0,
            format=formato,
            help=ajuda,
            key=f"{coluna}{label}_slider",
        )

    else:
        col_min, col_max = st.columns(2)
        with col_min:
            filtro_min = st.number_input(
                f"{label} mínimo",
                min_value=menor,
                value=menor,
                step=1.0,
                key=f"{coluna}{label}_min",
            )
        with col_max:
            filtro_max = st.number_input(
                f"{label} máximo",
                max_value=maior,
                value=maior,
                step=1.0,
                help=ajuda,
                key=f"{coluna}{label}_max",
            )

    return {
        "minimo": filtro_min,
        "maximo": filtro_max,
    }


def is_dados_carregados():
    return "lista_fiis" in st.session_state and "lista_acoes" in st.session_state


def mostrar_tab_detalhes():
    tab_detalhes = stx.tab_bar(
        data=[
            stx.TabBarItemData(
                id="tab_resultados",
                title="Resultados",
                description="Resultados",
            ),
            stx.TabBarItemData(
                id="tab_estatisticas",
                title="Estatísticas",
                description="Estatísticas",
            ),
            stx.TabBarItemData(
                id="tab_graficos",
                title="Gráficos",
                description="Gráficos",
            ),
        ],
        default="tab_resultados",
        key="tab_detalhes",
    )

    return tab_detalhes


def mostrar_tab_markowitz(df):
    if len(df) > 15:
        st.error("Muitos ativos...")
        st.stop()

    ativos = [item.strip() + ".SA" for item in df.index]
    # yf.enable_debug_mode()
    carteira = yf.download(ativos, start="2023-01-01", ignore_tz=True)["Adj Close"]

    # pd.DataFrame()
    # for i in ativos:
    #     try:
    #         carteira[i] = yf.download(i, start="2023-01-01", ignore_tz=True)[
    #             "Adj Close"
    #         ]
    #     except Exception:
    #         print(f"{i} não encontrado no YFinance")

    # print(carteira)
    retornos = carteira.pct_change().dropna()
    portfolio = rp.Portfolio(returns=retornos)
    # plotly.plot(retornos.T, alpha=0.4)

    mu = "hist"  # estimando os retornos com base no histórico
    cov = "hist"  # estimar a matriz de covariância através do histórico

    portfolio.assets_stats(method_mu=mu, method_cov=cov, d=0.94)

    # Construindo o modelo

    model = "Classic"
    rm = "MV"
    obj = "Sharpe"
    hist = True
    rf = 0
    l = 0

    w = portfolio.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

    st.write(w.T)

    ax = rp.plot_pie(
        w=w,
        title="Otimização de Portfólio",
        others=0.01,
        nrow=25,
        cmap="tab20",
        height=8,
        width=10,
        ax=None,
    )

    st.write(ax.figure, width=600)

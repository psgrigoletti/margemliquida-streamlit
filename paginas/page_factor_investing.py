import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
import pandas as pd
from libs.market_data.fundamentus.lista import get_df_acoes, get_df_fiis
import extra_streamlit_components as stx
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@st.cache_data(show_spinner="Buscando dados fundamentalistas para ações.", ttl=3600)
def busca_dados_acoes():
    df = get_df_acoes()
    df = df[df["Div.Yield"] > 0]
    df = df[df["Cotação"] > 0]
    df = df[df["Liq. Corr."] > 0]
    df = df[df["Liq.2meses"] > 0]
    st.session_state["lista_acoes"] = df
    return df


@st.cache_data(show_spinner="Buscando dados fundamentalistas para FIIs.", ttl=3600)
def busca_dados_fiis():
    df = get_df_fiis()
    df = df[df["Dividend Yield"] > 0]
    df = df[df["Cotação"] > 0]
    df = df[df["Liquidez"] > 0]
    st.session_state["lista_fiis"] = df
    return df


def busca_df_fiis_do_cache():
    if "lista_fiis" not in st.session_state:
        df = busca_dados_fiis()
        st.session_state["lista_fiis"] = df
    else:
        df = st.session_state["lista_fiis"]
    return df


def busca_df_acoes_do_cache():
    if "lista_acoes" not in st.session_state:
        df = busca_dados_acoes()
        st.session_state["lista_acoes"] = df
    else:
        df = st.session_state["lista_acoes"]
    return df


def is_dados_carregados():
    return "lista_fiis" in st.session_state and "lista_acoes" in st.session_state


def mostrar_tab_fiis():
    st.write("## FIIs")
    st.markdown("**Filtros iniciais:** Dividend Yield > 0; Cotação > 0; Liquidez > 0")

    filtros = {}

    with st.form("form_fiis"):
        mostrar_filtros_fiis(filtros)
        filtrar_fiis = st.form_submit_button("Filtrar")

    if filtrar_fiis:
        df_fiis_tela = filtrar_df_fiis(filtros)

        tab_detalhes_1, tab_detalhes_2, tab_detalhes_3, tab_detalhes_4 = st.tabs(
            [
                ":memo: Resultados",
                ":bar_chart: Gráficos",
                ":straight_ruler: Estatísticas",
                ":magic_wand: Fórmula Mágica",
            ]
        )

        with tab_detalhes_1:
            mostrar_tab_resultados(df_fiis_tela)

            acoes = [i + ".SA" for i in df_fiis_tela.index]
            pd.options.plotting.backend = "plotly"

            df_fechamento = yf.download(acoes, "2022-01-01")
            df_fechamento = df_fechamento / df_fechamento.iloc[1]
            fig = df_fechamento["Adj Close"].plot()
            st.plotly_chart(fig, use_container_width=True)

        with tab_detalhes_2:
            titulo = "Gráficos sobre os FIIs selecionados"
            graficos = [
                "Cotação",
                "Dividend Yield",
                "P/VP",
                "Valor de Mercado",
                "Liquidez",
            ]

            mostrar_tab_graficos(df_fiis_tela, titulo, graficos, 3, 2)

        with tab_detalhes_3:
            mostrar_tab_estatisticas(df_fiis_tela)

        with tab_detalhes_4:
            mostrar_tab_magic_formula_fiis(df_fiis_tela)


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


def mostrar_tab_magic_formula_acoes(
    df,
):
    manter = ["ROIC", "EV/EBIT"]
    remover = [col for col in df.columns if col not in manter]
    df = df.drop(remover, axis=1)

    df["EV/EBIT"] = df["EV/EBIT"].astype(float)
    df = df[df["EV/EBIT"] > 0]
    df = df.sort_values(by="EV/EBIT", ascending=True)
    df["Ranking EV/EBIT"] = range(1, len(df) + 1)

    df["ROIC"] = df["ROIC"].astype(float)
    df = df[df["ROIC"] > 0]
    df = df.sort_values(by="ROIC", ascending=False)
    df["Ranking ROIC"] = range(1, len(df) + 1)

    df["Magic Formula"] = df["Ranking EV/EBIT"] + df["Ranking ROIC"]
    df["Ranking Magic Formula"] = range(1, len(df) + 1)
    df = df.sort_values("Ranking Magic Formula", ascending=True)

    col1, col2 = st.columns([2, 6])
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        col1.image("imagens/livro-formula-magica.jpeg", width=250)
    with col2:
        st.write("#### " + str(df.count().unique()[0]) + " registros retornados")
        st.data_editor(
            df,
        )


def mostrar_tab_magic_formula_fiis(
    df,
):
    manter = ["Dividend Yield", "P/VP"]
    remover = [col for col in df.columns if col not in manter]
    df = df.drop(remover, axis=1)

    df["Dividend Yield"] = df["Dividend Yield"].astype(float)
    df = df[df["Dividend Yield"] > 0]
    df = df.sort_values(by="Dividend Yield", ascending=False)
    df["Ranking Dividend Yield"] = range(1, len(df) + 1)

    df["P/VP"] = df["P/VP"].astype(float)
    df = df[df["P/VP"] > 0]
    df = df.sort_values(by="P/VP", ascending=True)
    df["Ranking P/VP"] = range(1, len(df) + 1)

    df["Magic Formula"] = df["Ranking Dividend Yield"] + df["Ranking P/VP"]
    df["Ranking Magic Formula"] = range(1, len(df) + 1)
    df = df.sort_values("Ranking Magic Formula", ascending=True)

    col1, col2 = st.columns([2, 6])
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        col1.image("imagens/livro-formula-magica.jpeg", width=250)
    with col2:
        st.write("#### " + str(df.count().unique()[0]) + " registros retornados")
        st.data_editor(
            df,
            column_config={
                "Dividend Yield": st.column_config.NumberColumn(
                    "Dividend Yield",
                    help="Dividend Yield",
                    width="small",
                    required=True,
                    format="%.2f %%",
                )
            },
        )


def mostrar_tab_resultados(df):
    st.write("#### " + str(df.count().unique()[0]) + " registros retornados")
    st.write(df)


def mostrar_filtros_acoes(filtros):
    df_acoes = busca_df_acoes_do_cache().copy()
    col1, _, col2, _, col3, _ = st.columns([4, 1, 4, 1, 4, 1])

    with col1:
        menor_cotacao = float(df_acoes["Cotação"].min(numeric_only=True))
        maior_cotacao = float(df_acoes["Cotação"].max(numeric_only=True))

        filtros["cotacao"] = st.slider(
            "Cotação",
            menor_cotacao,
            maior_cotacao,
            (menor_cotacao, maior_cotacao),
            step=1.0,
            format="R$ %.2f",
        )

        menor_liquidez = float(df_acoes["Liq. Corr."].min(numeric_only=True))
        maior_liquidez = float(df_acoes["Liq. Corr."].max(numeric_only=True))

        filtros["Liq. Corr."] = st.slider(
            "Liquidez Corrente",
            menor_liquidez,
            maior_liquidez,
            (menor_liquidez, maior_liquidez),
            step=1.0,
            format="%.2f",
        )

    with col2:
        pass

    with col3:
        pass


def mostrar_filtros_fiis(filtros):
    df_fiis = busca_df_fiis_do_cache().copy()
    col1, _, col2, _, col3, _ = st.columns([4, 1, 4, 1, 4, 1])

    with col1:
        segmentos_possiveis = ["Todos"] + list(df_fiis["Segmento"].dropna().unique())
        filtros["segmento"] = st.selectbox("Segmento:", segmentos_possiveis)

        filtros["Ignorar mercado balcão"] = st.checkbox(
            "Ignorar mercado balcão", help="Ignorar tickers terminados em 11B"
        )

        filtros["Ignorar FIIs tijolo monoativo"] = st.checkbox(
            "Ignorar FIIs tijolo monoativo",
            help="Ignorar FIIs de tijolo que tenham apenas um ativo",
        )

        menor_liquidez = float(df_fiis["Liquidez"].min(numeric_only=True))
        maior_liquidez = float(df_fiis["Liquidez"].max(numeric_only=True))

        filtros["Liquidez"] = st.slider(
            "Liquidez",
            menor_liquidez,
            maior_liquidez,
            (menor_liquidez, maior_liquidez),
            step=1.0,
            format="%.2f",
        )

    with col2:
        menor_cotacao = float(df_fiis["Cotação"].min(numeric_only=True))
        maior_cotacao = float(df_fiis["Cotação"].max(numeric_only=True))

        filtros["cotacao"] = st.slider(
            "Cotação",
            menor_cotacao,
            maior_cotacao,
            (menor_cotacao, maior_cotacao),
            step=1.0,
            format="R$ %.2f",
        )

        menor_pvp = float(df_fiis["P/VP"].min(numeric_only=True))
        maior_pvp = float(df_fiis["P/VP"].max(numeric_only=True))

        filtros["pvp"] = st.slider(
            "P/VP",
            menor_pvp,
            maior_pvp,
            (menor_pvp, maior_pvp),
            step=0.1,
            format="%.2f",
        )

    with col3:
        filtros["dy"] = st.slider(
            "Dividend Yield (%)", 0, 100, (0, 100), step=1, format="%.2f"
        )

        menor_valor_mercado = (
            float(df_fiis["Valor de Mercado"].min(numeric_only=True)) / 1000000
        )
        maior_valor_mercado = (
            float(df_fiis["Valor de Mercado"].max(numeric_only=True)) / 1000000
        )

        filtros["valor_mercado"] = st.slider(
            "Valor mínimo de Mercado",
            menor_valor_mercado,
            maior_valor_mercado,
            value=menor_valor_mercado,
            step=1.0,
            format="%.2f milhões de R$",
        )


def filtrar_df_acoes(filtros):
    df_tela = busca_df_acoes_do_cache().copy()

    df_tela = df_tela[df_tela["Cotação"] >= filtros["cotacao"][0]]
    df_tela = df_tela[df_tela["Cotação"] <= filtros["cotacao"][1]]

    df_tela.set_index("Papel", drop=True, inplace=True)
    df_tela["ROE"] = df_tela["ROE"] * 100.0
    df_tela["ROIC"] = df_tela["ROIC"] * 100.0
    df_tela["Div.Yield"] = df_tela["Div.Yield"] * 100.0
    df_tela["Cresc. Rec.5a"] = df_tela["Cresc. Rec.5a"] * 100.0
    df_tela["Mrg Ebit"] = df_tela["Mrg Ebit"] * 100.0
    df_tela["Mrg. Líq."] = df_tela["Mrg. Líq."] * 100.0

    return df_tela


def filtrar_df_fiis(filtros):
    df_tela = busca_df_fiis_do_cache().copy()

    if filtros["segmento"] != "Todos":
        df_tela = df_tela[df_tela["Segmento"] == filtros["segmento"]]

    if filtros["Ignorar mercado balcão"]:
        df_tela = df_tela.loc[~df_tela["Papel"].str.endswith("11B")]

    if filtros["Ignorar FIIs tijolo monoativo"]:
        df_tela = df_tela[df_tela["Qtd de imóveis"] != 1]

    df_tela = df_tela[df_tela["Cotação"] >= filtros["cotacao"][0]]
    df_tela = df_tela[df_tela["Cotação"] <= filtros["cotacao"][1]]

    df_tela = df_tela[df_tela["Dividend Yield"] >= filtros["dy"][0] / 100]
    df_tela = df_tela[df_tela["Dividend Yield"] <= filtros["dy"][1] / 100]

    df_tela = df_tela[df_tela["P/VP"] >= filtros["pvp"][0]]
    df_tela = df_tela[df_tela["P/VP"] <= filtros["pvp"][1]]

    df_tela = df_tela[df_tela["Liquidez"] >= filtros["Liquidez"][0]]
    df_tela = df_tela[df_tela["Liquidez"] <= filtros["Liquidez"][1]]

    df_tela = df_tela[df_tela["Valor de Mercado"] >= filtros["valor_mercado"] * 1000000]

    df_tela.set_index("Papel", drop=True, inplace=True)
    df_tela["Dividend Yield"] = df_tela["Dividend Yield"] * 100.0

    return df_tela


def mostrar_tab_acoes():
    st.write("## Ações")
    st.markdown(
        "**Filtros iniciais:** Dividend Yield > 0; Cotação > 0; Liq. Corr. > 0; Liq.2meses > 0"
    )

    filtros = {}

    with st.form("form_acoes"):
        mostrar_filtros_acoes(filtros)
        filtrar_acoes = st.form_submit_button("Filtrar")

    if filtrar_acoes:
        df_acoes_tela = filtrar_df_acoes(filtros)

        tab_detalhes_1, tab_detalhes_2, tab_detalhes_3, tab_detalhes_4 = st.tabs(
            [
                ":memo: Resultados",
                ":bar_chart: Gráficos",
                ":straight_ruler: Estatísticas",
                ":magic_wand: Fórmula Mágica",
            ]
        )

        with tab_detalhes_1:
            mostrar_tab_resultados(df_acoes_tela)
            acoes = [i + ".SA" for i in df_acoes_tela.index]
            pd.options.plotting.backend = "plotly"

            df_fechamento = yf.download(acoes, "2022-01-01")
            df_fechamento = df_fechamento / df_fechamento.iloc[1]
            fig = df_fechamento["Adj Close"].plot()
            st.plotly_chart(fig, use_container_width=True)

        with tab_detalhes_2:
            titulo = "Gráficos sobre os Ações selecionadas"
            graficos = [
                "Cotação",
                "P/L",
                "P/VP",
                "Div.Yield",
                "ROIC",
                "ROE",
                "Liq. Corr.",
            ]

            mostrar_tab_graficos(df_acoes_tela, titulo, graficos, 3, 3)

        with tab_detalhes_3:
            mostrar_tab_estatisticas(df_acoes_tela)

        with tab_detalhes_4:
            mostrar_tab_magic_formula_acoes(df_acoes_tela)


def main():
    st.title(":star: Factor Investing")
    mensagens = st.container()

    if st.button("Carregar dados...") or (is_dados_carregados()):
        tab_geral = stx.tab_bar(
            data=[
                stx.TabBarItemData(id="tab_acoes", title="Ações", description="Ações"),
                stx.TabBarItemData(id="tab_fiis", title="FIIs", description="FIIs"),
            ],
            default="tab_acoes",
            key="tab_geral",
        )

        busca_df_fiis_do_cache()
        busca_df_acoes_do_cache()

        if tab_geral == "tab_acoes":
            mostrar_tab_acoes()

        elif tab_geral == "tab_fiis":
            mostrar_tab_fiis()

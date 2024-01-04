import math
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
import pandas as pd
from libs.market_data.fundamentus.lista import (
    get_df_acoes,
    get_df_fiis,
    get_df_setores,
    get_df_acoes_do_setor,
)
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


@st.cache_data(show_spinner="Buscando dados no Yahoo Finance.", ttl=3600)
def buscar_dados_yahoo(tickers, data_inicial, data_final):
    df = yf.download(tickers, data_inicial, data_final)
    return df["Adj Close"]


@st.cache_data(show_spinner="Buscando dados no Carteira Global.", ttl=3600)
def buscar_dados_carteira_global(tickers, data_inicial, data_final):
    from libs.market_data.carteira_global import CarteiraGlobal

    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_cotacoes_fechamento(tickers, data_inicial, data_final)
    return df


@st.cache_data(show_spinner="Buscando dados do IFIX na Carteira Global.", ttl=3600)
def buscar_dados_ifix_carteira_global(data_inicial, data_final):
    from libs.market_data.carteira_global import CarteiraGlobal

    ID_IFIX = 20
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_dados_indice(ID_IFIX, data_inicial, data_final)
    df.rename(columns={"Close": "IFIX"}, inplace=True)
    return df


@st.cache_data(show_spinner="Buscando dados do IBOV na Carteira Global.", ttl=3600)
def buscar_dados_ibov_carteira_global(data_inicial, data_final):
    from libs.market_data.carteira_global import CarteiraGlobal

    ID_IBOV = 2
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_dados_indice(ID_IBOV, data_inicial, data_final)
    df.rename(columns={"Close": "IBOV"}, inplace=True)
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

            if len(acoes) > 0 and len(acoes) <= 15:
                pd.options.plotting.backend = "plotly"

                df_fechamento = buscar_dados_carteira_global(
                    acoes, "2022-01-01", "2023-12-31"
                )
                # TODO: fazer essa funcao usando a carteira global
                df_ifix = buscar_dados_ifix_carteira_global("2022-01-01", "2023-12-31")
                df_fechamento = df_ifix.merge(
                    df_fechamento, left_index=True, right_index=True, how="inner"
                )
                df_fechamento = df_fechamento / df_fechamento.iloc[1]

                fig = df_fechamento.plot()
                fig.update_traces(line_width=5, selector=dict(name="IFIX"))
                fig.update_layout(legend_title_text="Tickers")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("O gráfico só é gerado para 15 ativos ou menos.")

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
        st.write(df)


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
        st.write(df)


def mostrar_tab_resultados(df):
    st.write("#### " + str(df.count().unique()[0]) + " registros retornados")
    st.write(df)


def mostrar_filtros_acoes(filtros):
    df_acoes = busca_df_acoes_do_cache().copy()
    col1, _, col2, _, col3, _ = st.columns([6, 1, 4, 1, 4, 1])

    with col1:
        setores_possiveis_ordenados = sorted(
            get_df_setores()["Setor"], key=lambda x: int(x.split(" - ")[0])
        )
        # setores_possiveis = ["Todos"] + list(setores_possiveis_ordenados)

        filtros["setores"] = st.multiselect(
            "Setor(es):", setores_possiveis_ordenados, []
        )

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
        segmentos_possiveis = list(df_fiis["Segmento"].dropna().unique())
        segmentos_possiveis.sort()
        filtros["segmentos"] = st.multiselect("Segmento(s):", segmentos_possiveis, [])

    with col2:
        filtros["Ignorar mercado balcão"] = st.checkbox(
            "Ignorar mercado balcão", True, help="Ignorar tickers terminados em 11B"
        )

    with col2:
        filtros["Ignorar FIIs tijolo monoativo"] = st.checkbox(
            "Ignorar FIIs tijolo monoativo",
            True,
            help="Ignorar FIIs de tijolo que tenham apenas um ativo",
        )

    with st.expander("**Liquidez**"):
        menor_liquidez = math.trunc(float(df_fiis["Liquidez"].min(numeric_only=True)))
        maior_liquidez = math.trunc(float(df_fiis["Liquidez"].max(numeric_only=True)))

        filtros["Liquidez mínima"] = st.number_input(
            "Liquidez mínima em R$",
            menor_liquidez,
            maior_liquidez,
            500000,
            step=10000,
            help="Volume médio diário em R$ de negociação do FII, considerando os últimos 2 meses",
        )

    with st.expander("**Cotação**"):
        menor_cotacao = math.trunc(float(df_fiis["Cotação"].min(numeric_only=True)))
        maior_cotacao = math.trunc(float(df_fiis["Cotação"].max(numeric_only=True)))

        filtros["cotacao"] = st.slider(
            "Cotação em R$",
            menor_cotacao,
            maior_cotacao,
            (50, 1000),
            step=10,
            format="R$ %.0f",
        )

    with st.expander("**P/VP**"):
        menor_pvp = float(df_fiis["P/VP"].min(numeric_only=True))
        maior_pvp = float(df_fiis["P/VP"].max(numeric_only=True))

        texto_pvp = ""

        st.write(texto_pvp)

        filtros["pvp"] = st.slider(
            "P/VP",
            menor_pvp,
            maior_pvp,
            (0.7, 1.4),
            step=0.1,
            format="%.2f%%",
        )

    with st.expander("**Valor de Mercado**"):
        menor_valor_mercado = math.trunc(
            float(df_fiis["Valor de Mercado"].min(numeric_only=True)) / 1000000
        )
        maior_valor_mercado = math.trunc(
            float(df_fiis["Valor de Mercado"].max(numeric_only=True)) / 1000000
        )

        col1_valor_mercado, _, _ = st.columns([2, 2, 6])

        with col1_valor_mercado:
            filtros["valor_mercado"] = st.number_input(
                "Valor mínimo de mercado em bilhões de RS",
                menor_valor_mercado,
                maior_valor_mercado,
                value=500,
                step=100,
                help="Valor mínimo de mercado em bilhões de RS",
            )

    with st.expander("**Dividend Yield**"):
        col1_dy, col2_dy, _ = st.columns([2, 2, 6])
        with col1_dy:
            filtros["dy_minimo"] = st.number_input(
                "Dividend Yield (%) mínimo", 0, 100, 6, step=1
            )
        with col2_dy:
            filtros["dy_maximo"] = st.number_input(
                "Dividend Yield (%) máximo", 0, 100, 12, step=1
            )


def filtrar_df_acoes(filtros):
    df_tela = busca_df_acoes_do_cache().copy()

    if filtros["setores"] != []:
        setores = [i.split(" - ")[0] for i in filtros["setores"]]
        tickers_do_setor = []
        for setor in setores:
            tickers_do_setor += list(get_df_acoes_do_setor(setor))
        df_tela = df_tela[df_tela["Papel"].isin(tickers_do_setor)]

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

    if filtros["segmentos"] != []:
        df_tela = df_tela[df_tela["Segmento"].isin(filtros["segmentos"])]

    if filtros["Ignorar mercado balcão"]:
        df_tela = df_tela.loc[~df_tela["Papel"].str.endswith("11B")]

    if filtros["Ignorar FIIs tijolo monoativo"]:
        df_tela = df_tela[df_tela["Qtd de imóveis"] != 1]

    df_tela = df_tela[df_tela["Cotação"] >= filtros["cotacao"][0]]
    df_tela = df_tela[df_tela["Cotação"] <= filtros["cotacao"][1]]

    df_tela = df_tela[df_tela["Dividend Yield"] >= filtros["dy_minimo"] / 100]
    df_tela = df_tela[df_tela["Dividend Yield"] <= filtros["dy_maximo"] / 100]

    df_tela = df_tela[df_tela["P/VP"] >= filtros["pvp"][0]]
    df_tela = df_tela[df_tela["P/VP"] <= filtros["pvp"][1]]

    df_tela = df_tela[df_tela["Liquidez"] >= float(filtros["Liquidez mínima"])]

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

            if len(acoes) <= 15:
                pd.options.plotting.backend = "plotly"

                df_fechamento = buscar_dados_carteira_global(
                    acoes, "2022-01-01", "2023-07-07"
                )
                df_ibov = buscar_dados_ibov_carteira_global("2022-01-01", "2023-07-07")
                df_fechamento = df_ibov.merge(
                    df_fechamento, left_index=True, right_index=True, how="inner"
                )
                df_fechamento = df_fechamento / df_fechamento.iloc[1]

                fig = df_fechamento.plot()
                fig.update_traces(line_width=5, selector=dict(name="IBOV"))
                fig.update_layout(legend_title_text="Tickers")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("O gráfico só é gerado para 15 ativos ou menos.")

            # st.write("Detalhes")
            # from fundamentus import get_papel

            # st.write(get_papel(list(df_acoes_tela.index)))

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
    alertas = st.empty()

    if st.button("Carregar dados...") or (is_dados_carregados()):
        tab_acoes, tab_fiis = st.tabs(["Ações", "FIIs"])

        busca_df_fiis_do_cache()
        busca_df_acoes_do_cache()

        with tab_acoes:
            mostrar_tab_acoes()

        with tab_fiis:
            mostrar_tab_fiis()

        with alertas:
            st.success("Filtros carregados com sucesso!")

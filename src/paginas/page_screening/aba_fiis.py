import pandas as pd
import streamlit as st

from .cache import (
    busca_df_fiis_do_cache,
    buscar_dados_carteira_global,
    buscar_dados_ifix_carteira_global,
)
from .comuns import (
    mostrar_tab_estatisticas,
    mostrar_tab_graficos,
    mostrar_tab_resultados,
    retonar_item_filtro,
)


def mostrar_filtros_fiis(filtros, itens_col1, itens_col2, itens_col3):
    """Apresentar na tela o filtro de FIIs"""
    df_fiis = busca_df_fiis_do_cache().copy()
    df_fiis["FFO Yield"] = df_fiis["FFO Yield"] * 100.0
    df_fiis["Dividend Yield"] = df_fiis["Dividend Yield"] * 100.0
    df_fiis["Cap Rate"] = df_fiis["Cap Rate"] * 100.0
    df_fiis["Vacância Média"] = df_fiis["Vacância Média"] * 100.0

    col1, _, col2, _, col3, _ = st.columns([4, 1, 4, 1, 4, 1])

    with col1:
        segmentos_possiveis = list(df_fiis["Segmento"].dropna().unique())
        segmentos_possiveis.sort()
        filtros["segmentos"] = st.multiselect("Segmento(s):", segmentos_possiveis, [])

        for item in itens_col1:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = retonar_item_filtro(
                df_fiis, coluna, label, "input_number", ajuda=help, formato=None
            )
    with col2:
        filtros["Ignorar mercado balcão"] = st.checkbox(
            "Ignorar mercado balcão", True, help="Ignorar tickers terminados em 11B"
        )

        filtros["Ignorar FIIs tijolo monoativo"] = st.checkbox(
            "Ignorar FIIs tijolo monoativo",
            True,
            help="Ignorar FIIs de tijolo que tenham apenas um ativo",
        )

        for item in itens_col2:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = retonar_item_filtro(
                df_fiis, coluna, label, "input_number", ajuda=help, formato=None
            )

        filtros["Apenas FIIs negociados nos últimos 2 meses"] = st.checkbox(
            "Apenas FIIs negociados nos últimos 2 meses",
            True,
            help="Apenas FIIs negociados nos últimos 2 meses",
        )

    with col3:
        for item in itens_col3:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = retonar_item_filtro(
                df_fiis, coluna, label, "input_number", ajuda=help, formato=None
            )


def filtrar_df_fiis(filtros, itens_col1, itens_col2, itens_col3):
    """Filtrar os FIIs de acordo com os filtros informados."""

    df_tela = busca_df_fiis_do_cache().copy()
    df_tela["FFO Yield"] = df_tela["FFO Yield"] * 100.0
    df_tela["Dividend Yield"] = df_tela["Dividend Yield"]
    df_tela["Cap Rate"] = df_tela["Cap Rate"] * 100.0
    df_tela["Vacância Média"] = df_tela["Vacância Média"] * 100.0

    if filtros["segmentos"] != []:
        df_tela = df_tela[df_tela["Segmento"].isin(filtros["segmentos"])]

    if filtros["Ignorar mercado balcão"]:
        df_tela = df_tela.loc[~df_tela["Papel"].str.endswith("11B")]

    if filtros["Ignorar FIIs tijolo monoativo"]:
        df_tela = df_tela[df_tela["Qtd de imóveis"] != 1]

    if filtros["Apenas FIIs negociados nos últimos 2 meses"]:
        df_tela = df_tela.loc[df_tela["Liquidez"] > 0]

    for item in itens_col1 + itens_col2 + itens_col3:
        coluna = item.get("coluna")
        minimo = float(filtros[coluna].get("minimo"))
        maximo = float(filtros[coluna].get("maximo"))

        if minimo > maximo:
            frase = f"Para o campo {coluna} o valor mínimo está maior que o valor máximo! Corrija o seu filtro!"
            print(frase)
            st.info(
                frase,
                icon="⚠️",
            )
            st.stop()

        df_tela = df_tela[df_tela[coluna] >= minimo]
        df_tela = df_tela[df_tela[coluna] <= maximo]

    df_tela.set_index("Papel", drop=True, inplace=True)
    df_tela["Dividend Yield"] = df_tela["Dividend Yield"] * 100.0

    return df_tela


def mostrar_tab_magic_formula_fiis(df):
    "Mostrar a aba Fórmula Mágica para os FIIs."

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
    df = df.sort_values("Magic Formula", ascending=True)
    df["Ranking Magic Formula"] = range(1, len(df) + 1)

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


def mostrar_tab_fiis():
    "Mostrar a aba de FIIs"

    itens_col1 = [
        {"coluna": "FFO Yield", "label": "FFO Yield (%)", "help": "Valor %"},
        {"coluna": "Valor de Mercado", "label": "Valor de Mercado", "help": ""},
        {"coluna": "Preço do m2", "label": "Preço do m2", "help": ""},
        {"coluna": "Vacância Média", "label": "Vacância Média (%)", "help": "Valor %"},
    ]

    itens_col2 = [
        {"coluna": "Dividend Yield", "label": "Div. Yield (%)", "help": "Valor %"},
        {"coluna": "Liquidez", "label": "Liquidez", "help": ""},
        {"coluna": "Aluguel por m2", "label": "Aluguel por m2", "help": ""},
    ]

    itens_col3 = [
        {"coluna": "Cotação", "label": "Cotação FII (R$)", "help": "Valor em R$"},
        {"coluna": "P/VP", "label": "P/VP FII", "help": ""},
        {"coluna": "Qtd de imóveis", "label": "Qtd de imóveis", "help": ""},
        {"coluna": "Cap Rate", "label": "Cap Rate (%)", "help": "Valor %"},
    ]

    st.write("## FIIs")
    filtros = {}

    with st.form("form_fiis"):
        mostrar_filtros_fiis(filtros, itens_col1, itens_col2, itens_col3)
        filtrar_fiis = st.form_submit_button("Filtrar")

    if filtrar_fiis:
        df_fiis_tela = filtrar_df_fiis(filtros, itens_col1, itens_col2, itens_col3)

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
                st.info(
                    "O gráfico de desempenho normalizado só é gerado para até 15 registros.",
                    icon="⚠️",
                )

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

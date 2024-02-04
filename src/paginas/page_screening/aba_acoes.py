import pandas as pd
import streamlit as st

from libs.market_data.fundamentus import lista

from .cache import (
    busca_df_acoes_do_cache,
    buscar_dados_carteira_global,
    buscar_dados_ibov_carteira_global,
)
from .comuns import (
    mostrar_tab_estatisticas,
    mostrar_tab_graficos,
    mostrar_tab_markowitz,
    mostrar_tab_resultados,
    retonar_item_filtro,
)


def mostrar_filtros_acoes(filtros, itens_col1, itens_col2, itens_col3):
    """Apresentar na tela o filtro de ações"""
    df_acoes = busca_df_acoes_do_cache().copy()

    df_acoes["ROE"] = df_acoes["ROE"] * 100.0
    df_acoes["ROIC"] = df_acoes["ROIC"] * 100.0
    df_acoes["Div.Yield"] = df_acoes["Div.Yield"] * 100.0
    df_acoes["Cresc. Rec.5a"] = df_acoes["Cresc. Rec.5a"] * 100.0
    df_acoes["Mrg Ebit"] = df_acoes["Mrg Ebit"] * 100.0
    df_acoes["Mrg. Líq."] = df_acoes["Mrg. Líq."] * 100.0

    col1, _, col2, _, col3, _ = st.columns([4, 1, 4, 1, 4, 1])

    with col1:
        setores_possiveis_ordenados = sorted(
            lista.get_df_setores()["Setor"], key=lambda x: int(x.split(" - ")[0])
        )
        filtros["setores"] = st.multiselect(
            "Setor(es):", setores_possiveis_ordenados, []
        )

        for item in itens_col1:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = retonar_item_filtro(
                df_acoes, coluna, label, "input_number", ajuda=help, formato=None
            )

        filtros["Apenas ações negociadas nos últimos 2 meses"] = st.checkbox(
            "Apenas ações negociadas nos últimos 2 meses",
            True,
            help="Apenas ações negociadas nos últimos 2 meses",
        )

    with col2:
        for item in itens_col2:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = retonar_item_filtro(
                df_acoes, coluna, label, "input_number", ajuda=help, formato=None
            )
    with col3:
        for item in itens_col3:
            coluna = item.get("coluna")
            label = item.get("label")
            help = item.get("help")

            filtros[coluna] = retonar_item_filtro(
                df_acoes, coluna, label, "input_number", ajuda=help, formato=None
            )


def filtrar_df_acoes(filtros, itens_col1, itens_col2, itens_col3):
    """Filtrar as ações de acordo com os filtros informados."""
    df_tela = busca_df_acoes_do_cache().copy()
    df_tela["ROE"] = df_tela["ROE"] * 100.0
    df_tela["ROIC"] = df_tela["ROIC"] * 100.0
    df_tela["Div.Yield"] = df_tela["Div.Yield"] * 100.0
    df_tela["Cresc. Rec.5a"] = df_tela["Cresc. Rec.5a"] * 100.0
    df_tela["Mrg Ebit"] = df_tela["Mrg Ebit"] * 100.0
    df_tela["Mrg. Líq."] = df_tela["Mrg. Líq."] * 100.0

    if filtros["Apenas ações negociadas nos últimos 2 meses"]:
        df_tela = df_tela.loc[df_tela["Liq.2meses"] > 0]

    if filtros["setores"] != []:
        setores = [i.split(" - ")[0] for i in filtros["setores"]]
        tickers_do_setor = []
        for setor in setores:
            tickers_do_setor += list(lista.get_df_acoes_do_setor(setor))
        df_tela = df_tela[df_tela["Papel"].isin(tickers_do_setor)]

    for item in itens_col1 + itens_col2 + itens_col3:
        coluna = item.get("coluna")
        minimo = float(filtros[coluna].get("minimo"))
        maximo = float(filtros[coluna].get("maximo"))

        print("Filtrando por:")
        print(f"Coluna: {coluna}")
        print(f"Mínimo: {minimo}")
        print(f"Máximo: {maximo}")

        if minimo > maximo:
            frase = f"Para o campo {coluna} o valor mínimo está maior que o valor máximo! Corrija o seu filtro!"
            print(frase)
            st.info(
                frase,
                icon="⚠️",
            )
            st.stop()

        print("Valores da coluna:")
        print(df_tela[coluna].unique())
        print("========================")
        df_tela = df_tela[df_tela[coluna] >= minimo]
        df_tela = df_tela[df_tela[coluna] <= maximo]

    df_tela.set_index("Papel", drop=True, inplace=True)

    if len(df_tela) == 0:
        st.error("Com os filtros aplicados não foram encontrados resultados.", icon="🚨")
        st.stop()

    return df_tela


def mostrar_tab_magic_formula_acoes(df):
    "Mostrar a aba Fórmula Mágica para as ações."
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


def mostrar_tab_acoes():
    "Mostrar a aba de Ações"
    itens_col1 = [
        {"coluna": "P/VP", "label": "P/VP Ação", "help": ""},
        {"coluna": "P/Ativo", "label": "P/Ativo", "help": ""},
        {"coluna": "P/Ativ Circ.Liq", "label": "P/Ativ Circ. Liq.", "help": ""},
        {"coluna": "Mrg Ebit", "label": "Mrg Ebit (%)", "help": "Valor %"},
        {"coluna": "ROIC", "label": "ROIC (%)", "help": "Valor %"},
        {"coluna": "Patrim. Líq", "label": "Patrim. Líq.", "help": ""},
    ]

    itens_col2 = [
        {"coluna": "Cotação", "label": "Cotação Ação (R$)", "help": "Valor em R$"},
        {"coluna": "PSR", "label": "PSR", "help": ""},
        {"coluna": "P/Cap.Giro", "label": "P/Cap. Giro", "help": ""},
        {"coluna": "EV/EBIT", "label": "EV/EBIT", "help": ""},
        {"coluna": "Mrg. Líq.", "label": "Margem Líquida (%)", "help": "Valor %"},
        {"coluna": "ROE", "label": "ROE (%)", "help": "Valor %"},
        {"coluna": "Dív.Brut/ Patrim.", "label": "Dív. Bruta/Patrim.", "help": ""},
    ]

    itens_col3 = [
        {"coluna": "P/L", "label": "P/L", "help": ""},
        {"coluna": "Div.Yield", "label": "Div. Yield (%)", "help": "Valor %"},
        {"coluna": "P/EBIT", "label": "P/EBIT", "help": ""},
        {"coluna": "EV/EBITDA", "label": "EV/EBITDA", "help": ""},
        {"coluna": "Liq. Corr.", "label": "Liq. Corr.", "help": ""},
        {"coluna": "Liq.2meses", "label": "Liq. 2 meses", "help": ""},
        {
            "coluna": "Cresc. Rec.5a",
            "label": "Cresc. Rec. 5 anos (%)",
            "help": "Valor %",
        },
    ]
    st.write("## Ações")

    filtros = {}

    with st.form("form_acoes"):
        mostrar_filtros_acoes(filtros, itens_col1, itens_col2, itens_col3)
        filtrar_acoes = st.form_submit_button("Filtrar")

    if filtrar_acoes:
        df_acoes_tela = filtrar_df_acoes(filtros, itens_col1, itens_col2, itens_col3)

        (
            tab_detalhes_1,
            tab_detalhes_2,
            tab_detalhes_3,
            tab_detalhes_4,
            tab_detalhes_5,
        ) = st.tabs(
            [
                ":memo: Resultados",
                ":bar_chart: Gráficos",
                ":straight_ruler: Estatísticas",
                ":magic_wand: Fórmula Mágica",
                ":dart: Markowitz",
            ]
        )

        with tab_detalhes_1:
            mostrar_tab_resultados(df_acoes_tela)
            acoes = [i + ".SA" for i in df_acoes_tela.index]

            if len(acoes) <= 15:
                pd.options.plotting.backend = "plotly"

                df_fechamento = buscar_dados_carteira_global(
                    acoes, "2022-01-01", "2023-12-31"
                )
                df_ibov = buscar_dados_ibov_carteira_global("2022-01-01", "2023-12-31")
                df_fechamento = df_ibov.merge(
                    df_fechamento, left_index=True, right_index=True, how="inner"
                )
                df_fechamento = df_fechamento / df_fechamento.iloc[1]

                fig = df_fechamento.plot()
                fig.update_traces(line_width=5, selector=dict(name="IBOV"))
                fig.update_layout(legend_title_text="Tickers")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(
                    "O gráfico de desempenho normalizado só é gerado para até 15 registros.",
                    # icon="⚠️",
                )

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

        with tab_detalhes_5:
            mostrar_tab_markowitz(df_acoes_tela)

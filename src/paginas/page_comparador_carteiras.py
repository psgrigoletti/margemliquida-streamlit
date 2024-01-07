from datetime import date  # , timedelta

# import numpy as np
import pandas as pd

# import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

from utils.validacoes_utils import ValidacoesUtils

# from tabulate import tabulate


def mostrar_pagina():
    if "carteiras" not in st.session_state:
        st.session_state["carteiras"] = {}


def criar_carteira(cotacoes, alocacoes):
    cotacao_inicial = cotacoes.iloc[0]
    pl = cotacoes * (round(alocacoes / cotacao_inicial, 0))
    # st.write(pl)
    pl["total"] = pl.sum(axis=1)
    normalizado = pl / pl.iloc[0]
    carteira_final = normalizado["total"]
    return carteira_final


def plotar_grafico(benchmarks, carteiras: dict):
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(12, 8))
    for b in benchmarks.values():
        plt.plot(b)
    for c in carteiras.values():
        plt.plot(c)
    plt.legend(list(benchmarks.keys()) + list(carteiras.keys()))
    st.pyplot(
        fig,
    )


def main():
    st.title(
        ":straight_ruler: Comparar Carteira",
    )
    st.write(
        "**Fonte**: https://finance.yahoo.com/ via [yfinance](https://pypi.org/project/yfinance/)"
    )

    mostrar_pagina()
    alertas = st.empty()

    hoje = date.today()
    ano_passado = date(hoje.year - 1, hoje.month, hoje.day)

    with st.expander("**Adicionar carteira**", expanded=False):
        lista_ibovespa = [
            "RRRP3",
            "ALSO3",
            "ALPA4",
            "ABEV3",
            "ARZZ3",
            "ASAI3",
            "AZUL4",
            "B3SA3",
            "BBSE3",
            "BBDC3",
            "BBDC4",
            "BRAP4",
            "BBAS3",
            "BRKM5",
            "BRFS3",
            "BPAC11",
            "CRFB3",
            "CCRO3",
            "CMIG4",
            "CIEL3",
            "COGN3",
            "CPLE6",
            "CSAN3",
            "CPFE3",
            "CMIN3",
            "CVCB3",
            "CYRE3",
            "DXCO3",
            "ELET3",
            "ELET6",
            "EMBR3",
            "ENBR3",
            "ENGI11",
            "ENEV3",
            "EGIE3",
            "EQTL3",
            "EZTC3",
            "FLRY3",
            "GGBR4",
            "GOAU4",
            "GOLL4",
            "NTCO3",
            "SOMA3",
            "HAPV3",
            "HYPE3",
            "IGTI11",
            "IRBR3",
            "ITSA4",
            "ITUB4",
            "JBSS3",
            "KLBN11",
            "RENT3",
            "LWSA3",
            "LREN3",
            "MGLU3",
            "MRFG3",
            "CASH3",
            "BEEF3",
            "MRVE3",
            "MULT3",
            "PCAR3",
            "PETR3",
            "PETR4",
            "PRIO3",
            "PETZ3",
            "RADL3",
            "RAIZ4",
            "RDOR3",
            "RAIL3",
            "SBSP3",
            "SANB11",
            "SMTO3",
            "CSNA3",
            "SLCE3",
            "SUZB3",
            "TAEE11",
            "VIVT3",
            "TIMS3",
            "TOTS3",
            "UGPA3",
            "USIM5",
            "VALE3",
            "VIIA3",
            "VBBR3",
            "WEGE3",
            "YDUQ3",
        ]
        acoes_selecionadas = st.multiselect(
            "Selecione as ações que vão compor a carteira", sorted(lista_ibovespa)
        )

        nome_carteira = st.text_input("Nome da carteira")

        st.write("Informe os valores inicias para cada ação:")

        df = pd.DataFrame(
            columns=["Reais (R$)"], index=[a + ".SA" for a in acoes_selecionadas]
        ).transpose()
        df_editavel = st.data_editor(df)

        if st.button("Adicionar carteira"):
            if len(acoes_selecionadas) <= 1:
                with alertas:
                    st.error(icon="🚨", body="Selecione pelo menos 2 ações.")
                    st.stop()

            if not nome_carteira:
                with alertas:
                    st.error(icon="🚨", body="Informe um nome para a carteira.")
                    st.stop()
            else:
                st.session_state["carteiras"][nome_carteira] = df_editavel.transpose()

    with st.expander("**Carteiras já adicionadas**", expanded=False):
        st.write(st.session_state["carteiras"])
        if st.button("Limpar carteiras"):
            st.session_state["carteiras"] = []

    with st.expander("**Outros parâmetros**", expanded=False):
        lista_benchmarks_disponiveis = ["^BVSP", "USDBRL=X", "SPY", "^IRX"]
        benchmarks_selecionados = st.multiselect(
            "Selecione os benchmarks", lista_benchmarks_disponiveis
        )

        col1, col2, _ = st.columns([2, 2, 6])
        data_inicial = col1.date_input("Data inicial:", ano_passado)
        data_final = col2.date_input("Data final:", hoje)

    if st.button("Analisar"):
        frase = "Crie pelo menos 2 carteiras."
        condicao = len(st.session_state["carteiras"]) <= 1
        ValidacoesUtils.validar_condicao(condicao, alertas, frase)

        frase = "Selecione pelo menos 2 benchmarks."
        condicao = len(benchmarks_selecionados) <= 1
        ValidacoesUtils.validar_condicao(condicao, alertas, frase)

        frase = "Data inicial e final são obrigatórias."
        condicao = not data_inicial or not data_final
        ValidacoesUtils.validar_condicao(condicao, alertas, frase)

        # Criar dicionário com os benchmarks
        benchmarks = yf.download(
            benchmarks_selecionados,
            start=data_inicial.strftime("%Y-%m-%d"),
            end=data_final.strftime("%Y-%m-%d"),
        )["Adj Close"]
        benchmarks.dropna(inplace=True)
        benchmarks_normalizado = benchmarks / benchmarks.iloc[0]
        benchmarks_dict = {}
        for c in benchmarks_normalizado.columns:
            benchmarks_dict[c] = benchmarks_normalizado[c]

        # Criar um dicionário com as carteiras
        carteiras_dict = {}
        for ck in st.session_state["carteiras"].keys():
            cv = st.session_state["carteiras"][ck]
            cv = cv.rename(columns={"Reais (R$)": "0"})
            cv["0"] = cv["0"].astype(float)
            alocacoes = cv["0"]
            acoes = [col for col in alocacoes.index]
            cotacoes = yf.download(
                acoes,
                start=data_inicial.strftime("%Y-%m-%d"),
                end=data_final.strftime("%Y-%m-%d"),
            )["Adj Close"]
            cotacoes.dropna(inplace=True)
            carteira = criar_carteira(cotacoes, alocacoes)
            carteiras_dict[ck] = carteira

        plotar_grafico(benchmarks_dict, carteiras_dict)

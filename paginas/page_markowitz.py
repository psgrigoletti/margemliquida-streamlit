import streamlit as st
import datetime
from libs.dividendos import Dividendos
from libs.market_data.carteira_global import CarteiraGlobal
import logging
from utils.data_hora_utils import DataHoraUtils
import yfinance as yf
import numpy as np
import pandas as pd

## Construção da página


@st.cache_data
def buscar_cotacoes(tickers, data_inicial):
    df = yf.download(tickers=tickers, start=data_inicial)["Adj Close"]
    df = df.pct_change().apply(lambda x: np.log(1 + x)).dropna()
    return df


def main():
    st.title(
        ":heavy_dollar_sign: Markowitz",
    )
    mensagens = st.container()

    ## Formulário

    col1, col2, col3 = st.columns([1, 1, 1])
    tickers = col1.text_input("Tickers separados por espaço:", "")
    data_inicial = col2.date_input("Data inicial:", datetime.date(2018, 1, 1))
    data_final = col3.date_input("Data final:", datetime.datetime.now())

    if st.button("Executar", help="Executar"):
        lista_acoes = tickers.split(" ")
        lista_acoes = [i + ".SA" for i in lista_acoes]
        retornos = buscar_cotacoes(lista_acoes, data_inicial)
        # st.write(retornos)
        media_retornos = retornos.mean()
        matriz_cov = retornos.cov()

        numero_carteiras = 10000
        tabela_retornos_esperados = np.zeros(numero_carteiras)
        tabela_volatilidades_esperadas = np.zeros(numero_carteiras)
        tabela_sharpe = np.zeros(numero_carteiras)
        tabela_pesos = np.zeros((numero_carteiras, len(lista_acoes)))

        for k in range(numero_carteiras):
            pesos = np.random.random(len(lista_acoes))
            pesos = pesos / np.sum(pesos)
            tabela_pesos[k, :] = pesos

            tabela_retornos_esperados[k] = np.sum(media_retornos * pesos * 252)
            tabela_volatilidades_esperadas[k] = np.sqrt(
                np.dot(pesos.T, np.dot(matriz_cov * 252, pesos))
            )
            tabela_sharpe[k] = (
                tabela_retornos_esperados[k] / tabela_volatilidades_esperadas[k]
            )

        indice_do_sharpe_maximo = tabela_sharpe.argmax()

        resposta = []
        for i in range(len(lista_acoes)):
            resposta.append(
                [
                    lista_acoes[i],
                    str(round(tabela_pesos[indice_do_sharpe_maximo][i] * 100.0, 2))
                    + " %",
                ]
            )
        resposta_df = pd.DataFrame(resposta, columns=["Ação", "Percentual"])

        col1, col2 = st.columns([3, 7])

        with col1:
            st.write(resposta_df)

        tabela_retornos_esperados_arit = np.exp(tabela_retornos_esperados) - 1
        eixo_y_fronteira_eficiente = np.linspace(
            tabela_retornos_esperados_arit.min(),
            tabela_retornos_esperados_arit.max(),
            50,
        )

        def pegando_retorno(peso_teste):
            peso_teste = np.array(peso_teste)
            retorno = np.sum(media_retornos * peso_teste) * 252
            retorno = np.exp(retorno) - 1
            return retorno

        def checando_soma_pesos(peso_teste):
            return np.sum(peso_teste) - 1

        def pegando_vol(peso_teste):
            peso_teste = np.array(peso_teste)
            vol = np.sqrt(np.dot(peso_teste.T, np.dot(matriz_cov * 252, peso_teste)))
            return vol

        from scipy.optimize import minimize

        peso_inicial = [1 / len(lista_acoes)] * len(lista_acoes)
        limites = tuple([(0, 1) for ativo in lista_acoes])

        eixo_x_fronteira_eficiente = []
        for retorno_possivel in eixo_y_fronteira_eficiente:
            restricoes = (
                {"type": "eq", "fun": checando_soma_pesos},
                {"type": "eq", "fun": lambda w: pegando_retorno(w) - retorno_possivel},
            )
            result = minimize(
                pegando_vol,
                peso_inicial,
                method="SLSQP",
                bounds=limites,
                constraints=restricoes,
            )
            eixo_x_fronteira_eficiente.append(result["fun"])

        import matplotlib.pyplot as plt
        import matplotlib.ticker as mtick

        fig, ax = plt.subplots()
        ax.scatter(
            tabela_volatilidades_esperadas,
            tabela_retornos_esperados_arit,
            c=tabela_sharpe,
        )
        plt.xlabel("Volatilidade esperada")
        plt.ylabel("Retorno esperado")
        # ax.xaxis.label.set_color("white")
        # ax.yaxis.label.set_color("white")
        ax.scatter(
            tabela_volatilidades_esperadas[indice_do_sharpe_maximo],
            tabela_retornos_esperados_arit[indice_do_sharpe_maximo],
            c="red",
        )
        ax.plot(eixo_x_fronteira_eficiente, eixo_y_fronteira_eficiente)
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        # ax.tick_params(axis="x", colors="white")
        # ax.tick_params(axis="y", colors="white")

        with col2:
            st.pyplot(fig)

import datetime

# from libs.dividendos import Dividendos
# from libs.market_data.carteira_global import CarteiraGlobal
# AQUI https://www.youtube.com/watch?v=ynmBdBWy4gs
import logging

import numpy as np
import pandas as pd
import streamlit as st

# from utils.data_hora_utils import DataHoraUtils
import yfinance as yf
from paginas.page_markowitz.aba_pyfolio import (
    criar_grafico_carteira_minima_variancia,
)

# ## Construção da página


@st.cache_data
def buscar_cotacoes(tickers, data_inicial, data_final):
    df = yf.download(tickers=tickers, start=data_inicial, end=data_final)["Adj Close"]
    return df


def main():
    st.title(
        ":heavy_dollar_sign: Markowitz",
    )

    #     mensagens = st.container()

    col1, col2, col3 = st.columns([1, 1, 1])
    tickers = col1.text_input(
        "Tickers separados por espaço (sem .SA):", "PETR3 BBSE3 VALE3"
    )

    data_inicial = col2.date_input("Data inicial:", datetime.date(2018, 1, 1))
    data_final = col3.date_input("Data final:", datetime.datetime.now())

    if st.button("Executar", help="Executar"):
        # st.write("# Preços", precos)
        # retornos = precos.pct_change().apply(lambda x: np.log(1 + x)).dropna()
        # st.write("# Retornos", retornos)
        # media_retornos = retornos.mean()
        # st.write("# Média retornos", media_retornos)
        # matriz_cov = retornos.cov()
        # st.write("# Matriz covariância", matriz_cov)

        lista_acoes = tickers.split(" ")
        lista_acoes = [i + ".SA" for i in lista_acoes]
        precos = buscar_cotacoes(lista_acoes, data_inicial, data_final)
        retornos = precos.pct_change().dropna()

        st.write("# Ações", lista_acoes)
        st.write("# Fechamentos", precos)
        st.write("# Retornos", retornos)
        pd.options.display.float_format = "{:.4}".format
        criar_grafico_carteira_minima_variancia(retornos)


# https://gist.github.com/paulorodriguesxv/db3be69072ce4f82ef9f0838c5176b92
# https://github.com/robertmartin8/PyPortfolioOpt
# https://plotly.com/python/v3/ipython-notebooks/markowitz-portfolio-optimization/

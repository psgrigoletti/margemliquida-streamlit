# from datetime import date
# import plotly.graph_objects as go

import matplotlib as mpl

# import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

# import seaborn as sns
import streamlit as st
import yfinance as yf
from deep_translator import GoogleTranslator
from margemliquida_market_data.b3.bdrs import buscar_lista_bdrs_nao_patrocinados
from margemliquida_market_data.b3.etfs import buscar_lista_etfs_renda_variavel

mpl.use("Agg")
st.set_option("deprecation.showPyplotGlobalUse", False)


@st.cache_data(show_spinner="Buscando lista dos ETFs de renda variável...", ttl=3600)
def buscar_lista_etfs_renda_variavel_do_cache():
    return buscar_lista_etfs_renda_variavel(forcar_webscrapping=True)


@st.cache_data(show_spinner="Buscando lista dos BDRs não patrocinados...", ttl=3600)
def buscar_lista_bdrs_nao_patrocinados_do_cache():
    return buscar_lista_bdrs_nao_patrocinados(forcar_webscrapping=True)


def main():
    st.title(":chart_with_upwards_trend: BDRs e ETFs")
    st.write(
        "**Fonte**: https://finance.yahoo.com/ via [yfinance](https://pypi.org/project/yfinance/)"
    )
    alertas = st.empty()

    opcoes = st.radio("Selecione", ["BDRs", "ETFs"])
    if opcoes == "BDRs":
        with st.form(key="form_indice"):
            tickers = st.multiselect(
                "BDRs", buscar_lista_bdrs_nao_patrocinados_do_cache()
            )
            analisar = st.form_submit_button("Analisar")
    elif opcoes == "ETFs":
        with st.form(key="form_acoes"):
            tickers = st.multiselect("ETFs", buscar_lista_etfs_renda_variavel())
            analisar = st.form_submit_button("Analisar")

    if analisar:
        if len(tickers) <= 1:
            with alertas:
                st.error("Selecione pelo menos 2 tickers.", icon="🚨")
                st.stop()

        data_inicial = "2023-01-01"
        data_final = "2024-02-03"

        try:
            retornos = yf.download(
                tickers, start=data_inicial, end=data_final, interval="1d"
            )
            fechamentos = retornos["Close"]
            fechamentos_normalizados = fechamentos / fechamentos.iloc[0]
            pd.options.plotting.backend = "plotly"
            fig = fechamentos_normalizados.plot()
            st.plotly_chart(fig, use_container_width=True)

            abas = st.tabs(tickers)
            indice_aba = 0

            for aba in abas:
                with aba:
                    dados = yf.Ticker(tickers[indice_aba])
                    about, sobre, graficos = st.tabs(["About", "Sobre", "Gráficos"])
                    with about:
                        st.write("# About")
                        if opcoes == "BDRs":
                            st.write(dados.info["longBusinessSummary"])
                        elif opcoes == "ETFs":
                            st.write(dados.info["shortName"])
                            st.write(dados.info["longName"])
                            if "longBusinessSummary" in dados.info:
                                st.write(dados.info["longBusinessSummary"])
                    with sobre:
                        st.write("# Sobre")
                        if opcoes == "BDRs":
                            translated = GoogleTranslator(
                                source="en", target="pt"
                            ).translate(dados.info["longBusinessSummary"])
                            st.write(translated)
                        elif opcoes == "ETFs":
                            st.write(dados.info["shortName"])
                            st.write(dados.info["longName"])
                            if "longBusinessSummary" in dados.info:
                                st.write(dados.info["longBusinessSummary"])
                    with graficos:
                        fig = mpf.plot(
                            dados.history(period="2y"),
                            type="candle",
                            # style="charles",
                            datetime_format="%d/%b/%y",
                            title=f"{tickers[indice_aba]}",
                            ylabel="Preço (R$)",
                            volume=True,
                            mav=(7, 21, 200),
                            # ylabel_lower="Shares\nTraded",
                        )
                        st.pyplot(fig)

                    indice_aba += 1

        except Exception as ex:
            st.write("Erro ao gerar gráfico...")
            print(ex)

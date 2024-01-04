import streamlit as st
import yfinance as yf
import quantstats as qs
import imgkit
import uuid
import os
import pandas as pd


def main():
    st.title(":flag-br: Relatório QuantStats")
    alertas = st.empty()
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.text_input("Ticker", "BBSE3.SA")

    with col2:
        indice = st.text_input("Índice", "BOVA11.SA")

    with col3:
        data_inicial = st.text_input("Data inicial", "2023-01-01")

    if st.button("Gerar relatórios"):
        ticker = ticker.upper()
        if not ticker.endswith(".SA"):
            ticker = ticker + ".SA"

        indice = indice.upper()
        if not indice.endswith(".SA"):
            indice = indice + ".SA"

        with st.spinner("Gerando os relatórios, aguarde..."):
            qs.extend_pandas()

            # fetch the daily returns for a stock
            stock = yf.download(ticker, start=data_inicial, interval="1d")
            stock.rename(columns={"Close": ticker}, inplace=True)
            stock = stock[ticker].pct_change()
            stock = stock.dropna()

            index = yf.download(indice, start=data_inicial, interval="1d")
            index.rename(columns={"Close": indice}, inplace=True)
            index = index[indice].pct_change()
            index = index.dropna()

            tab_resumo, tab_completo = st.tabs(["Resumo", "Completo"])

            qs.stats.sharpe(stock)
            stock.sharpe()
            fig = qs.plots.snapshot(stock, title=f"{ticker} Performance", show=False)

            with tab_resumo:
                st.write(fig)

            with tab_completo:
                myuuid = uuid.uuid4()

                arquivo_html = f"quantstats-tearsheet-{myuuid}.html"
                arquivo_jpg = f"quantstats-tearsheet-{myuuid}.jpg"

                pd.options.plotting.backend = "matplotlib"

                _ = qs.reports.html(
                    stock,
                    index,
                    output=arquivo_html,
                    download_filename=arquivo_html,
                )

                imgkit.from_file(arquivo_html, arquivo_jpg)
                st.image(arquivo_jpg)

                os.remove(arquivo_html)
                os.remove(arquivo_jpg)

                with alertas:
                    st.success("Relatórios gerados com sucesso.", icon="✅")

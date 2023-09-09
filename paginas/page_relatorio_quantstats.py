import time
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from libs.tesouro_direto import TesouroDireto


# @st.cache_data(show_spinner="Carregando dados...", ttl=60*5)
# def atualizar_dados_tesouro_direto(data_atual):
#     td = TesouroDireto()
#     td.atualizar_graficos()
#     return td


def carregar_dados(mensagens):
    print("carregar")


#     delta = 0
#     if time.tzname[0] == "UTC":
#         delta = 3
#     agora = datetime.today() - timedelta(hours=delta, minutes=0)
#     agora = agora.strftime('%d/%m/%Y')

#     td = atualizar_dados_tesouro_direto(agora)

#     with mensagens:
#         st.success("Dados carregados com sucesso!")

#     selic, ipca, pre = st.tabs(["SELIC", ":dragon: IPCA+", "PREFIXADO"])

#     with selic:
#         st.markdown("## Tesouro SELIC")
#         st.plotly_chart(td.retornar_grafico_precos_tesouro_selic(),
#                         use_container_width=True)
#         st.plotly_chart(td.retornar_grafico_taxas_tesouro_selic(),
#                         use_container_width=True)

#     with ipca:
#         st.markdown("## Tesouro IPCA+")
#         st.plotly_chart(td.retornar_grafico_precos_tesouro_ipca(),
#                         use_container_width=True)
#         st.plotly_chart(td.retornar_grafico_taxas_tesouro_ipca(),
#                         use_container_width=True)

#     with pre:
#         st.markdown("## Tesouro PREFIXADO")
#         st.plotly_chart(td.retornar_grafico_precos_tesouro_pre(),
#                         use_container_width=True)
#         st.plotly_chart(td.retornar_grafico_taxas_tesouro_pre(),
#                         use_container_width=True)


def main():
    st.title(":flag-br: Relatório QuantStats")
    mensagens = st.container()

    ticker = st.text_input("Ticker", "BBSE3.SA")
    indice = st.text_input("Índice", "BOVA11.SA")
    data_inicial = st.text_input("Data inicial", "2023-01-01")

    if st.button("Carregar dados..."):
        carregar_dados(mensagens)
        import quantstats as qs

        # extend pandas functionality with metrics, etc.
        qs.extend_pandas()

        # fetch the daily returns for a stock
        stock = yf.download(ticker, start=data_inicial, interval="1d")[
            "Close"
        ].pct_change()
        stock = stock.dropna()
        # stock.index = pd.to_datetime(stock.index)

        index = yf.download(indice, start=data_inicial, interval="1d")[
            "Close"
        ].pct_change()
        index = index.dropna()
        # index.index = pd.to_datetime(index.index)

        # show sharpe ratio

        tab_resumo, tab_completo = st.tabs(["Resumo", "Completo"])

        qs.stats.sharpe(stock)

        # or using extend_pandas() :)
        stock.sharpe()
        fig = qs.plots.snapshot(stock, title=f"{ticker} Performance", show=False)

        with tab_resumo:
            st.write(fig)

        with tab_completo:
            html = qs.reports.html(
                stock,
                index,
                output="quantstats-tearsheet.html",
                download_filename="quantstats-tearsheet.html",
            )

            import imgkit

            imgkit.from_file("quantstats-tearsheet.html", "quantstats-tearsheet.jpg")
            st.image("quantstats-tearsheet.jpg")

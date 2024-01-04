import streamlit as st
import yfinance as yf
import pandas as pd

# from datetime import date
# import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    st.title(":chart_with_upwards_trend: Rentabilidades mensais")
    alertas = st.empty()

    opcoes = st.radio("Selecione", ["Índices", "Ações"])
    if opcoes == "Índices":
        with st.form(key="form_indice"):
            ticker = st.selectbox(
                "Índice",
                [
                    "^BVSP",
                    "^GSPC",
                    "^IXIC",
                    "^GDAXI",
                    "^N225",
                    "^FTSE",
                    "CL=F",
                    "GC=F",
                    "BTC-USD",
                    "ETH-USD",
                    "BNB-USD",
                    "EURBRL=X",
                    "USDBRL=X",
                    "CADBRL=X",
                ],
            )

            analisar = st.form_submit_button("Analisar")
    else:
        with st.form(key="form_acoes"):
            ticker = st.text_input("Ações")
            analisar = st.form_submit_button("Analisar")

    if analisar:
        if len(ticker) == 0:
            with alertas:
                st.error("Informe um ticker.", icon="🚨")
                st.stop()

        data_inicial = "1999-12-01"
        data_final = "2023-12-01"

        ticker = ticker.upper()
        if opcoes == "Ações" and not ticker.endswith(".SA"):
            ticker += ".SA"
        try:
            retornos = yf.download(
                ticker, start=data_inicial, end=data_final, interval="1mo"
            )["Close"].pct_change()
            retorno_mensal = retornos.groupby(
                [
                    retornos.index.year.rename("Year"),
                    retornos.index.month.rename("Month"),
                ]
            ).mean()
        except:
            with alertas:
                st.error("Problema ao buscar os dados no YFinance.", icon="🚨")
                st.stop()

        tabela_retornos = pd.DataFrame(retorno_mensal)
        tabela_retornos = tabela_retornos.pivot_table(
            values="Close", index="Year", columns="Month"
        )
        tabela_retornos.columns = [
            "Jan",
            "Fev",
            "Mar",
            "Abr",
            "Mai",
            "Jun",
            "Jul",
            "Ago",
            "Set",
            "Out",
            "Nov",
            "Dez",
        ]
        # st.write(tabela_retornos)

        fig, ax = plt.subplots(figsize=(12, 9))
        cmap = sns.color_palette("RdYlGn", 50)  # RED YELLOW GREEN
        sns.heatmap(
            tabela_retornos,
            cmap=cmap,
            annot=True,
            fmt=".2%",
            center=0,
            vmax=0.02,
            vmin=-0.02,
            cbar=False,
            linewidths=1,
            xticklabels=True,
            yticklabels=True,
            ax=ax,
        )
        ax.set_title(ticker, fontsize=18)
        ax.set_yticklabels(
            ax.get_yticklabels(),
            rotation=0,
            verticalalignment="center",
            fontsize=13,
        )
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)
        ax.xaxis.tick_top()
        plt.ylabel("")
        st.pyplot(fig)

        stats = pd.DataFrame(tabela_retornos.mean(), columns=["Média"])
        stats["Mediana"] = tabela_retornos.median()
        stats["Maior"] = tabela_retornos.max()
        stats["Menor"] = tabela_retornos.min()
        stats["Positivos"] = tabela_retornos.gt(0).sum() / tabela_retornos.count()
        stats["Negativos"] = tabela_retornos.le(0).sum() / tabela_retornos.count()

        stats_a = stats[["Média", "Mediana", "Maior", "Menor"]]
        stats_a = stats_a.transpose()

        fig, ax = plt.subplots(figsize=(12, 2.5))
        cmap = sns.color_palette("RdYlGn", 50)  # RED YELLOW GREEN
        sns.heatmap(
            stats_a,
            cmap=cmap,
            annot=True,
            fmt=".2%",
            center=0,
            vmax=0.02,
            vmin=-0.02,
            cbar=False,
            linewidths=1,
            xticklabels=True,
            yticklabels=True,
            ax=ax,
        )
        ax.set_yticklabels(
            ax.get_yticklabels(), rotation=0, verticalalignment="center", fontsize=8
        )
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)
        ax.xaxis.tick_top()
        plt.ylabel("")
        st.pyplot(fig)

        stats_b = stats[["Positivos", "Negativos"]]
        stats_b = stats_b.transpose()

        fig, ax = plt.subplots(figsize=(12, 2.5))
        cmap = sns.color_palette("RdYlGn", 50)  # RED YELLOW GREEN
        sns.heatmap(
            stats_b,
            annot=True,
            fmt=".2%",
            center=0,
            vmax=0.02,
            vmin=-0.02,
            cbar=False,
            linewidths=1,
            xticklabels=True,
            yticklabels=True,
            ax=ax,
        )
        ax.set_yticklabels(
            ax.get_yticklabels(), rotation=0, verticalalignment="center", fontsize=7
        )
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=12)
        ax.xaxis.tick_top()
        plt.ylabel("")
        st.pyplot(fig)

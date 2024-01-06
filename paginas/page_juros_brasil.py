import streamlit as st
from bcb import sgs
import matplotlib.pyplot as plt
import pandas as pd


def main():
    st.title(":calendar: Juros no Brasil")
    st.write("**Fonte**: ? via [?]()")
    mensagens = st.container()
    selic_diaria = sgs.get({"SELIC Diária": 11}, start="2023-01-01")
    selic_diaria["SELIC Acumulada"] = (
        (1 + selic_diaria["SELIC Diária"] / 100).cumprod()
    ) - 1
    selic_diaria["SELIC Acumulada"] = selic_diaria["SELIC Acumulada"] * 100.0
    # selic_diaria.index = selic_diaria.index.to_period("M")

    st.write(selic_diaria)

    # fig = selic_diaria.plot(figsize=(12, 6))
    pd.options.plotting.backend = "plotly"
    fig = selic_diaria.plot()
    # fig.update_traces(line_width=5, selector=dict(name="SELIC"))
    # fig.update_layout(legend_title_text="SELIC")
    st.plotly_chart(fig, use_container_width=True)
    # plt.title("Fonte: https://dadosabertos.bcb.gov.br", fontsize=10)
    # plt.suptitle("IPCA acumulado 12 meses - Janela Móvel", fontsize=18)
    # plt.xlabel("Data")
    # plt.ylabel("%")
    # plt.legend().set_visible(False)
    # st.write(fig)

import time
from datetime import datetime, timedelta

import streamlit as st
from libs.tesouro_direto import TesouroDireto


@st.cache_data(show_spinner="Carregando dados...", ttl=60 * 5)
def atualizar_dados_tesouro_direto(data_atual):
    td = TesouroDireto()
    td.atualizar_graficos()
    return td


def carregar_dados(mensagens):
    delta = 0
    if time.tzname[0] == "UTC":
        delta = 3
    agora = datetime.today() - timedelta(hours=delta, minutes=0)
    agora = agora.strftime("%d/%m/%Y")

    td = atualizar_dados_tesouro_direto(agora)

    with mensagens:
        st.success("Dados carregados com sucesso!", icon="✅")

    selic, ipca, pre = st.tabs(["SELIC", ":dragon: IPCA+", "PREFIXADO"])

    with selic:
        st.markdown("## Tesouro SELIC")
        st.plotly_chart(
            td.retornar_grafico_precos_tesouro_selic(), use_container_width=True
        )
        st.plotly_chart(
            td.retornar_grafico_taxas_tesouro_selic(), use_container_width=True
        )

    with ipca:
        st.markdown("## Tesouro IPCA+")
        st.plotly_chart(
            td.retornar_grafico_precos_tesouro_ipca(), use_container_width=True
        )
        st.plotly_chart(
            td.retornar_grafico_taxas_tesouro_ipca(), use_container_width=True
        )

    with pre:
        st.markdown("## Tesouro PREFIXADO")
        st.plotly_chart(
            td.retornar_grafico_precos_tesouro_pre(), use_container_width=True
        )
        st.plotly_chart(
            td.retornar_grafico_taxas_tesouro_pre(), use_container_width=True
        )


def main():
    st.title(":flag-br: Tesouro Direto")
    st.write("**Fonte**: https://www.tesourotransparente.gov.br/")

    mensagens = st.container()

    if st.button("Carregar dados..."):
        carregar_dados(mensagens)

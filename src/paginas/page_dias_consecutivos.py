import datetime

import streamlit as st
from libs.dias_consecutivos import DiasConsecutivos


@st.cache_data(show_spinner="Carregando dados...", ttl=60 * 5)
def buscar_dados_ticker(
    ticker, dias_analise, data_final, data_inicial, direcao, dias_consecutivos
):
    dias_consecutivos = DiasConsecutivos(
        ticker=ticker,
        dias_apos=dias_analise,
        end_date=data_final,
        start_date=data_inicial,
        direcao=direcao,
        dias_consecutivos=dias_consecutivos,
    )
    return dias_consecutivos


def validar_parametros(ticker, data_inicial, data_final, dias_analise, mensagens):
    if not ticker:
        mensagens.error("Ticker não informado.", icon="🚨")
        st.stop()

    if not data_inicial:
        mensagens.error("Data inicial não informada.", icon="🚨")
        st.stop()

    if not data_final:
        mensagens.error("Data final não informada.", icon="🚨")
        st.stop()

    if data_final <= data_inicial:
        mensagens.error("Data inicial deve ser menor que a Data final.", icon="🚨")
        st.stop()

    if not dias_analise or len(dias_analise) == 0:
        frase = "Selecione ao menos 1 valor em 'Analisar n dias após'."
        mensagens.error(frase, icon="🚨")
        st.stop()


def main():
    st.title(":calendar: Dias Consecutivos")
    st.write(
        "**Fonte**: https://finance.yahoo.com/ via [yfinance](https://pypi.org/project/yfinance/)"
    )
    mensagens = st.container()

    col1, col2, col3 = st.columns(3)
    ticker = col1.text_input("Ticker:", value="PETR4.SA")

    data_inicial = col2.date_input("Data inicial:", value=datetime.date(2020, 1, 1))

    data_final = col3.date_input("Data final:", value=datetime.date(2024, 1, 1))

    st.markdown("#### Buscar por:")

    col5, col6, _, _, _ = st.columns(5)

    dias_consecutivos = col5.number_input(
        "Dias consecutivos:", min_value=3, max_value=10, value=5
    )

    direcao = col6.select_slider("Tendência:", ["Baixa", "Alta"])

    st.markdown("#### Análise/Resultado:")
    dias_analise = st.multiselect(
        "Analisar n dias após:", [1, 2, 3, 5, 10, 15, 20], [1, 2, 5, 10]
    )
    mostrar_grafico = st.checkbox("Mostrar Gráfico", value=True)

    if st.button("Analisar"):
        validar_parametros(ticker, data_inicial, data_final, dias_analise, mensagens)
        dias_consecutivos = buscar_dados_ticker(
            ticker, dias_analise, data_final, data_inicial, direcao, dias_consecutivos
        )
        if dias_consecutivos.quantidade_periodos_encontrados == 0:
            with mensagens:
                st.error("Nenhum resultado encontrado.", icon="🚨")
            st.stop()
        else:
            with mensagens:
                st.success("Análise realizada com sucesso.", icon="✅")

        if mostrar_grafico:
            tab1, tab2, tab3 = st.tabs(["Gráfico", "Relatório", "Tabela"])
            tab1.plotly_chart(
                dias_consecutivos.retornar_grafico(), use_container_width=True
            )
            tab2.markdown(dias_consecutivos.retornar_relatorio())
            tab3.markdown(dias_consecutivos.retornar_tabela())
        else:
            tab2, tab3 = st.tabs(["Relatório", "Tabela"])
            tab2.markdown(dias_consecutivos.retornar_relatorio())
            tab3.markdown(dias_consecutivos.retornar_tabela())

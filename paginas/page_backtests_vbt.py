import streamlit as st
import yfinance as yf
import pandas as pd
import vectorbt as vbt
import ta
from st_pages import add_page_title
import numpy as np
import fundamentus as fd
from utils.streamlit_utils import adicionar_avisos_dev
from datetime import date, timedelta

hoje = date.today()
ano_passado = date(hoje.year - 1, hoje.month, hoje.day)


@st.cache_data(show_spinner="Buscando todos os dados fundamentalistas...", ttl=3600)
def get_resultado():
    return fd.get_resultado()


def validar():
    from datetime import date, timedelta
    from dateutil.relativedelta import relativedelta

    if len(papeis_selecionados) < 2:
        with alertas:
            st.error(icon="🚨", body="Selecione pelo menos 2 tickers.")
        st.stop()

    diferenca_meses = (data_final.year - data_inicial.year) * \
        12 + (data_final.month - data_inicial.month)

    if diferenca_meses < 1:
        with alertas:
            st.error(
                icon="🚨", body="Selecione as datas com pelo menos 1 mês de intervalo.")
        st.stop()


st.set_page_config(layout="wide")
add_page_title()
adicionar_avisos_dev()
alertas = st.container()

estrategias = ['Buy and hold']

lista_ibovespa = ['RRRP3', 'ALSO3', 'ALPA4', 'ABEV3', 'ARZZ3',
                  'ASAI3', 'AZUL4', 'B3SA3',  'BBSE3', 'BBDC3', 'BBDC4',
                  'BRAP4', 'BBAS3', 'BRKM5', 'BRFS3', 'BPAC11', 'CRFB3',
                  'CCRO3', 'CMIG4', 'CIEL3', 'COGN3', 'CPLE6', 'CSAN3',
                  'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'DXCO3', 'ELET3',
                  'ELET6', 'EMBR3', 'ENBR3', 'ENGI11', 'ENEV3',
                  'EGIE3', 'EQTL3', 'EZTC3', 'FLRY3', 'GGBR4', 'GOAU4',
                  'GOLL4', 'NTCO3', 'SOMA3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ITSA4',
                  'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LWSA3', 'LREN3', 'MGLU3', 'MRFG3',
                  'CASH3', 'BEEF3', 'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'PRIO3',
                  'PETZ3', 'RADL3', 'RAIZ4', 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'SMTO3',
                  'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 'TIMS3', 'TOTS3', 'UGPA3',
                  'USIM5', 'VALE3', 'VIIA3', 'VBBR3', 'WEGE3', 'YDUQ3']


with st.form("form"):
    estrategia_selecionada = st.selectbox(
        'Selecione uma estratégia:', estrategias, disabled=True)

    check_analisar_carteira = st.checkbox(
        "Analisar carteira?", value=True, disabled=True)

    papeis_selecionados = st.multiselect(
        'Selecione o(s) ticker(s) que compõe a carteira:', sorted(lista_ibovespa), ['PETR4', 'VALE3'])
    col1form, col2form, col3form = st.columns(3)
    with col1form:
        data_inicial = st.date_input("Data inicial:", ano_passado)
    with col2form:
        data_final = st.date_input("Data final:", hoje)
    with col3form:
        cash_inicial = st.number_input("R$ inicial:", 1000)
        taxa_livre_risco = st.number_input("Taxa livre de risco:", 0.003)

    if st.form_submit_button("Analisar"):
        validar()

        lista_ativos = list(map(lambda i: i+".SA", papeis_selecionados))
        valor_percentual = 1/len(lista_ativos)
        lista_percentuais = []
        for i in range(len(lista_ativos)):
            lista_percentuais.append(valor_percentual)

        carteira = vbt.YFData.download(
            lista_ativos, start=data_inicial.strftime('%Y-%m-%d'),
            end=data_final.strftime('%Y-%m-%d'), missing_columns='drop', missing_index='drop').get("Close")
        alocacao = pd.DataFrame.vbt.empty_like(carteira, fill_value=np.nan)
        alocacao.iloc[0] = lista_percentuais

        portfolio = vbt.Portfolio.from_orders(
            close=carteira, size=alocacao, size_type='targetpercent',
            group_by=True, cash_sharing=True, init_cash=cash_inicial, freq='d')

        stats1 = portfolio.stats(settings=dict(risk_free=taxa_livre_risco))
        stats2 = portfolio.returns_stats(
            settings=dict(risk_free=taxa_livre_risco))
        graph1 = portfolio.plot()
        graph2 = portfolio.drawdowns.plot(top_n=5)
        graph3 = portfolio.plot_underwater()

        tab1, tab2 = st.tabs(["📈 Gráficos", "🗃 Estatísticas"])

        with tab1:
            tab3, tab4, tab5 = st.tabs(
                ["Retorno acumulado", "Drawdown (top 5)", "Underwater"])
            tab3.subheader("Retorno acumulado")
            tab3.plotly_chart(graph1, use_container_width=True)
            tab4.subheader("Drawdown (top 5)")
            tab4.plotly_chart(graph2, use_container_width=True)
            tab5.subheader("Underwater")
            tab5.plotly_chart(graph3, use_container_width=True)
        with tab2:
            col1, col2 = st.columns(2)
            col1.write(stats1)
            col2.write(stats2)

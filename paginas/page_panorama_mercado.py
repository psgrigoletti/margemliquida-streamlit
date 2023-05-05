import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
from st_pages import add_page_title
import plotly.graph_objects as go

# Construção da página

st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

st.markdown(date.today().strftime('%d/%m/%Y'))
st.subheader("Mercados pelo Mundo")
dict_tickers = {
    "Bovespa": "^BVSP",
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DAX": "^GDAXI",
    "FTSE 100": "^FTSE",
    "Cruid Oil": "CL=F",
    "Gold": "GC=F",
    "BITCOIN": "BTC-USD",
    "ETHEREUM": "ETH-USD",
    "PETR4": "PETR4.SA",
    "VALE3": "VALE3.SA",
}

df_info = pd.DataFrame({'Ativo': dict_tickers.keys(),
                        'Ticker': dict_tickers.values()})
df_info['Ult. Valor'] = ''
df_info['%'] = ''
count = 0
with st.spinner("Baixando cotações..."):
    for ticker in dict_tickers.values():
        cotacoes = yf.download(ticker, period='5d')['Adj Close']
        variacao = ((cotacoes.iloc[-1]/cotacoes.iloc[-2])-1)*100
        df_info['Ult. Valor'][count] = round(cotacoes.iloc[-1], 2)
        df_info['%'][count] = round(variacao, 2)
        count += 1

# st.write(df_info)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(df_info['Ativo'][0], df_info['Ult. Valor']
              [0], delta=str(df_info['%'][0]) + '%')
    st.metric(df_info['Ativo'][1], df_info['Ult. Valor']
              [1], delta=str(df_info['%'][1]) + '%')
    st.metric(df_info['Ativo'][2], df_info['Ult. Valor']
              [2], delta=str(df_info['%'][2]) + '%')

with col2:
    st.metric(df_info['Ativo'][3], df_info['Ult. Valor']
              [3], delta=str(df_info['%'][3]) + '%')
    st.metric(df_info['Ativo'][4], df_info['Ult. Valor']
              [4], delta=str(df_info['%'][4]) + '%')
    st.metric(df_info['Ativo'][5], df_info['Ult. Valor']
              [5], delta=str(df_info['%'][5]) + '%')

with col3:
    st.metric(df_info['Ativo'][6], df_info['Ult. Valor']
              [6], delta=str(df_info['%'][6]) + '%')
    st.metric(df_info['Ativo'][7], df_info['Ult. Valor']
              [7], delta=str(df_info['%'][7]) + '%')
    st.metric(df_info['Ativo'][8], df_info['Ult. Valor']
              [8], delta=str(df_info['%'][8]) + '%')

st.markdown("---")
st.subheader("Comportamento durante o dia")

lista_ticker = [x for x in dict_tickers.keys()]
indice = st.selectbox("Selecione o ticker", lista_ticker)
ticker_diario = yf.download(dict_tickers.get(
    indice), period='1d', interval='5m')

fig = go.Figure(data=[go.Candlestick(x=ticker_diario.index, open=ticker_diario['Open'],
                high=ticker_diario['High'], close=ticker_diario['Close'], low=ticker_diario['Low'])])
fig.update_layout(title=indice, xaxis_rangeslider_visible=False)

st.plotly_chart(fig)

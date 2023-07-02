import streamlit as st
import datetime
from libs.dividendos import Dividendos 
import logging

from st_pages import Page, Section, show_pages, add_page_title

st.set_page_config(layout="wide")
st.markdown("# 〰️ Dividendos")
add_page_title()
mensagens = st.container()

@st.cache_data
def retornar_dados(ticker, data_inicial, data_final):
    logging.log(logging.INFO, f"Buscando histórico de {ticker} entre {data_inicial} e {data_final}")
    d = Dividendos()
    dados = d.retornar_dados(ticker, data_inicial, data_final)
    return dados
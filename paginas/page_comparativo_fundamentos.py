import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
from st_pages import add_page_title
import plotly.graph_objects as go
import fundamentus as fd

# Construção da página

st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

lista_tickers = fd.list_papel_all()

comparar = st.checkbox("Comparar 2 ativos?")
col1, col2 = st.columns(2)

with col1:
    with st.expander("Ativo 1", expanded=True):
        papel1 = st.selectbox('Selecione o 1º papel', lista_tickers)
        info_papel1 = fd.get_detalhes_papel(papel1)
        st.write("**Empresa**:", info_papel1['Empresa'][0])
        st.write("**Setor**:", info_papel1['Setor'][0])
        st.write("**Subsetor**:", info_papel1['Subsetor'][0])
        st.write("**Valor de Mercado**:",
                 f"R$ {float(info_papel1['Valor_de_mercado'][0]):,.2f}")
        st.write("**Patrimônio Líquido**:",
                 f"R$ {float(info_papel1['Patrim_Liq'][0]):,.2f}")
        st.write(
            "**Receita Líquida 12m**:", f"R$ {float(info_papel1['Receita_Liquida_12m'][0]):,.2f}")
        st.write("**Dívida Bruta**:",
                 f"R$ {float(info_papel1['Div_Bruta'][0]):,.2f}")
        st.write("**Dívida Líquida**:",
                 f"R$ {float(info_papel1['Div_Liquida'][0]):,.2f}")
        st.write("**P/L**:", f"R$ {float(info_papel1['PL'][0]):,.2f}")
        st.write("**Dividend Yield**:", f"{info_papel1['Div_Yield'][0]}")

if comparar:
    with col2:
        with st.expander("Ativo 2", expanded=True):
            papel2 = st.selectbox('Selecione o 2º papel', lista_tickers)
            info_papel2 = fd.get_detalhes_papel(papel2)
            st.write("**Empresa**:", info_papel2['Empresa'][0])
            st.write("**Setor**:", info_papel2['Setor'][0])
            st.write("**Subsetor**:", info_papel2['Subsetor'][0])
            st.write("**Valor de Mercado**:",
                     f"R$ {float(info_papel2['Valor_de_mercado'][0]):,.2f}")
            st.write("**Patrimônio Líquido**:",
                     f"R$ {float(info_papel2['Patrim_Liq'][0]):,.2f}")
            st.write(
                "**Receita Líquida 12m**:", f"R$ {float(info_papel2['Receita_Liquida_12m'][0]):,.2f}")
            st.write("**Dívida Bruta**:",
                     f"R$ {float(info_papel2['Div_Bruta'][0]):,.2f}")
            st.write("**Dívida Líquida**:",
                     f"R$ {float(info_papel2['Div_Liquida'][0]):,.2f}")
            st.write("**P/L**:", f"R$ {float(info_papel2['PL'][0]):,.2f}")
            st.write("**Dividend Yield**:", f"{info_papel2['Div_Yield'][0]}")

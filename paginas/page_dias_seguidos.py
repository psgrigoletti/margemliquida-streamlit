import streamlit as st
import datetime
from libs.dias_consecutivos import DiasConsecutivos
from libs.dividendos import Dividendos 
import logging

from st_pages import Page, Section, show_pages, add_page_title

st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

col1, col2, col3 = st.columns(3)
ticker = col1.text_input("Ticker:", value="PETR4.SA")
data_inicial = col2.date_input("Data inicial:", value=datetime.date(2020, 1, 1))
data_final = col3.date_input("Data final:", value=datetime.date(2023, 4, 1))

st.markdown(f"#### Buscar por:")
col5, col6, _,_,_ = st.columns(5)
dias_consecutivos = col5.number_input("Dias consecutivos:", min_value=3, max_value=10, value=5)
direcao = col6.select_slider("Tendência:", ["down", "up"])

st.markdown("#### Análise/Resultado:")
col7, col8, _ = st.columns(3)
dias_analise = col7.multiselect("Analisar n dias após:", [1,2,3,5,10,15], [1,2,5,10])
mostrar_grafico = col7.checkbox("Mostrar Gráfico:", value=True)
if st.button("Analisar"):
    dias_consecutivos = DiasConsecutivos(ticker=ticker, dias_apos=dias_analise, 
                                         end_date=data_final, start_date=data_inicial,
                                         direcao=direcao, dias_consecutivos=dias_consecutivos)
    if mostrar_grafico:
        tab1, tab2, tab3 = st.tabs(["Gráfico", "Relatório", "Tabela"])
        tab1.plotly_chart(dias_consecutivos.retornar_grafico(), use_container_width=True)
        tab2.markdown(dias_consecutivos.retornar_relatorio())
        tab3.markdown(dias_consecutivos.retornar_tabela())
    else:
        tab2, tab3 = st.tabs(["Relatório", "Tabela"])
        tab2.markdown(dias_consecutivos.retornar_relatorio())
        tab3.markdown(dias_consecutivos.retornar_tabela())        
        
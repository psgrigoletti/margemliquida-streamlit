import streamlit as st
import datetime
from libs.dias_consecutivos import DiasConsecutivos
import logging
from st_pages import add_page_title

@st.cache_data
def buscar_dados_ticker(ticker, dias_analise, data_final, data_inicial, direcao, dias_consecutivos):
    logging.log(logging.INFO, f"Buscando histórico de {ticker} entre {data_inicial} e {data_final}")
    dias_consecutivos = DiasConsecutivos(ticker=ticker, dias_apos=dias_analise, 
                                         end_date=data_final, start_date=data_inicial,
                                         direcao=direcao, dias_consecutivos=dias_consecutivos)
    return dias_consecutivos    

def validar_parametros(ticker, data_inicial, data_final, dias_analise):
    if not ticker:
        mensagens.error('Ticker não informado.', icon="🚨")
        st.stop()
    
    if not data_inicial:
        mensagens.error('Data inicial não informada.', icon="🚨")
        st.stop()

    if not data_final:
        mensagens.error('Data final não informada.', icon="🚨")
        st.stop()
    
    if data_final <= data_inicial:
        mensagens.error('Data inicial deve ser menor que a Data final.', icon="🚨")
        st.stop()

    if not dias_analise or len(dias_analise)==0:
        mensagens.error('Selecione pelo menos um valor em \'Analisar n dias após\'.', icon="🚨")
        st.stop()
        
st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

col1, col2, col3 = st.columns(3)
ticker = col1.text_input("Ticker:", value="PETR4.SA")
data_inicial = col2.date_input("Data inicial:", value=datetime.date(2020, 1, 1))
data_final = col3.date_input("Data final:", value=datetime.date(2023, 4, 1))

st.markdown("#### Buscar por:")
col5, col6, _,_,_ = st.columns(5)
dias_consecutivos = col5.number_input("Dias consecutivos:", min_value=3, max_value=10, value=5)
direcao = col6.select_slider("Tendência:", ["Baixa", "Alta"])

st.markdown("#### Análise/Resultado:")
dias_analise = st.multiselect("Analisar n dias após:", [1,2,3,5,10,15,20], [1,2,5,10])
mostrar_grafico = st.checkbox("Mostrar Gráfico", value=True)
if st.button("Analisar"):
    validar_parametros(ticker, data_inicial, data_final, dias_analise)
    dias_consecutivos = buscar_dados_ticker(ticker, dias_analise, 
                                         data_final, data_inicial,
                                         direcao, dias_consecutivos)
    if dias_consecutivos.quantidade_periodos_encontrados == 0:
        mensagens.error("Nenhum resultado encontrado.", icon="🚨")
        st.stop()
    else:
        mensagens.success("Análise realizada com sucesso.", icon="✅")
    
    if mostrar_grafico:
        tab1, tab2, tab3 = st.tabs(["Gráfico", "Relatório", "Tabela"])
        tab1.plotly_chart(dias_consecutivos.retornar_grafico(), use_container_width=True)
        tab2.markdown(dias_consecutivos.retornar_relatorio())
        tab3.markdown(dias_consecutivos.retornar_tabela())
    else:
        tab2, tab3 = st.tabs(["Relatório", "Tabela"])
        tab2.markdown(dias_consecutivos.retornar_relatorio())
        tab3.markdown(dias_consecutivos.retornar_tabela())

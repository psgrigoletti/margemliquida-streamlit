import streamlit as st
import datetime
from libs.dividendos import Dividendos 
from libs.carteira_global import CarteiraGlobal 
# from libs.carteira_teorica_b3 import CarteiraTeoricaB3
import logging
from st_pages import add_page_title

# @st.cache_data
# def retornar_carteira_teorica(carteira="IBOV"):
#     logging.log(logging.INFO, f"Buscando carteira teórica {carteira}")
#     ctb3 = CarteiraTeoricaB3()
#     df = ctb3.busca_carteira_teorica(carteira)
#     lista = df['Código'].to_list()
#     lista.sort()
#     return lista

# @st.cache_data
# def retornar_lista_acoes():
#     logging.log(logging.INFO, f"Buscando lista de ações disponíveis")
#     cg = CarteiraGlobal()
#     cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
#     lista = cg.retornar_lista_acoes()
#     return lista

# @st.cache_data
# def retornar_lista_fiis():
#     logging.log(logging.INFO, f"Buscando lista de FIIs disponíveis")
#     cg = CarteiraGlobal()
#     cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
#     lista = cg.retornar_lista_fiis()
#     return lista

@st.cache_data
def retornar_dados_fii(ticker):
    logging.log(logging.INFO, f"Buscando dados gerais do FII {ticker}")
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    dados = cg.retonar_dados_fiis(ticker)
    return dados

@st.cache_data
def retornar_dados_acao(ticker):
    logging.log(logging.INFO, f"Buscando dados gerais da Ação {ticker}")
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    dados = cg.retonar_dados_acoes(ticker)
    return dados

@st.cache_data
def retornar_dados(ticker, data_inicial, data_final):
    logging.log(logging.INFO, f"Buscando histórico de {ticker} entre {data_inicial} e {data_final}")
    d = Dividendos()
    d.setar_chave_carteira_global(st.secrets["carteira_global"]["x_api_key"])
    dados = d.retornar_dados(ticker, data_inicial, data_final)
    return dados

def validar_parametros(tipo, ticker, data_inicial, data_final):
    if not ticker:
        mensagens.error('Ticker não informado.', icon="🚨")
        st.stop()
        return False
    
    if not data_inicial:
        mensagens.error('Data inicial não informada.', icon="🚨")
        st.stop()
        return False

    if not data_final:
        mensagens.error('Data final não informada.', icon="🚨")
        st.stop()
        return False
    
    if data_final <= data_inicial:
        mensagens.error('Data inicial deve ser menor que a Data final.', icon="🚨")
        st.stop()
        return False
    
    if tipo == "Ações":
        try:
            dados = retornar_dados_acao(ticker)
            if(not dados):
                mensagens.error(f'Ticker {ticker} não encontrado.', icon="🚨")
                st.stop()
                return False
            else:
                return True
        except:
            mensagens.error('Ticker não encontrado.', icon="🚨")
            st.stop()
            return False

    elif tipo == "FIIs":
        try:
            dados = retornar_dados_fii(ticker)
            if(not dados):
                mensagens.error(f'Ticker {ticker} não encontrado.', icon="🚨")
                st.stop()
                return False
            else:
                return True
        except:
            mensagens.error('Ticker não encontrado.', icon="🚨")
            st.stop()
            return False
    else:
        mensagens.error('É obrigatório selecionar um Tipo.', icon="🚨")
        st.stop()
        return False 
        
    return True
        
st.set_page_config(layout="wide")
add_page_title()

st.markdown("# Dividendos")

mensagens = st.container()

tipo = st.radio(
    "Tipo",
    ('Ações', 'FIIs'))

col1, col2, col3 = st.columns([1,1,1])
#ticker = col1.input_text("Informe o ticker:")
# if tipo == 'Ações':
#     ticker = col1.selectbox(
#         'Selecione a Ação que deseja analisar:',
#         carteira_ibov)
# else:
#     ticker = col1.selectbox(
#         'Selecione o FII que deseja analisar:',
#         fiis) 

ticker = col1.text_input('Informe o ticker:', "")

data_inicial = col2.date_input(
    "Data inicial:",
    datetime.date(2018, 1, 1))

data_final = col3.date_input(
    "Data final:",
    datetime.date(2023, 3, 12))

if st.button("Buscar informações", help="Buscar informações"):
    if validar_parametros(tipo, ticker, data_inicial, data_final):
        try:
            if tipo == "Ações":
                dados_ticker = retornar_dados_acao(ticker)
            elif tipo == "FIIs":
                dados_ticker = retornar_dados_fii(ticker)
                
            dados = retornar_dados(ticker, data_inicial, data_final)
            sobre, graficos, tabela = st.tabs(["Sobre o Ticker", "Gráficos", "Tabela"])
                
            with sobre:
                # st.json(dados_ticker)
                st.markdown(f"**Tipo:** {dados_ticker['equity_type_name']}")
                st.markdown(f"**Setor:** {dados_ticker['company_sector']}")
                st.markdown(f"**Sub-setor:** {dados_ticker['company_sub_sector']}")
                st.markdown(f"**Segmento:** {dados_ticker['company_segment']}")
                if dados_ticker['equity_type_name'] == "Ações":
                    st.markdown(f"**Atividade:** {dados_ticker['company_activity']}")
                    
                if dados_ticker['equity_type_name'] == "FII":
                    st.markdown(f"**Nome do fundo:** {dados_ticker['name']}")    
                    st.markdown(f"**Duração:** {dados_ticker['duration_period']}")    
                    st.markdown(f"**Gestora:** {dados_ticker['manager_name']}")
                    st.markdown(f"**CNPJ da gestora:** {dados_ticker['manager_cnpj']}")               
                    st.markdown(f"**Tipo de gestão:** {dados_ticker['management_type']}")               
                                    
                st.markdown(f"**CNPJ:** {dados_ticker['cnpj']}", )
                st.markdown(f"**Site:** {dados_ticker['site']}")
                st.markdown(f"**Código CVM:** {dados_ticker['cvm_code']}")
            
            with tabela:
                st.dataframe(dados, width=0, height=0, use_container_width=True)

            with graficos:
                data_inicial_formatada = data_inicial.strftime("%d/%m/%Y")
                data_final_formatada = data_final.strftime("%d/%m/%Y")        
                
                d = Dividendos()
                d.setar_chave_carteira_global(st.secrets["carteira_global"]["x_api_key"])       
                st.markdown(f"## {ticker} - Evolução dos Dividendos e Dividend Yield")
                st.plotly_chart(d.retornar_grafico_evolucao(ticker, dados), use_container_width=True)
                #st.bar_chart(dados['Dividends'], width=0, height=0, use_container_width=True)
                
                st.markdown(f"## {ticker} - Tendência dos Dividendos e Dividend Yield")
                #st.line_chart(dados['Dividends'].rolling(10).mean(), width=0, height=0, use_container_width=True)
                st.plotly_chart(d.retornar_grafico_tendencia(ticker, dados), use_container_width=True)

                st.markdown(f"## {ticker} - Dividendos pagos por mês")
                st.markdown(f"Soma dos dividendos pagos, em R$, agrupados por mês.")
                st.markdown(f"Considerando o período entre {data_inicial_formatada} e {data_final_formatada}.")
                #div_mes = dados.groupby(['NomeMês'])[['NomeMês', 'Mês', 'Dividends']].sum(numeric_only=True).head().sort_values('Mês')['Dividends']
                #st.bar_chart(div_mes, width=0, height=0, use_container_width=True)
                st.plotly_chart(d.retornar_grafico_mensal(ticker, dados), use_container_width=True)

                st.markdown(f"## {ticker} - Dividendos pagos por ano")
                st.markdown(f"Soma dos dividendos pagos, em R$, agrupados por ano.") 
                st.markdown(f"Considerando o período entre {data_inicial_formatada} e {data_final_formatada}.")
                #st.bar_chart(dados.groupby(['Ano'])['Dividends'].sum(numeric_only=True), width=0, height=0, use_container_width=True)
                st.plotly_chart(d.retornar_grafico_anual(ticker, dados), use_container_width=True)

                st.markdown(f"## {ticker} - Número de vezes que pagou dividendos por ano")
                st.markdown(f"Considerando o período entre {data_inicial_formatada} e {data_final_formatada}.")
                st.plotly_chart(d.retornar_grafico_quantidade_pagamentos_anual(ticker, dados), use_container_width=True)  
                
                # st.markdown(f"## Dividend Yield de {ticker}")
                # dividend_yield = dados['DY'] # dividir pelo último valor em cada ano (multiplicar por 100)
                # st.bar_chart(dividend_yield, width=0, height=0, use_container_width=True)
        except:
            mensagens.error('Erro ao buscar os dados. Verifique os parâmetros usados.', icon="🚨")
            st.stop()

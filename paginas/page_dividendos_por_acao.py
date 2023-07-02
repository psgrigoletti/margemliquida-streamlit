import streamlit as st
import datetime
from libs.dividendos import Dividendos 
from libs.market_data.carteira_global import CarteiraGlobal 
import logging
from utils.data_hora_utils import DataHoraUtils

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

def validar_parametros(tipo, ticker, data_inicial, data_final, mensagens):
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
    
    if tipo == "Ações":
        try:
            dados = retornar_dados_acao(ticker)
            if(not dados):
                mensagens.error(f'Ticker {ticker} não encontrado.', icon="🚨")
                st.stop()
            else:
                return True
        except(Exception):
            mensagens.error('Ticker não encontrado.', icon="🚨")
            st.stop()

    elif tipo == "FIIs":
        try:
            dados = retornar_dados_fii(ticker)
            if(not dados):
                mensagens.error(f'Ticker {ticker} não encontrado.', icon="🚨")
                st.stop()
            else:
                return True
        except(Exception):
            mensagens.error('Ticker não encontrado.', icon="🚨")
            st.stop()
    else:
        mensagens.error('É obrigatório selecionar um Tipo.', icon="🚨")
        st.stop()

def gerar_bloco_sobre(dados_ticker):
    # st.json(dados_ticker)
    if dados_ticker['equity_type_name'] == "Ações":
        st.metric("Nome da empresa:", f"{dados_ticker['name']}", delta=None, delta_color="normal", help=None, label_visibility="visible")
        
        st.markdown(f"**Tipo:** {dados_ticker['equity_type_name']} {dados_ticker['specification']}")
        #st.markdown(f"**Nome da empresa:** {dados_ticker['name']}")            
        st.markdown(f"**Setor:** {dados_ticker['company_sector']}")
        st.markdown(f"**Sub-setor:** {dados_ticker['company_sub_sector']}")
        st.markdown(f"**Segmento:** {dados_ticker['company_segment']}")
        st.markdown(f"**Atividade:** {dados_ticker['company_activity']}")
        st.markdown(f"**CNPJ da empresa:** {dados_ticker['cnpj']}", )
        st.markdown(f"**Site:** {dados_ticker['site']}")
        st.markdown(f"**Código CVM:** {dados_ticker['cvm_code']}")
        
    if dados_ticker['equity_type_name'] == "FII":
        st.metric("Nome da fundo:", f"{dados_ticker['name']}", delta=None, delta_color="normal", help=None, label_visibility="visible")

        #st.markdown(f"**Nome do fundo:** {dados_ticker['name']}")    
        st.markdown(f"**Nome completo:** {dados_ticker['fnet_name']}")
        st.markdown(f"**Segmento:** {dados_ticker['segment']}")
        st.markdown(f"**Site:** {dados_ticker['site']}")
        
        st.markdown(f"**Data inicial:** {dados_ticker['initial_date']}")    
        st.markdown(f"**Duração:** {dados_ticker['duration_period']}")    
        st.markdown(f"**Tipo de gestão:** {dados_ticker['management_type']}")               
        st.markdown(f"**Gestor:** {dados_ticker['manager_name']}")
        st.markdown(f"**CNPJ do Gestor:** {dados_ticker['manager_cnpj']}")  
        st.markdown(f"**Site do Gestor:** {dados_ticker['manager_website']}")  

## Construção da página
        
def main():
    st.title(":dragon: Inflação no Brasil", )
    mensagens = st.container()

    ## Formulário

    tipo = st.radio("Tipo", ('Ações', 'FIIs'), horizontal=True)
    col1, col2, col3 = st.columns([1,1,1])
    ticker = col1.text_input('Ticker:', "")
    data_inicial = col2.date_input("Data inicial:", datetime.date(2018, 1, 1))
    data_final = col3.date_input("Data final:", datetime.datetime.now())

    if st.button("Pesquisar", help="Pesquisar"):
        mensagens.empty()
        validar_parametros(tipo, ticker, data_inicial, data_final, mensagens)
        
        try:
            if tipo == "Ações":
                dados_ticker = retornar_dados_acao(ticker)
            elif tipo == "FIIs":
                dados_ticker = retornar_dados_fii(ticker)
                
            dados = retornar_dados(ticker, data_inicial, data_final)
            sobre, graficos, tabela = st.tabs(["Sobre o Ticker", "📈 Gráficos", "🗃 Dados"])
                
            with sobre:
                gerar_bloco_sobre(dados_ticker)
            
            with tabela:
                st.dataframe(dados, width=0, height=0, use_container_width=True)

            with graficos:
                data_inicial_formatada = DataHoraUtils.retorna_data_formato_ddmmyyyy(data_inicial)
                data_final_formatada = DataHoraUtils.retorna_data_formato_ddmmyyyy(data_final)        
                
                d = Dividendos()
                d.setar_chave_carteira_global(st.secrets["carteira_global"]["x_api_key"])       
                st.markdown(f"## {ticker} - Evolução dos Dividendos e Dividend Yield")
                st.plotly_chart(d.retornar_grafico_evolucao(ticker, dados), use_container_width=True)
                
                st.markdown(f"## {ticker} - Tendência dos Dividendos e Dividend Yield")
                st.plotly_chart(d.retornar_grafico_tendencia(ticker, dados), use_container_width=True)

                st.markdown(f"## {ticker} - Dividendos pagos por mês")
                st.markdown(f"Soma dos dividendos pagos, em R$, agrupados por mês.")
                st.markdown(f"Considerando o período entre {data_inicial_formatada} e {data_final_formatada}.")
                st.plotly_chart(d.retornar_grafico_mensal(ticker, dados), use_container_width=True)

                st.markdown(f"## {ticker} - Dividendos pagos por ano")
                st.markdown(f"Soma dos dividendos pagos, em R$, agrupados por ano.") 
                st.markdown(f"Considerando o período entre {data_inicial_formatada} e {data_final_formatada}.")
                st.plotly_chart(d.retornar_grafico_anual(ticker, dados), use_container_width=True)

                st.markdown(f"## {ticker} - Número de vezes que pagou dividendos por ano")
                st.markdown(f"Considerando o período entre {data_inicial_formatada} e {data_final_formatada}.")
                st.plotly_chart(d.retornar_grafico_quantidade_pagamentos_anual(ticker, dados), use_container_width=True)  

            mensagens.success("Pesquisa realizada com sucesso.", icon="✅")

        except(Exception):
            mensagens.error('Erro ao buscar os dados. Verifique os parâmetros usados.', icon="🚨")
            st.stop()

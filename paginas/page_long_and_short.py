import datetime
import streamlit as st
from libs.analisador_cointegracao import AnalisadorCointegracao
from st_pages import add_page_title
from libs.long_and_short.analisador_correlacao import AnalisadorCorrelacao
from libs.long_and_short.buscador_dados import BuscadorDados
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# @st.cache_data
def buscar_cotacoes_ativos(ativo_1, ativo_2):
    buscador_dados = BuscadorDados()
    buscador_dados.busca_ativos_especificos("2020-01-01", "2023-03-18", lista_ativos = [ativo_1, ativo_2])
    df = buscador_dados.retorna_dados()
    return df

def make_markdown_table(array):

    """ Input: Python list with rows of table as lists
               First element as header. 
        Output: String to put into a .md file 
        
    Ex Input: 
        [["Name", "Age", "Height"],
         ["Jake", 20, 5'10],
         ["Mary", 21, 5'7]] 
    """


    markdown = "\n" + str("| ")

    for e in array[0]:
        to_add = " " + str(e) + str(" |")
        markdown += to_add
    markdown += "\n"

    markdown += '|'
    for i in range(len(array[0])):
        markdown += str("-------------- | ")
    markdown += "\n"

    for entry in array[1:]:
        markdown += str("| ")
        for e in entry:
            to_add = str(e) + str(" | ")
            markdown += to_add
        markdown += "\n"

    return markdown + "\n"    

resultado_cash_neutro = [["Financeiro Calculado", "", "R$ XX.XXX,XX"], 
                         ["**Ativos**", ":red_circle: **Short**", ":large_green_circle: **Long**"], 
                         ["", "AZUL4", "CVCB3"],
                         ["**Último preço**", "R$ XXX,00", "R$ XXX,00"],
                         ["**Quantidade**", "X.XXX", "X.XXX"],
                         ["**Financeiro**", "R$ XX.XXX,XX", "R$ XX.XXX,XX"]]




resultado_beta_neutro = [["Financeiro Calculado", "", "R$ XX.XXX,XX"], 
                         ["**Ativos**", ":red_circle: **Short**", ":large_green_circle: **Long**"], 
                         ["", "AZUL4", "CVCB3"],
                         ["**Último preço**", "R$ XXX,00", "R$ XXX,00"],
                         ["**Quantidade**", "X.XXX", "X.XXX"],
                         ["**Beta**", "X,XX", "X,XX"],
                         ["**Financeiro**", "R$ XX.XXX,XX", "R$ XX.XXX,XX"]]

## Construção da página
        
st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

col1, col2 = st.columns([2,3])
col3, col4 = col1.columns([1,1])

ativo_1 = col3.text_input("Ativo 1:", value="PETR3.SA", key="ativo_1")
ativo_2 = col4.text_input("Ativo 2:", value="PETR4.SA", key="ativo_2")

financeiro_desejado = col3.number_input("Financeiro desejado (R$):", value=20000)
opcoes_periodo_regressao = ['50 períodos', '100 períodos', '150 períodos', '200 períodos', '250 períodos']
periodo_regressao = col4.selectbox("Período de regressão:", options=opcoes_periodo_regressao)

if col1.button("Calcular cointegração", help="Calcular cointegração"):
    buscadorDados = BuscadorDados()
    buscadorDados.busca_ativos_especificos("2020-01-01", "2023-03-18", lista_ativos = [ativo_1, ativo_2])
    ultimos_n_dias = int(periodo_regressao.replace(" períodos", ""))
    df = buscadorDados.retorna_dados()
    lista_pares1 = buscadorDados.retorna_pares_ativos(retornar_invertidos=False)
    lista_pares2 = buscadorDados.retorna_pares_ativos(retornar_invertidos=True)
        
    with col2.expander("Gráficos **Correlação**:", expanded=True):
        analisador_correlacao = AnalisadorCorrelacao(df, lista_pares1, correlacao_minima='.1')
        grafico01, grafico02, grafico03, grafico04 = st.tabs(["Grafico 1", "Gráfico 2", "Gráfico 3", "Grafico 4"])
        grafico01.pyplot(fig=analisador_correlacao.retornar_grafico_1(ativo_1, ativo_2))
        grafico02.pyplot(fig=analisador_correlacao.retornar_grafico_2(ativo_1, ativo_2))
        grafico03.pyplot(fig=analisador_correlacao.retornar_grafico_3(ativo_1, ativo_2))        
        grafico04.pyplot(fig=analisador_correlacao.retornar_grafico_4(ativo_1, ativo_2))
            
    with col2.expander("Gráficos **Cointegração**:", expanded=True):
        analisador_cointegracao = AnalisadorCointegracao(df.tail(ultimos_n_dias), lista_pares2)
        analisador_cointegracao.gera_analise()
        grafico11, grafico12 = st.tabs(["Grafico 1", "Gráfico 2"])
        grafico11.pyplot(analisador_cointegracao.retornar_grafico_1())
        grafico12.pyplot(analisador_cointegracao.retornar_grafico_2())

    with col2.expander("Gráfico do resíduo:", expanded=True):
        st.markdown("blablabla")
        
    with col2.expander("Gráfico do ratio:", expanded=True):
        st.markdown("blablabla")
        
    with col2.expander("Resultado da cointegração:", expanded=True):
        st.markdown("blablabla")

    with col2.expander("Teste de Dickey-Fuller aumentado:", expanded=True):
        st.markdown("blablabla")
        
    cash_neutro, beta_neutro = col1.tabs(["Cash neutro", "Beta neutro"])
    
    cash_neutro.markdown(make_markdown_table(resultado_cash_neutro))
    beta_neutro.markdown(make_markdown_table(resultado_beta_neutro))    

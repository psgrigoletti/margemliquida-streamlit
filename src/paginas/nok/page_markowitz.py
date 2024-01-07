# import datetime
# import streamlit as st
# from st_pages import add_page_title
# import yfinance as yf
# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# from libs.markowitz import Markowitz


# ## Construção da página

# st.set_page_config(layout="wide")
# add_page_title()
# mensagens = st.container()

# @st.cache_data
# def buscar_precos_fechamento(acoes, data_inicial, data_final):
#     return yf.download(list(map((lambda x: x + ".SA"), acoes)), start=data_inicial, end=data_final)['Adj Close']

# acoes = st.multiselect(
#     'Selecione as ações que compõe a carteira:',
#     ['TAEE11', 'CPLE6', 'WIZS3', 'ITSA4', 'ABCB4', 'FLRY3', 'OFSA3', 'SAPR11'],
#     ['TAEE11', 'CPLE6', 'WIZS3'])

# col1, col2, col3, col4 = st.columns([1,1,1,1])
# data_inicial = col1.date_input("Data inicial:", datetime.date(2018, 1, 1))
# data_final = col2.date_input("Data final:", datetime.datetime.now())
# taxa_livre_de_risco = col3.number_input("Selic atual (taxa livre de risco) (percentual):", 13.75)
# numero_de_portfolios_aleatorios = col4.number_input("Número de portifólios aleatórios:", 5000)

# if st.button("Pesquisar", help="Pesquisar"):
#     mensagens.empty()
#     precos_fechamento = buscar_precos_fechamento(acoes, data_inicial, data_final)
#     markowitz = Markowitz(precos_fechamento, taxa_livre_de_risco, numero_de_portfolios_aleatorios)

#     with st.expander("Gráfico dos preços de fechamento:"):
#         st.pyplot(markowitz.retornar_grafico_de_precos())

#     with st.expander("Gráfico normalizado dos preços de fechamento:"):
#         st.pyplot(markowitz.retornar_grafico_de_precos_normalizados())

#     with st.expander("Gráfico dos retornos diários:"):
#         st.pyplot(markowitz.retornar_grafico_retornos_diarios())

#     with st.expander("Gráfico da Volatilidade e dos Retornos Médios:"):
#         st.pyplot(markowitz.retornar_grafico_vol_e_retornos_medios())

#     with st.expander("Matriz de Correlação:"):
#         st.pyplot(fig=markowitz.retornar_matriz_correlacao())

#     with st.expander("Matriz Risco x Retorno:"):
#         st.pyplot(fig=markowitz.retornar_matriz_risco_retorno())

#     with st.expander("Fronteira Eficiente 1:"):
#         st.pyplot(fig=markowitz.display_simulated_ef_with_random())

#     with st.expander("Fronteira Eficiente 2:"):
#         st.pyplot(fig=markowitz.apresentar_fronteira_eficiente_calculada_usando_random())

#     with st.expander("Otimização de Carteira:"):
#         st.pyplot(fig=markowitz.display_ef_with_selected())

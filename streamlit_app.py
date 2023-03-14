import streamlit as st
# import streamlit_authenticator as stauth
# import yaml
from st_pages import Page, Section, show_pages, add_page_title, add_indentation

# from yaml.loader import SafeLoader

st.set_page_config(page_title="Dashboard Margem Líquida", page_icon=None, 
                   layout="wide", initial_sidebar_state="auto", 
                   menu_items=None)

show_pages(
    [
        Page("streamlit_app.py", "Inicial", ":beginner:"),        
        Section(name="OK", icon=":white_check_mark:"),
        Page("paginas/page_dividendos_por_acao.py", "Dividendos por ação", ":heavy_dollar_sign:"),
        Page("paginas/page_tesouro_direto.py", "Tesouro Direto", ":flag-br:"),
        Section(name="Em desenvolvimento", icon=":computer:"),        
        Page("paginas/page_analise_fundamentalista.py", "Análise Fundamentalista", ":bank:"),
        Page("paginas/page_relatorio_focus.py", "Relatório Focus", ":newspaper:"),
        Page("paginas/page_dividendos_maiores_pagadores.py", "Maiores pagadores de dividendos", ":moneybag:"),
        Section(name="Testes", icon=":test_tube:"),        
        Page("paginas/page_test_webdriver.py", "Teste Webdriver", ":test_tube:"),        
    ]
)

# venv: https://www.alura.com.br/artigos/ambientes-virtuais-em-python
# emojis: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/

add_indentation() 
add_page_title()

st.markdown("### Sobre:")
st.markdown("Aplicação criada para exercitar os aprendizados no curso Python para Mercado Financeiro")
st.markdown("Versão: 0.0.1 - 13/03/2023")

st.markdown("### Curso:")
col1, col2 = st.columns([1,2])
col1.image("imagens/pmf.png", width=250)
col2.markdown("**Trading com Dados**: https://tradingcomdados.com/")
col2.markdown("**Curso Python para Mercado Financeiro**: https://hotmart.com/pt-br/marketplace/produtos/python-para-mercado-financeiro/")
st.markdown("### Contato:")
col4, col5 = st.columns([1,2])
col4.image("imagens/eu.jpeg", width=250)
col5.markdown("**Pablo Grigoletti** - psgrigoletti@gmail.com")
col5.markdown("**Github:** https://github.com/psgrigoletti/")
col5.markdown("**Linkedin:** https://www.linkedin.com/in/psgrigoletti/")
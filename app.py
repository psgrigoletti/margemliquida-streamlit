# https://www.alura.com.br/artigos/ambientes-virtuais-em-python

import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title

# import locale
# locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


st.set_page_config(
    page_title="Dashboard Margem Líquida",
    layout="wide",
)

add_page_title()

#st.markdown("# Página Principal")
#st.sidebar.markdown("# Página Principal")

# emojis: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
show_pages(
    [
        Page(st.secrets["pasta_ajustada"] + "app.py", "Inicial", ":beginner:"),        
        Section(name="Dividendos", icon=":wavy_dash:"),
        Page(st.secrets["pasta_ajustada"] + "pages/page_dividendos_por_acao.py", "Por ação", ":moneybag:"),
        Page(st.secrets["pasta_ajustada"] + "pages/page_dividendos_maiores_pagadores.py", "Maiores pagadores", ":moneybag:"),
        Section(name="Outros", icon=":mate_drink:"),        
        Page(st.secrets["pasta_ajustada"] + "pages/page_analise_fundamentalista.py", "Análise Fundamentalista", ":bank:"),
        Page(st.secrets["pasta_ajustada"] + "pages/page_relatorio_focus.py", "Relatório Focus", ":newspaper:"),
        Page(st.secrets["pasta_ajustada"] + "pages/page_tesouro_direto.py", "Tesouro Direto", ":flag-br:"),
        Page(st.secrets["pasta_ajustada"] + "pages/page_test_webdriver.py", "Teste Webdriver", ":test_tube:"),        
    ]
)
st.markdown("### Sobre:")
st.markdown("Aplicação criada para exercitar os aprendizados no curso Python para Mercado Financeiro")
st.markdown("Versão: 0.0.1 - 13/03/2023")

st.markdown("### Curso:")
col1, col2 = st.columns([1,2])
col1.image(st.secrets["pasta_ajustada"] + "imagens/pmf.png", width=250)
col2.markdown("**Trading com Dados**: https://tradingcomdados.com/")
col2.markdown("**Curso Python para Mercado Financeiro**: https://hotmart.com/pt-br/marketplace/produtos/python-para-mercado-financeiro/")
st.markdown("### Contato:")
col4, col5 = st.columns([1,2])
col4.image(st.secrets["pasta_ajustada"] + "imagens/eu.jpeg", width=250)
col5.markdown("**Pablo Grigoletti** - psgrigoletti@gmail.com")
col5.markdown("**Github:** https://github.com/psgrigoletti/")
col5.markdown("**Linkedin:** https://www.linkedin.com/in/psgrigoletti/")

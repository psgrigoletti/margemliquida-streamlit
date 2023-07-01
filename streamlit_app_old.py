import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title, add_indentation

st.set_page_config(page_title="Dashboard Margem Líquida", page_icon=None,
                   layout="wide", initial_sidebar_state="auto",
                   menu_items=None)


def mostrar_pagina_autorizada():
    show_pages(
        [
            Page("streamlit_app.py", "Inicial", ":beginner:"),
            Section(name="OK", icon=":white_check_mark:"),
            Page("paginas/page_comparador_carteiras.py",
                 "Comparador de Carteiras", ":straight_ruler:"),
            Page("paginas/page_dividendos_por_acao.py",
                 "Dividendos por ação", ":heavy_dollar_sign:"),
            Page("paginas/page_dias_consecutivos.py",
                 "Estratégia Dias Consecutivos", ":infinity:"),
            Page("paginas/page_tesouro_direto.py",
                 "Tesouro Direto", ":flag-br:"),
            Page("paginas/page_relatorio_focus.py",
                 "Relatório Focus", ":newspaper:"),
            Page("paginas/page_juros_futuros.py",
                 "Juros Futuros", ":calendar:"),
            Page("paginas/page_inflacao.py", "Inflação no Brasil", ":dragon:"),
            Page("paginas/page_panorama_mercado.py",
                 "Panorama de Mercado", ":coffee:"),
            Page("paginas/page_rentabilidades_mensais.py",
                 "Rentabilidades Mensais", ":1234:"),
            Page("paginas/page_comparativo_fundamentos.py",
                 "Comparador de Fundamentos", ":tophat:"),
            Page("paginas/page_backtests.py",
                 "Backtests", ":chart:"),
            Page("paginas/page_backtests_vbt.py",
                 "Backtests com VectorBT", ":chart:"),
            Section(name="Em desenvolvimento", icon=":computer:"),
            Page("paginas/page_analise_fundamentalista.py",
                 "Análise Fundamentalista", ":bank:"),
            Page("paginas/page_dividendos_maiores_pagadores.py",
                 "Maiores pagadores de dividendos", ":moneybag:"),
            Page("paginas/page_markowitz.py", "Markowitz", ":compass:"),
            Page("paginas/page_long_and_short.py", "Long & Short", ":jigsaw:"),
            Section(name="Testes", icon=":test_tube:"),
            Page("paginas/page_test_webdriver.py",
                 "Teste Webdriver", ":test_tube:"),
        ]
    )

    # venv: https://www.alura.com.br/artigos/ambientes-virtuais-em-python
    # emojis: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
    # emojis: https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md

    add_indentation()
    add_page_title()

    st.markdown("### Sobre:")
    st.markdown(
        "Aplicação criada para exercitar os aprendizados no curso Python para Mercado Financeiro")
    st.markdown("Versão: 0.0.1 - 13/03/2023")

    st.markdown("### Curso:")
    col1, col2 = st.columns([1, 2])
    col1.image("imagens/pmf.png", width=250)
    col2.markdown("**Trading com Dados**: https://tradingcomdados.com/")
    col2.markdown(
        "**Curso Python para Mercado Financeiro**: https://hotmart.com/pt-br/marketplace/produtos/python-para-mercado-financeiro/")
    st.markdown("### Contato:")
    col4, col5 = st.columns([1, 2])
    col4.image("imagens/eu.jpeg", width=250)
    col5.markdown("**Pablo Grigoletti** - psgrigoletti@gmail.com")
    col5.markdown("**Github:** https://github.com/psgrigoletti/")
    col5.markdown("**Linkedin:** https://www.linkedin.com/in/psgrigoletti/")


if 'logado' not in st.session_state:
    st.session_state['logado'] = False
    st.header("Login")
    st.text_input("Usuário:")
    st.text_input("Senha:")
    if st.button("Entrar"):
        st.session_state['logado'] = True

if st.session_state['logado'] == True:
    mostrar_pagina_autorizada()

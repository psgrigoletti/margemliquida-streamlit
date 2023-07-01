import importlib
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import paginas.util as putil
from st_pages import Page, Section, show_pages


with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    print(config)

# hashed_passwords = stauth.Hasher(
#     ['psgrigoletti', 'nutri.fschumacher']).generate()
# print(hashed_passwords)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')


# def format_func(lista_paginas, name):
#     return descricoes[lista_paginas.index(name)]


# print(authentication_status)

if authentication_status:
    with st.sidebar:

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
                Page("paginas/page_inflacao.py",
                     "Inflação no Brasil", ":dragon:"),
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
                Page("paginas/page_long_and_short.py",
                     "Long & Short", ":jigsaw:"),
                Section(name="Testes", icon=":test_tube:"),
                Page("paginas/page_test_webdriver.py",
                     "Teste Webdriver", ":test_tube:"),
            ],
        )

        col1, col2 = st.columns([1, 3])

        with col1:
            authenticator.logout(':door:', 'main')

        with col2:
            st.write(f'Olá *{name}*')

        st.divider()

        # lista_nomes_arquivos_paginas = putil.listar()
        # descricoes = []
        # arquivos = []

        # for nome_arquivo in lista_nomes_arquivos_paginas:
        #     arquivo = importlib.import_module('.'+nome_arquivo, 'paginas')
        #     arquivos.append(arquivo)
        #     try:
        #         descricao = arquivo.descricao
        #     except:
        #         descricao = nome_arquivo
        #     descricoes.append(descricao)

        pagina_selecionada = st.selectbox(
            'Menu:', lista_nomes_arquivos_paginas)

        # st.button(descricao)

    if pagina_selecionada:
        arquivos[lista_nomes_arquivos_paginas.index(pagina_selecionada)].run()

elif authentication_status == False:
    st.error('Usuário/senha estão incorretos.')
elif authentication_status == None:
    st.warning('Por favor, informe usuário e senha.')

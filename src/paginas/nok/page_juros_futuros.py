# import streamlit as st
# from st_pages import add_page_title
# from libs.juros_futuros import JurosFuturos

# # Construção da página

# st.set_page_config(layout="wide")
# add_page_title()
# mensagens = st.container()
# mensagens.error(
#     icon="🚨", body="Infelizmente o site ADVFN bloqueou o acesso aos dados que usávamos para gerar os gráficos.")
# st.stop()


# @st.cache_resource(show_spinner="Buscando dados do juros futuro...", ttl=3600)
# def retornar_jf_com_dados_atualizados(anos, anos_anteriores, semanas):
#     juros_futuros = JurosFuturos()
#     juros_futuros.atualizar_dados(anos, anos_anteriores, semanas)
#     return juros_futuros


# def gerar_observacoes():
#     st.write("------")
#     st.write(
#         "Observação: Dados do site [ADVFN](https://br.advfn.com/) e [Anbima](https://www.anbima.com.br/).")


# juros_futuros = retornar_jf_com_dados_atualizados(5, 0, 5)

# por_titulo, por_vencimento, por_dias_uteis = st.tabs(
#     ["por Título", "por Data de Vencimento", "por Dias Úteis"])

# with por_titulo:
#     st.markdown("# Juros Futuros por Título (ADVFN)")
#     st.plotly_chart(juros_futuros.retornar_grafico_por_titulo())

# with por_vencimento:
#     st.markdown("# Juros Futuros por Data de Vencimento (ADVFN)")
#     st.plotly_chart(juros_futuros.retornar_grafico_por_data_vencimento())

# with por_dias_uteis:
#     st.markdown("# Juros Futuros por Dias Úteis (ADVFN e ANBIMA)")
#     st.plotly_chart(juros_futuros.retornar_grafico_por_dias_uteis())

# gerar_observacoes()

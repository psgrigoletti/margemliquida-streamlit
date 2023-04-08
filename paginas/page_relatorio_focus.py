import streamlit as st
from libs.relatorio_focus import RelatorioFocus
from st_pages import add_page_title
from utils.data_hora_utils import DataHoraUtils
import logging

## Construção da página
        
st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

@st.cache_resource
def atualizar_dados_relatorio_focus(data_atual):
    logging.log(logging.INFO, "Buscando dados do BCB")
    rf = RelatorioFocus()
    rf.atualizar_atualizar_dados()
    return rf     

agora = DataHoraUtils.retorna_data_atual_formato_ddmmyyyy()
try:
    rf = atualizar_dados_relatorio_focus(agora)
except Exception:
    mensagens.error('Erro ao buscar os dados do Banco Central do Brasil. Por favor tente mais tarde.', icon="🚨")
    st.stop()

selic, ipca = st.tabs(["SELIC", ":dragon: IPCA+"])

with selic:
    st.markdown("## Expectativa SELIC")
    st.plotly_chart(rf.retornar_grafico_selic(), use_container_width=True)

with ipca:
    st.markdown("## Expectativa IPCA")
    st.plotly_chart(rf.retornar_grafico_ipca(), use_container_width=True)

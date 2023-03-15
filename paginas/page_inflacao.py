import streamlit as st
from libs.inflacao import Inflacao
from st_pages import add_page_title
from utils.data_hora_utils import DataHoraUtils

## Construção da página
        
st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

@st.cache_resource
def retornar_inflacao_com_dados_atualizados(data):
    inflacao = Inflacao()
    inflacao.atualizar_dados()
    return inflacao    

inflacao = retornar_inflacao_com_dados_atualizados(DataHoraUtils.retorna_data_atual_formato_ddmmyyyy())

st.markdown("# IPCA acumulado em 12 meses")
st.plotly_chart(inflacao.retornar_grafico_acumulado_12m(), use_container_width=True)

st.markdown("# Contribuição de cada setor no IPCA")
st.plotly_chart(inflacao.retornar_grafico_por_grupo(), use_container_width=True)
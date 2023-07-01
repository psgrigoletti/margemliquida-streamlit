import streamlit as st
from libs.inflacao import Inflacao
from utils.data_hora_utils import DataHoraUtils


@st.cache_resource(show_spinner="Carregando dados...", ttl=60*5)
def retornar_inflacao_com_dados_atualizados(data):
    inflacao = Inflacao()
    inflacao.atualizar_dados()
    return inflacao


def carregar_dados(mensagens):
    inflacao = retornar_inflacao_com_dados_atualizados(
        DataHoraUtils.retorna_data_atual_formato_ddmmyyyy())

    st.markdown("# IPCA acumulado em 12 meses")
    st.plotly_chart(inflacao.retornar_grafico_acumulado_12m(),
                    use_container_width=True)

    st.markdown("# Contribuição de cada setor no IPCA")
    st.plotly_chart(inflacao.retornar_grafico_por_grupo(),
                    use_container_width=True)


def main():
    st.title(":dragon: Inflação no Brasil", )
    mensagens = st.container()

    if st.button("Carregar dados..."):
        carregar_dados(mensagens)

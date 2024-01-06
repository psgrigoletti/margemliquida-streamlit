from libs.analise_fundamentalista import AnaliseFundamentalista
from libs.dados_cvm import DadosCVM

import streamlit as st
from st_pages import Page, Section, show_pages, add_page_title
from utils.data_hora_utils import DataHoraUtils

add_page_title()


def buscar_demonstrativos(
    _af, empresas_selecionadas, anos_selecionados, periodos_selecionados
):
    if (
        len(empresas_selecionadas) > 0
        and len(anos_selecionados) > 0
        and len(periodos_selecionados) > 0
    ):
        df_filtradas = _af.df_dados_empresas_disponiveis[
            _af.df_dados_empresas_disponiveis.DENOM_SOCIAL.str.contains(
                "|".join(empresas_selecionadas), na=False
            )
        ]
        codigos_cvm = list(df_filtradas["CD_CVM"])
        empresas_selecionadas = list(df_filtradas["DENOM_SOCIAL"])
        codigos_cvm = list(map(lambda i: str(i).zfill(6), codigos_cvm))
        print("vai buscar demonstrativos")
        _af.buscar_demonstrativos(
            codigos_cvm, empresas_selecionadas, anos_selecionados, periodos_selecionados
        )


def gerar_graficos_fundamentalistas(_af):
    print("vai mostrar DRE")
    st.dataframe(_af.retonar_df_dre_completo())
    print("vai gerar o gráfico")
    st.plotly_chart(_af.gerar_grafico_anual(), use_container_width=True)


@st.cache_data
def buscar_empresas(data_atual):
    dados_cvm = DadosCVM()
    dados_cvm.buscar_empresas()
    return list(dados_cvm.df_dados_empresas_disponiveis["DENOM_SOCIAL"].unique())


# st.set_page_config(
#     page_title="Análise Fundamentalista",
#     layout="wide",
# )

hoje = DataHoraUtils.retorna_data_atual_formato_ddmmyyyy()

st.markdown("# Análise Fundamentalista")
st.sidebar.markdown("# Análise Fundamentalista")
empresas_selecionadas = st.multiselect(
    "Selecione os ativos:", buscar_empresas(hoje), []
)

anos_selecionados = st.multiselect(
    "Selecione os anos:", list([2019, 2020, 2021, 2022]), []
)

periodos_selecionados = st.multiselect(
    "Selecione os anos:", list(["ANUAL", "TRIMESTRAL"]), []
)

# if st.button("Buscar informações", help="Buscar informações"):
#     buscar_demonstrativos(af, empresas_selecionadas, anos_selecionados, periodos_selecionados)
#     gerar_graficos_fundamentalistas(af)

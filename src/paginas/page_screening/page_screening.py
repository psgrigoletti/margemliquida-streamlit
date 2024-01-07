import streamlit as st

from .aba_acoes import mostrar_tab_acoes
from .aba_fiis import mostrar_tab_fiis
from .cache import busca_df_acoes_do_cache, busca_df_fiis_do_cache
from .comuns import is_dados_carregados


def main():
    st.title(":star: Screening")
    st.write(
        "**Fonte**: https://www.fundamentus.com.br/ e https://api.carteiraglobal.com/"
    )
    alertas = st.empty()

    if st.button("Carregar dados...") or (is_dados_carregados()):
        busca_df_fiis_do_cache()
        busca_df_acoes_do_cache()
        tab_acoes, tab_fiis = st.tabs(["Ações", "FIIs"])
        with tab_acoes:
            mostrar_tab_acoes()

        with tab_fiis:
            mostrar_tab_fiis()

        with alertas:
            st.success("Filtros carregados com sucesso!", icon="✅")

"""Módulo utilitário para validações"""

import streamlit as st


class ValidacoesUtils:
    """Classe utilitária para validações"""

    @staticmethod
    def validar_condicao(
        condicao_erro: bool, onde: st.empty, mensagem_erro: str
    ) -> None:
        """validar_condicao _summary_

        Args:
            condicao_erro (bool): _description_
            onde (st.empty): _description_
            mensagem_erro (str): _description_
        """
        if condicao_erro:
            with onde:
                st.error(mensagem_erro, icon="🚨")
            st.stop()

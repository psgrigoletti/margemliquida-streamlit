import streamlit as st
from datetime import datetime
import os


def adicionar_avisos_dev():
    _, col_avisos = st.columns([7, 3])
    with col_avisos:
        st.write(
            "Encontrou algum problema? [me avise](https://github.com/psgrigoletti/margemliquida-streamlit/issues/new?title=escreva%20o%20seu%20titulo&body=escreva%20o%20seu%20comentario) por favor.")
        # Obter informações sobre o arquivo
        info = os.stat(__file__)
        # Extrair a data da última modificação
        mod_time = info.st_mtime
        # Converter o tempo em formato legível
        mod_time_str = datetime.fromtimestamp(
            mod_time).strftime('%d/%m/%Y %H:%M:%S')
        st.write(
            f"Última atualização do código desta página em: {mod_time_str}.")

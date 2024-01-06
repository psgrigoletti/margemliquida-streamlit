import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

import yaml
from yaml.loader import SafeLoader
from menu import Menu

st.set_page_config(page_title="Sistema Margem Líquida", layout="wide")

with open("./config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    None,
)

_, col1, _ = st.columns(3)
with col1:
    mensagens = st.empty()
    name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    with st.sidebar:
        st.markdown("### Sistema MargemLíquida")

        pagina = option_menu(
            menu_title=None,  # required
            options=Menu.labels,  # required
            icons=None,  # optional
            menu_icon="menu-down",  # optional
            default_index=0,  # optional
        )
        authenticator.logout(":door: Sair")
        st.write("---")
        st.markdown(f"Usuário: {name}")
        st.markdown("Versão 1.0")
        st.write("---")
        st.write("**Encontrou algum problema?**")
        st.write(
            "[Me avise](https://github.com/psgrigoletti/margemliquida-streamlit/issues/new?title=escreva%20o%20seu%20titulo&body=escreva%20o%20seu%20comentario) por favor."
        )

    Menu.carregar_pagina(pagina)
elif authentication_status == False:
    with mensagens:
        st.error("Usuário/senha estão incorretos.")
elif authentication_status == None:
    with mensagens:
        st.warning("Por favor, informe usuário e senha.")

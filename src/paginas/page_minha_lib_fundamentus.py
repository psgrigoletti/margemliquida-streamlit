import fundamentus as fd
import streamlit as st
from libs.market_data.fundamentus import lista as minha_fd
from requests_cache import DO_NOT_CACHE, CachedSession

session = CachedSession(expire_after=DO_NOT_CACHE)


def main():
    st.title(":test_tube: Minha Lib Fundamentus")
    st.write("**Fonte**: https://www.fundamentus.com.br/")

    if st.button("Carregar dados..."):
        st.write("Fundamentus Original")
        st.write(fd.get_resultado())

        st.write("Minha Lib Fundamentus")
        st.write(minha_fd.get_df_acoes(formato_original=True))

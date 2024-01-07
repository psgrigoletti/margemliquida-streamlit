def main():
    import streamlit as st

    st.markdown("### Sobre:")
    st.markdown(
        "Aplicação criada para exercitar os aprendizados no curso Python para Mercado Financeiro")

    st.markdown("### Curso:")
    col1, col2 = st.columns([1, 2])
    col1.image("imagens/pmf.png", width=250)
    col2.markdown("**Trading com Dados**: https://tradingcomdados.com/")
    col2.markdown(
        "**Curso Python para Mercado Financeiro**: https://hotmart.com/pt-br/marketplace/produtos/python-para-mercado-financeiro/")
    st.markdown("### Contato:")
    col4, col5 = st.columns([1, 2])
    col4.image("imagens/eu.jpeg", width=250)
    col5.markdown("**Pablo Grigoletti** - psgrigoletti@gmail.com")
    col5.markdown("**Github:** https://github.com/psgrigoletti/")
    col5.markdown("**Linkedin:** https://www.linkedin.com/in/psgrigoletti/")

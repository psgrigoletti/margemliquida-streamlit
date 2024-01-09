import pandas as pd
import streamlit as st


def main():
    st.title(":coin: Cotações na Binance")
    st.write("**Fonte**: https://api.binance.com")

    if st.button("Carregar dados..."):
        df = pd.read_json("https://api.binance.com/api/v3/ticker/24hr")
        st.write(df)

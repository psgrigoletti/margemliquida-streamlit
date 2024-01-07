import yfinance as yf
import streamlit as st
from libs.market_data.fundamentus.lista import (
    get_df_acoes,
    get_df_fiis,
    get_df_setores,
    get_df_acoes_do_setor,
)


@st.cache_data(show_spinner="Buscando dados fundamentalistas para ações.", ttl=3600)
def busca_dados_acoes():
    df = get_df_acoes()
    df = df[df["Div.Yield"] > 0]
    df = df[df["Cotação"] > 0]
    df = df[df["Liq. Corr."] > 0]
    df = df[df["Liq.2meses"] > 0]
    st.session_state["lista_acoes"] = df
    return df


@st.cache_data(show_spinner="Buscando dados fundamentalistas para FIIs.", ttl=3600)
def busca_dados_fiis():
    df = get_df_fiis()
    df = df[df["Dividend Yield"] > 0]
    df = df[df["Cotação"] > 0]
    df = df[df["Liquidez"] > 0]
    st.session_state["lista_fiis"] = df
    return df


@st.cache_data(show_spinner="Buscando dados no Yahoo Finance.", ttl=3600)
def buscar_dados_yahoo(tickers, data_inicial, data_final):
    df = yf.download(tickers, data_inicial, data_final)
    return df["Adj Close"]


@st.cache_data(show_spinner="Buscando dados no Carteira Global.", ttl=3600)
def buscar_dados_carteira_global(tickers, data_inicial, data_final):
    from libs.market_data.carteira_global import CarteiraGlobal

    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_cotacoes_fechamento(tickers, data_inicial, data_final)
    return df


@st.cache_data(show_spinner="Buscando dados do IFIX na Carteira Global.", ttl=3600)
def buscar_dados_ifix_carteira_global(data_inicial, data_final):
    from libs.market_data.carteira_global import CarteiraGlobal

    ID_IFIX = 20
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_dados_indice(ID_IFIX, data_inicial, data_final)
    df.rename(columns={"Close": "IFIX"}, inplace=True)
    return df


@st.cache_data(show_spinner="Buscando dados do IBOV na Carteira Global.", ttl=3600)
def buscar_dados_ibov_carteira_global(data_inicial, data_final):
    from libs.market_data.carteira_global import CarteiraGlobal

    ID_IBOV = 2
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_dados_indice(ID_IBOV, data_inicial, data_final)
    df.rename(columns={"Close": "IBOV"}, inplace=True)
    return df

import streamlit as st
import yfinance as yf
from libs.market_data.carteira_global import CarteiraGlobal
from libs.market_data.fundamentus import lista
from requests_cache import DO_NOT_CACHE, CachedSession

session = CachedSession(expire_after=DO_NOT_CACHE)


@st.cache_data(show_spinner="Buscando dados fundamentalistas para ações.", ttl=3600)
def busca_dados_acoes():
    df = lista.get_df_acoes()
    # df = df[df["Div.Yield"] > 0]
    # df = df[df["Cotação"] > 0]
    # df = df[df["Liq. Corr."] > 0]
    # df = df[df["Liq.2meses"] > 0]
    st.session_state["lista_acoes"] = df
    return df


@st.cache_data(show_spinner="Buscando dados fundamentalistas para FIIs.", ttl=3600)
def busca_dados_fiis():
    df = lista.get_df_fiis()
    # df = df[df["Dividend Yield"] > 0]
    # df = df[df["Cotação"] > 0]
    # df = df[df["Liquidez"] > 0]
    st.session_state["lista_fiis"] = df
    return df


@st.cache_data(show_spinner="Buscando dados no Yahoo Finance.", ttl=3600)
def buscar_dados_yahoo(tickers, data_inicial, data_final):
    df = yf.download(tickers, data_inicial, data_final)
    return df["Adj Close"]


@st.cache_data(show_spinner="Buscando dados no Carteira Global.", ttl=3600)
def buscar_dados_carteira_global(tickers, data_inicial, data_final):
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_cotacoes_fechamento(tickers, data_inicial, data_final)
    return df


@st.cache_data(show_spinner="Buscando dados do IFIX na Carteira Global.", ttl=3600)
def buscar_dados_ifix_carteira_global(data_inicial, data_final):
    ID_IFIX = 20
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_dados_indice(ID_IFIX, data_inicial, data_final)
    df.rename(columns={"Close": "IFIX"}, inplace=True)
    return df


@st.cache_data(show_spinner="Buscando dados do IBOV na Carteira Global.", ttl=3600)
def buscar_dados_ibov_carteira_global(data_inicial, data_final):
    ID_IBOV = 2
    cg = CarteiraGlobal()
    cg.setar_token(st.secrets["carteira_global"]["x_api_key"])
    df = cg.retonar_dados_indice(ID_IBOV, data_inicial, data_final)
    df.rename(columns={"Close": "IBOV"}, inplace=True)
    return df


def busca_df_fiis_do_cache():
    if "lista_fiis" not in st.session_state:
        df = busca_dados_fiis()
        st.session_state["lista_fiis"] = df
    else:
        df = st.session_state["lista_fiis"]
    return df


def busca_df_acoes_do_cache():
    if "lista_acoes" not in st.session_state:
        df = busca_dados_acoes()
        st.session_state["lista_acoes"] = df
    else:
        df = st.session_state["lista_acoes"]
    return df

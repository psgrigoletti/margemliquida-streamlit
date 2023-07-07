from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import libs.market_data.fundamentus.utils as utils

hdr = {
    "User-agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
    "Accept": "text/html, text/plain, text/css, text/sgml, */*;q=0.01",
    "Accept-Encoding": "gzip, deflate",
}


# def get_df_setores(hdr=hdr):
#     url = "https://www.fundamentus.com.br/buscaavancada.php"
#     content = requests.get(url, headers=hdr)
#     setores = bs.find("select", {"name": "City"})["content"]
#     print(setores)


# get_df_setores()


def get_df_fiis(hdr=hdr):
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    content = requests.get(url, headers=hdr)
    df = pd.read_html(
        content.text, decimal=",", thousands=".", attrs={"id": "tabelaResultado"}
    )[0]

    df["Dividend Yield"] = utils.perc_to_float(df["Dividend Yield"])
    df["FFO Yield"] = utils.perc_to_float(df["FFO Yield"])
    df["Cap Rate"] = utils.perc_to_float(df["Cap Rate"])
    df["Vacância Média"] = utils.perc_to_float(df["Vacância Média"])

    return df


def get_df_acoes(hdr=hdr):
    url = "https://www.fundamentus.com.br/resultado.php"
    content = requests.get(url, headers=hdr)
    df = pd.read_html(
        content.text, decimal=",", thousands=".", attrs={"id": "resultado"}
    )[0]

    df["Div.Yield"] = utils.perc_to_float(df["Div.Yield"])
    df["Mrg Ebit"] = utils.perc_to_float(df["Mrg Ebit"])
    df["Mrg. Líq."] = utils.perc_to_float(df["Mrg. Líq."])
    df["ROIC"] = utils.perc_to_float(df["ROIC"])
    df["ROE"] = utils.perc_to_float(df["ROE"])
    df["Cresc. Rec.5a"] = utils.perc_to_float(df["Cresc. Rec.5a"])

    return df

from bs4 import BeautifulSoup
import pandas as pd
import requests
from .utils import perc_to_float
import fundamentus as fd

hdr = {
    "User-agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201",
    "Accept": "text/html, text/plain, text/css, text/sgml, */*;q=0.01",
    "Accept-Encoding": "gzip, deflate",
}


def get_df_setores(hdr=hdr):
    url = "https://www.fundamentus.com.br/buscaavancada.php"
    response = requests.get(url, headers=hdr)
    soup = BeautifulSoup(response.text, "html.parser")
    select = soup.find("select", {"name": "setor"})
    options = select.find_all("option")

    options_list = []
    for option in options:
        option_value = option.get("value")
        option_text = option.text
        if option_value and option_text:
            options_list.append(option_value + " - " + option_text)

    df = pd.DataFrame(options_list, columns=["Setor"])
    return df


def get_df_acoes_do_setor(id_setor):
    df = fd.list_papel_setor(id_setor)
    return df


def get_df_fiis(hdr=hdr):
    url = "https://www.fundamentus.com.br/fii_resultado.php"
    content = requests.get(url, headers=hdr)
    from io import StringIO

    df = pd.read_html(
        StringIO(str(content.text)),
        decimal=",",
        thousands=".",
        attrs={"id": "tabelaResultado"},
    )[0]

    df["Dividend Yield"] = perc_to_float(df["Dividend Yield"])
    df["FFO Yield"] = perc_to_float(df["FFO Yield"])
    df["Cap Rate"] = perc_to_float(df["Cap Rate"])
    df["Vacância Média"] = perc_to_float(df["Vacância Média"])

    return df


def get_df_acoes(hdr=hdr, formato_original=False):
    url = "https://www.fundamentus.com.br/resultado.php"
    content = requests.get(url, headers=hdr)

    from io import StringIO

    if formato_original:
        df = pd.read_html(
            StringIO(str(content.text)),
            decimal=",",
            thousands=".",
            attrs={"id": "resultado"},
        )[0]

    else:
        df = pd.read_html(
            StringIO(str(content.text)),
            decimal=",",
            thousands=".",
            attrs={"id": "resultado"},
            header=0,
        )[0]

    df["Div.Yield"] = perc_to_float(df["Div.Yield"])
    df["Mrg Ebit"] = perc_to_float(df["Mrg Ebit"])
    df["Mrg. Líq."] = perc_to_float(df["Mrg. Líq."])
    df["ROIC"] = perc_to_float(df["ROIC"])
    df["ROE"] = perc_to_float(df["ROE"])
    df["Cresc. Rec.5a"] = perc_to_float(df["Cresc. Rec.5a"])

    return df

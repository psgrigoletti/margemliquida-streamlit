from io import StringIO
from time import sleep

import pandas as pd
from selenium_config import meu_firefox


def buscar_dados_fundsexplorer():
    url = "https://www.fundsexplorer.com.br/ranking"
    wd = meu_firefox.configura_webdriver_firefox()
    wd.get(url)
    sleep(8)
    html_content = wd.page_source
    fiis_fundsexplorer = pd.read_html(StringIO(str(html_content)), encoding="utf-8")[0]
    fiis_fundsexplorer.rename(columns={"Fundos": "Código"}, inplace=True)
    return fiis_fundsexplorer

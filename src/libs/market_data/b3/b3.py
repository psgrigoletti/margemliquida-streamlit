import os
from time import sleep

import pandas as pd
from libs.market_data.selenium_config.meu_firefox import configura_webdriver_firefox
from selenium.webdriver.common.by import By


class CarteiraTeoricaB3:
    def __init__(self):
        pass

    @staticmethod
    def _buscar_carteira_teorica(indice, espera=6):
        url = f"https://sistemaswebb3-listados.b3.com.br/indexPage/day/{indice.upper()}?language=pt-br"

        wd = configura_webdriver_firefox()

        wd.get(url)
        wd.find_element(By.ID, "segment").send_keys("Setor de Atuação")
        sleep(espera)

        wd.find_element(By.LINK_TEXT, "Download").click()
        sleep(espera)

        path = "/tmp/downloads/"
        lista = os.listdir(path)
        lista = [path + arquivo for arquivo in lista]
        # print(lista)
        time_sorted_list = sorted(lista, key=os.path.getmtime)
        file_name = time_sorted_list[len(time_sorted_list) - 1]

        return pd.read_csv(
            file_name,
            sep=";",
            encoding="ISO-8859-1",
            skipfooter=2,
            engine="python",
            thousands=".",
            decimal=",",
            header=1,
            index_col=False,
        )

    @staticmethod
    def _corrigir_setores_ibov(setor):
        if (
            setor == "Cons N  Básico"
            or setor == "Cons N Cíclico"
            or setor == "Cons N Ciclico"
        ):
            return "Consumo Não-Cíclico"
        if setor == "Financ e Outros" or setor == "Financeiro e Outros":
            return "Financeiro"
        if setor == "Utilidade Públ":
            return "Utilidade Pública"
        if setor == "Diverso":
            return "Diversos"
        if setor == "Holdings Divers":
            return "Holdings Diversas"
        if setor == "Mats Básicos":
            return "Materiais Básicos"
        if setor == "Tec.Informação":
            return "Tecnologia da Informação"
        if setor == "Telecomunicaçã":
            return "Telecomunicação"
        if setor == "Bens Indls":
            return "Bens Industriais"
        else:
            return setor

    @staticmethod
    def buscar_dados_ifix():
        ifix = CarteiraTeoricaB3._buscar_carteira_teorica("IFIX")
        ifix.drop(columns=["Setor", "Tipo", "Part. (%)Acum."], inplace=True)
        return ifix

    @staticmethod
    def buscar_dados_ibov():
        ibov = CarteiraTeoricaB3._buscar_carteira_teorica("IBOV")
        ibov["Subsetor"] = ibov["Setor"].apply(lambda s: s[s.rfind("/") + 1 :].strip())
        ibov["Setor"] = ibov["Setor"].apply(lambda s: s[: s.rfind("/")].strip())
        ibov["Setor"] = ibov["Setor"].apply(CarteiraTeoricaB3._corrigir_setores_ibov)
        return ibov

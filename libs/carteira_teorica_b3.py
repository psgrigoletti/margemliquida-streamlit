from selenium.webdriver.common.by import By
from kora.selenium import wd
from time import sleep
import pandas as pd
import os


class CarteiraTeoricaB3:
    def __init__(self):
        pass
    
    def busca_carteira_teorica(self, indice, espera=8):
        url = f'https://sistemaswebb3-listados.b3.com.br/indexPage/day/{indice.upper()}?language=pt-br'
        wd.get(url)
        wd.find_element(By.ID, 'segment').send_keys("Setor de Atuação")
        sleep(espera)

        wd.find_element(By.LINK_TEXT, "Download").click()
        sleep(espera)

        caminho = os.getcwd()
        arquivos = os.listdir(caminho)
        arquivos = [f for f in arquivos if f[-3:] == 'csv' and indice.upper() in f]
        
        return pd.read_csv(arquivos[0], sep=';', encoding='ISO-8859-1', skipfooter=2, engine="python", thousands='.', decimal=',', header=1, index_col=False)
# import streamlit as st
# from time import sleep
# import pandas as pd
# import os

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By

# #@st.cache_resource
# def get_driver():
#     return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# options = Options()
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')

# driver = get_driver()

# url = f'https://sistemaswebb3-listados.b3.com.br/indexPage/day/{"IBOV".upper()}?language=pt-br'
# driver.get(url)
# driver.find_element(By.ID, 'segment').send_keys("Setor de Atuação")
# sleep(8)

# driver.find_element(By.LINK_TEXT, "Download").click()
# sleep(8)

# caminho = os.getcwd()
# arquivos = os.listdir(caminho)
# arquivos = [f for f in arquivos if f[-3:] == 'csv' and "IBOV".upper() in f]

# st.dataframe(pd.read_csv(arquivos[0], sep=';', encoding='ISO-8859-1', skipfooter=2,
#                          engine="python", thousands='.', decimal=',', header=1, index_col=False))

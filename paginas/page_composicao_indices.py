import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import os
import plotly.express as px
from io import StringIO


def configura_webdriver_firefox():
    # Configurar as opções do Firefox para o modo headless e definir a pasta de download
    firefox_options = Options()
    firefox_options.headless = True  # Modo headless

    # Configurar a pasta de download e permitir o download automático
    firefox_options.set_preference("browser.download.folderList", 2)
    firefox_options.set_preference(
        "browser.download.dir", "/tmp/downloads"
    )  # Substitua pelo caminho da sua pasta
    firefox_options.set_preference("browser.download.useDownloadDir", True)
    firefox_options.set_preference(
        "browser.download.viewableInternally.enabledTypes", ""
    )
    firefox_options.set_preference(
        "browser.helperApps.neverAsk.saveToDisk", "application/zip"
    )  # Substitua pelo tipo MIME do seu arquivo

    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--disable-gpu")

    # Criar uma instância do WebDriver do Firefox
    driver = webdriver.Firefox(options=firefox_options)
    return driver


def busca_carteira_teorica(indice, espera=6):
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


def corrigir_setores_ibov(setor):
    if setor == "Cons N  Básico" or setor == "Cons N Cíclico":
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


@st.cache_data(show_spinner="Carregando dados do IFIX", ttl=60 * 5)
def buscar_dados_ifix():
    ifix = busca_carteira_teorica("IFIX")
    ifix.drop(columns=["Setor", "Tipo", "Part. (%)Acum."], inplace=True)
    return ifix


@st.cache_data(show_spinner="Carregando dados do site fundsexplorer", ttl=60 * 5)
def buscar_dados_fundsexplorer():
    url = "https://www.fundsexplorer.com.br/ranking"
    wd = configura_webdriver_firefox()
    wd.get(url)
    sleep(8)
    html_content = wd.page_source
    fiis_fundsexplorer = pd.read_html(StringIO(str(html_content)), encoding="utf-8")[0]
    fiis_fundsexplorer.rename(columns={"Fundos": "Código"}, inplace=True)
    return fiis_fundsexplorer


@st.cache_data(show_spinner="Carregando dados do IBOV", ttl=60 * 5)
def buscar_dados_ibov():
    ibov = busca_carteira_teorica("IBOV")
    ibov["Subsetor"] = ibov["Setor"].apply(lambda s: s[s.rfind("/") + 1 :].strip())
    ibov["Setor"] = ibov["Setor"].apply(lambda s: s[: s.rfind("/")].strip())
    ibov["Setor"] = ibov["Setor"].apply(corrigir_setores_ibov)
    return ibov


def main():
    st.title(
        ":flashlight: Composição dos índices (IBOV e IFIX)",
    )
    st.write(
        "**Fonte**: https://b3.com.br e https://www.fundsexplorer.com.br/ via [selenium](https://pypi.org/project/selenium/)"
    )
    alertas = st.empty()

    if st.button("Carregar dados..."):
        with alertas:
            st.info(
                "O carregamento dos dados pode demorar um pouco... aguarde...",
                icon="⌛",
            )
        tab_ibov, tab_ifix = st.tabs(["IBOV", "IFIX"])
        with tab_ifix:
            st.title("IFIX")
            tab_ifix1, tab_ifix2, tab_ifix3, tab_ifix4, tab_ifix5 = st.tabs(
                [
                    ":memo: Dados B3",
                    ":memo: Dados fundsexplorer",
                    ":memo: Dados consolidados",
                    ":bar_chart: Gráfico sunburst",
                    ":bar_chart: Gráfico treemap",
                ]
            )

            ibov = buscar_dados_ibov()
            ifix = buscar_dados_ifix()
            funds = buscar_dados_fundsexplorer()
            ifix_final = pd.merge(ifix, funds, how="left", on="Código")
            ifix_final["Setor"] = ifix_final["Setor"].fillna("?")

            with tab_ifix1:
                st.write(ifix)

            with tab_ifix2:
                st.write(funds)

            with tab_ifix3:
                st.write(ifix_final)

            with tab_ifix4:
                fig1_ifix = px.sunburst(
                    data_frame=ifix_final,
                    path=["Setor", "Código"],
                    values="Part. (%)",
                    height=800,
                )
                fig1_ifix.update_traces(
                    textfont_color="black",
                    textfont_size=15,
                    # hovertemplate="<b>%{label}:</b> %{value:.2f}%",
                )
                st.write(fig1_ifix)

            with tab_ifix5:
                fig2_ifix = px.treemap(
                    data_frame=ifix_final,
                    path=["Setor", "Código"],
                    values="Part. (%)",
                    height=800,
                )
                fig2_ifix.update_traces(
                    textfont_color="black",
                    textfont_size=15,
                    # hovertemplate="<b>%{label}:</b> %{value:.2f}%",
                )
                st.write(fig2_ifix)

        with tab_ibov:
            st.title("IBOV")
            tab_ibov1, tab_ibov2, tab_ibov3 = st.tabs(
                [
                    ":memo: Dados B3",
                    ":bar_chart: Gráfico sunburst",
                    ":bar_chart: Gráfico treemap",
                ]
            )

            with tab_ibov1:
                st.write(ibov)

            with tab_ibov2:
                fig1_ibov = px.sunburst(
                    data_frame=ibov,
                    path=["Setor", "Subsetor", "Código"],
                    values="Part. (%)",
                    height=800,
                )
                fig1_ibov.update_traces(
                    textfont_color="black",
                    textfont_size=15,
                    # hovertemplate="<b>%{label}:</b> %{value:.2f}%",
                )
                st.write(fig1_ibov)

            with tab_ibov3:
                fig2_ibov = px.treemap(
                    data_frame=ibov,
                    path=["Setor", "Subsetor", "Código"],
                    values="Part. (%)",
                    height=800,
                )
                fig2_ibov.update_traces(
                    textfont_color="black",
                    textfont_size=15,
                    # hovertemplate="<b>%{label}:</b> %{value:.2f}%",
                )
                st.write(fig2_ibov)
        with alertas:
            st.empty()
            st.success("Dados carregados com sucesso...")

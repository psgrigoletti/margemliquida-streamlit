from typing import List
import streamlit as st
import zipfile
import io
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime, timedelta


def mes_ano_no_passado(mes, ano):
    # Obtém o mês e o ano atuais
    data_atual = datetime.now()
    ano_atual = data_atual.year
    mes_atual = data_atual.month

    # Compara o ano e o mês fornecidos com o ano e o mês atuais
    if int(ano) < ano_atual or (int(ano) == ano_atual and int(mes) < mes_atual):
        return True
    else:
        return False


def data_anterior(data):
    # Converte a string de data para um objeto datetime
    data_obj = datetime.strptime(data, "%Y-%m-%d")

    # Calcula a data anterior subtraindo um dia
    data_anterior = data_obj - timedelta(days=1)

    # Formata a data anterior de volta para o formato 'YYYY-MM-DD'
    data_anterior_formatada = data_anterior.strftime("%Y-%m-%d")

    return data_anterior_formatada


@st.cache_data(ttl=3600, show_spinner="Carregando fundos com as maiores baixas...")
def carregar_fundos_maiores_baixas(mes, ano, maior_data_dos_dados, quantidade):
    cotas_normalizadas = carregar_cotas_normalizadas(mes, ano)
    baixas = (
        cotas_normalizadas.sort_values(maior_data_dos_dados, ascending=True)[
            : int(quantidade)
        ][maior_data_dos_dados]
        - 1
    ) * 100
    # st.write(baixas)
    fundo_df_baixa = pd.DataFrame(
        columns=["Retornos", "Nome do Fundo", "Classe", "Patrimônio Líquido"]
    )
    for cnpj in baixas.index:
        fundo = carregar_dados_cadastrais_de([cnpj])
        if esta_nos_dados_cadastrais(cnpj):
            fundo_df_baixa.loc[cnpj] = [
                baixas[baixas.index == cnpj].values[0],
                fundo["DENOM_SOCIAL"].values[0],
                fundo["CLASSE"].values[0],
                fundo["VL_PATRIM_LIQ"].values[0],
            ]
        else:
            fundo_df_baixa.loc[cnpj] = [
                baixas[baixas.index == cnpj].values[0],
                "NAO ENCONTRADO",
                "NAO ENCONTRADO",
                0,
            ]
    return fundo_df_baixa


@st.cache_data(ttl=3600, show_spinner="Carregando fundos com as maiores altas...")
def carregar_fundos_maiores_altas(mes, ano, maior_data_dos_dados, quantidade):
    cotas_normalizadas = carregar_cotas_normalizadas(mes, ano)
    altas = (
        cotas_normalizadas.sort_values(maior_data_dos_dados, ascending=False)[
            : int(quantidade)
        ][maior_data_dos_dados]
        - 1
    ) * 100
    # st.write(altas)
    fundo_df_alta = pd.DataFrame(
        columns=["Retornos", "Nome do Fundo", "Classe", "Patrimônio Líquido"]
    )
    # st.write(fundo_df_alta)
    for cnpj in altas.index:
        fundo = carregar_dados_cadastrais_de([cnpj])
        # st.write(fundo)
        # print("LISTA DE FUNDOS ALTA")
        # print("Vai pesquisar: " + cnpj)
        # print("Quantidade registros retornados: " + str(len(fundo)))
        # print(fundo)

        if esta_nos_dados_cadastrais(cnpj):
            fundo_df_alta.loc[cnpj] = [
                altas[altas.index == cnpj].values[0],
                fundo["DENOM_SOCIAL"].values[0],
                fundo["CLASSE"].values[0],
                fundo["VL_PATRIM_LIQ"].values[0],
            ]
        else:
            fundo_df_alta.loc[cnpj] = [
                altas[altas.index == cnpj].values[0],
                "NAO ENCONTRADO",
                "NAO ENCONTRADO",
                0,
            ]
    return fundo_df_alta


@st.cache_data(ttl=3600, show_spinner="Carregando dados cadastrais da CVM...")
def carregar_todos_dados_cadastrais():
    url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
    cadastral = pd.read_csv(
        url,
        sep=";",
        encoding="ISO-8859-1",
        dtype={
            14: str,
            17: str,
            18: str,
            20: str,
            22: str,
            24: str,
            27: str,
            37: str,
            38: str,
            39: str,
            40: str,
        },
    )
    cadastral = cadastral[~cadastral["SIT"].str.contains("CANCELADA")]
    cadastral = cadastral[~cadastral["DENOM_SOCIAL"].str.contains("NAO ENCONTRADO")]
    # print(
    #     "Retornando informações cadastrais de "
    #     + str(len(cadastral))
    #     + " fundos (não cancelados)"
    # )
    return cadastral


@st.cache_data(ttl=3600, show_spinner="Carregando dados cadastrais dos gestores...")
def carregar_lista_de_gestores():
    cadastral = carregar_todos_dados_cadastrais()
    cadastral.sort_values(by=["GESTOR"], inplace=True)
    cadastral = cadastral[cadastral["GESTOR"].notna()]
    gestores = cadastral["GESTOR"].unique()
    return gestores


@st.cache_data(ttl=3600, show_spinner="Carregando dados cadastrais das classes...")
def carregar_lista_de_classes():
    cadastral = carregar_todos_dados_cadastrais()
    cadastral.sort_values(by=["CLASSE"], inplace=True)
    cadastral = cadastral[cadastral["CLASSE"].notna()]
    classes = cadastral["CLASSE"].unique()
    return classes


# @st.cache_data(
#     ttl=3600, show_spinner="Carregando dados cadastrais de um ou mais CNPJs..."
# )


def esta_nos_dados_cadastrais(cnpj):
    cadastral = carregar_todos_dados_cadastrais()
    filtrado = cadastral[cadastral["CNPJ_FUNDO"] == cnpj]
    return len(filtrado) > 0


def carregar_dados_cadastrais_de(cnpjs):
    cadastral = carregar_todos_dados_cadastrais()
    filtrado = cadastral[cadastral["CNPJ_FUNDO"].isin(cnpjs)]
    return filtrado


@st.cache_data(ttl=3600, show_spinner="Carregando informes diários da CVM...")
def carregar_dados_informes_diarios(mes, ano):
    # try:
    arquivo = f"inf_diario_fi_{ano}{mes}.csv"
    link = f"https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{ano}{mes}.zip"
    r = requests.get(link)
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    arquivo_fi = zf.open(arquivo)
    linhas = arquivo_fi.readlines()
    linhas = [i.strip().decode("ISO-8859-1") for i in linhas]
    linhas = [i.split(";") for i in linhas]
    df = pd.DataFrame(linhas, columns=linhas[0])
    informes_diarios = df[1:].reset_index()
    informes_diarios[
        [
            "VL_TOTAL",
            "VL_QUOTA",
            "VL_PATRIM_LIQ",
            "CAPTC_DIA",
            "RESG_DIA",
            "NR_COTST",
        ]
    ] = informes_diarios[
        [
            "VL_TOTAL",
            "VL_QUOTA",
            "VL_PATRIM_LIQ",
            "CAPTC_DIA",
            "RESG_DIA",
            "NR_COTST",
        ]
    ].apply(
        pd.to_numeric
    )

    return informes_diarios
    # except:
    #     mensagens = st.container()
    #     mensagens.error("Erro ao baixar dados de https://dados.cvm.gov.br/", icon="🚨")
    #     st.stop()


@st.cache_data(ttl=3600, show_spinner="Carregando cotas normalizadas...")
def carregar_cotas_normalizadas(mes, ano):
    informes_diarios = carregar_dados_informes_diarios(mes, ano)
    filtro = informes_diarios[informes_diarios["NR_COTST"] > 1000]
    fundos = filtro.pivot(
        index="DT_COMPTC",
        columns="CNPJ_FUNDO",
        values=["VL_TOTAL", "VL_QUOTA", "VL_PATRIM_LIQ"],
    )
    normalizados = fundos["VL_QUOTA"] / fundos["VL_QUOTA"].iloc[0]
    cotas_normalizadas = pd.DataFrame(normalizados.iloc[-1])
    return cotas_normalizadas


def main():
    st.title(":flag-br: Fundos Brasileiros")
    st.write("**Fonte**: _http://dados.cvm.gov.br_")
    alertas = st.container()

    col1, col2, col3, col4 = st.columns([1, 1, 1, 4])
    with col1:
        mes = st.text_input("Mês (formato MM)", "12")
    with col2:
        ano = st.text_input("Ano (formado YYYY)", "2023")
    with col3:
        quantidade = st.text_input("Quantidade", "10")
    # with col4:
    #     gestor = st.selectbox(
    #         "Gestor", carregar_lista_de_gestores(), placeholder="Selecione"
    #     )
    #     classe = st.selectbox(
    #         "Classe",
    #         [" "] + carregar_lista_de_classes(),
    #         placeholder="Selecione",
    #     )

    if st.button("Carregar dados..."):
        if not mes_ano_no_passado(mes, ano):
            with alertas:
                st.error("Informe um mês ano que já tenha encerrado", icon="🚨")
            st.stop()

        try:
            informes_diarios = carregar_dados_informes_diarios(mes, ano)
        except:
            with alertas:
                frase = "Erro ao buscar dados de http://dados.cvm.gov.br. Tente mais tarde..."
                st.error(frase, icon="🚨")
            st.stop()

        maior_data_dos_dados = informes_diarios["DT_COMPTC"].max()
        # maior_data_dos_dados = data_anterior(maior_data_dos_dados)

        st.write(f"Considerados dados até {maior_data_dos_dados}")
        tab1, tab2, tab3 = st.tabs(["Maior PL", "Mais subiram", "Mais caíram"])

        with tab1:
            st.write(
                f"### :statue_of_liberty: {quantidade} maiores fundos (considerando PL) no período selecionado ({mes}/{ano})"
            )
            comparativo = informes_diarios[
                informes_diarios["DT_COMPTC"] == maior_data_dos_dados
            ].copy()
            comparativo.sort_values("VL_PATRIM_LIQ", inplace=True)
            cnpjs = comparativo.CNPJ_FUNDO.iloc[-int(quantidade) :]
            # fundos = informes_diarios[informes_diarios["CNPJ_FUNDO"].isin(cnpjs)]
            # variacao = fundo.VL_QUOTA.plot().figure
            # print(cnpjs.values)
            retorno = carregar_dados_cadastrais_de(cnpjs.values)
            retorno.sort_values("VL_PATRIM_LIQ", inplace=True, ascending=False)
            retorno = retorno.head(int(quantidade))
            st.write(
                retorno[
                    [
                        "VL_PATRIM_LIQ",
                        "TP_FUNDO",
                        "CNPJ_FUNDO",
                        "DENOM_SOCIAL",
                        "SIT",
                        "CLASSE",
                        "FUNDO_EXCLUSIVO",
                        "PUBLICO_ALVO",
                        "DIRETOR",
                        "GESTOR",
                        "AUDITOR",
                        "CUSTODIANTE",
                        "CLASSE_ANBIMA",
                    ]
                ]
            )
            # st.pyplot(variacao)
        with tab2:
            st.write(
                f"### :heavy_dollar_sign: {quantidade} fundos que mais subiram no período selecionado ({mes}/{ano})"
            )

            fundo_df_alta = carregar_fundos_maiores_altas(
                mes, ano, maior_data_dos_dados, quantidade
            )
            fig1 = plt.figure(figsize=(10, 4))
            sns.barplot(
                data=fundo_df_alta, x=fundo_df_alta.index, y=fundo_df_alta["Retornos"]
            )
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=80)
            plt.xlabel("CNPJ")

            st.write(fundo_df_alta)
            st.pyplot(fig1)

        with tab3:
            st.write(
                f"### :poop: {quantidade} fundos que mais caíram no período selecionado ({mes}/{ano})"
            )
            fundo_df_baixa = carregar_fundos_maiores_baixas(
                mes, ano, maior_data_dos_dados, quantidade
            )

            fig2 = plt.figure(figsize=(10, 4))
            sns.barplot(
                data=fundo_df_baixa,
                x=fundo_df_baixa.index,
                y=fundo_df_baixa["Retornos"],
            ).figure
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=80)
            plt.xlabel("CNPJ")

            st.write(fundo_df_baixa)
            st.pyplot(fig2)

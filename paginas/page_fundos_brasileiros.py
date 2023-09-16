import streamlit as st
import zipfile
import io
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def carregar_dados_cadastrais():
    url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
    cadastral = pd.read_csv(url, sep=";", encoding="ISO-8859-1")
    return cadastral


@st.cache_data
def carregar_dados_cadastrais_de(_cnpjs: list):
    cadastral = carregar_dados_cadastrais()
    cadastral = cadastral[~cadastral["SIT"].str.contains("CANCELADA")]
    return cadastral[cadastral["CNPJ_FUNDO"].isin(_cnpjs)]


@st.cache_data
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


@st.cache_data
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
    mensagens = st.container()

    col1, col2, col3, _ = st.columns([1, 1, 1, 4])
    with col1:
        mes = st.text_input("Mês (formato MM)", "08")
    with col2:
        ano = st.text_input("Ano (formado YYYY)", "2023")
    with col3:
        quantidade = st.text_input("Quantidade", "10")

    if st.button("Carregar dados..."):
        tab1, tab2, tab3 = st.tabs(["Maior PL", "Mais subiram", "Mais caíram"])
        informes_diarios = carregar_dados_informes_diarios(mes, ano)

        with tab1:
            st.write(
                f"### :statue_of_liberty: {quantidade} maiores fundos (considerando PL) no período selecionado ({mes}/{ano})"
            )
            comparativo = informes_diarios[
                informes_diarios["DT_COMPTC"] == f"{ano}-{mes}-31"
            ]
            comparativo.sort_values("VL_PATRIM_LIQ", inplace=True)
            cnpjs = comparativo.CNPJ_FUNDO.iloc[-int(quantidade) :]
            # fundos = informes_diarios[informes_diarios["CNPJ_FUNDO"].isin(cnpjs)]
            # variacao = fundo.VL_QUOTA.plot().figure
            # print(cnpjs.values)
            retorno = carregar_dados_cadastrais_de(cnpjs.values)
            retorno.sort_values("VL_PATRIM_LIQ", inplace=True, ascending=False)
            retorno = retorno.head(int(quantidade))
            st.write(retorno)
            # st.pyplot(variacao)
        with tab2:
            st.write(
                f"### :heavy_dollar_sign: {quantidade} fundos que mais subiram no período selecionado ({mes}/{ano})"
            )
            cotas_normalizadas = carregar_cotas_normalizadas(mes, ano)
            altas = (
                cotas_normalizadas.sort_values(f"{ano}-{mes}-31", ascending=False)[
                    : int(quantidade)
                ][f"{ano}-{mes}-31"]
                - 1
            ) * 100
            fundo_df_alta = pd.DataFrame(
                columns=["Retornos", "Nome do Fundo", "Classe", "Patrimônio Líquido"]
            )
            for cnpj in altas.index:
                fundo = carregar_dados_cadastrais_de([cnpj])
                fundo_df_alta.loc[cnpj] = [
                    altas[altas.index == cnpj].values[0],
                    fundo["DENOM_SOCIAL"].values[0],
                    fundo["CLASSE"].values[0],
                    fundo["VL_PATRIM_LIQ"].values[0],
                ]
            fig1 = plt.figure(figsize=(10, 4))
            sns.barplot(
                data=fundo_df_alta, x=fundo_df_alta.index, y=fundo_df_alta["Retornos"]
            )
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=80)
            st.write(fundo_df_alta)
            st.pyplot(fig1)

        with tab3:
            st.write(
                f"### :poop: {quantidade} fundos que mais caíram no período selecionado ({mes}/{ano})"
            )
            cotas_normalizadas = carregar_cotas_normalizadas(mes, ano)
            baixas = (
                cotas_normalizadas.sort_values(f"{ano}-{mes}-31", ascending=True)[
                    : int(quantidade)
                ][f"{ano}-{mes}-31"]
                - 1
            ) * 100
            fundo_df_baixa = pd.DataFrame(
                columns=["Retornos", "Nome do Fundo", "Classe", "Patrimônio Líquido"]
            )
            for cnpj in baixas.index:
                fundo = carregar_dados_cadastrais_de([cnpj])
                fundo_df_baixa.loc[cnpj] = [
                    baixas[baixas.index == cnpj].values[0],
                    fundo["DENOM_SOCIAL"].values[0],
                    fundo["CLASSE"].values[0],
                    fundo["VL_PATRIM_LIQ"].values[0],
                ]
            fig2 = plt.figure(figsize=(10, 4))
            sns.barplot(
                data=fundo_df_baixa,
                x=fundo_df_baixa.index,
                y=fundo_df_baixa["Retornos"],
            ).figure
            locs, labels = plt.xticks()
            plt.setp(labels, rotation=80)
            st.write(fundo_df_baixa)
            st.pyplot(fig2)

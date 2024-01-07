import io

# import locale
import logging
import os
import time
import zipfile

import pandas as pd
import requests
import xlsxwriter


class DadosCVM:
    URL_DADOS_CIAS = (
        "http://dados.cvm.gov.br/dados/CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv"
    )
    df_dados_empresas = None
    df_dados_empresas_disponiveis = None
    demonstrativos_interesse = ["BPA", "DRE", "BPP"]

    def __init__(self):
        logging.log(logging.INFO, "Inicializando objeto da classe DadosCVM")
        # locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    def buscar_empresas(self):
        logging.log(
            logging.INFO, "Buscando dados das empresas do site http://dados.cvm.gov.br/"
        )

        self.df_dados_empresas = pd.read_csv(
            self.URL_DADOS_CIAS, sep=";", encoding="ISO-8859-1"
        )

        situacao_interesse = "ATIVO"
        tipo_mercado_interesse = "BOLSA"

        logging.log(logging.INFO, "Filtrando apenas por empresas ATIVAS e na BOLSA")
        self.df_dados_empresas_disponiveis = self.df_dados_empresas[
            (self.df_dados_empresas["SIT"] == situacao_interesse)
            & (self.df_dados_empresas["TP_MERC"] == tipo_mercado_interesse)
        ]

    def __retorna_ponteiro_arquivo_zip(self, url):
        try:
            req = requests.get(url)
            arquivo_zip = zipfile.ZipFile(io.BytesIO(req.content))
            print("Sucesso ao baixar o arquivo de " + url, icon="✅")
        except:
            print("Erro ao buscar o arquivo de " + url)
            arquivo_zip = None
        return arquivo_zip

    def __atualiza_dict_df_demonstrativo(
        self, tipo, arquivo_zip, demonstrativo, ano, codigos_cvm, dict_df
    ):
        if not arquivo_zip is None:
            nome_arquivo_csv = (
                tipo + "_cia_aberta_" + str(demonstrativo) + "_con_" + str(ano) + ".csv"
            )  # CONSIDERANDO SOMENTE OS DF CONSOLIDADOS
            arquivo_csv = arquivo_zip.open(nome_arquivo_csv)
            linhas = arquivo_csv.readlines()
            linhas = [i.strip().decode("ISO-8859-1") for i in linhas]
            linhas = [i.split(";") for i in linhas]
            df = pd.DataFrame(linhas[1:], columns=linhas[0])
            df["VL_AJUSTADO"] = pd.to_numeric(df["VL_CONTA"])
            df = df[df["ORDEM_EXERC"] == "ÚLTIMO"]

            for codigo_cvm in codigos_cvm:
                if not codigo_cvm + "|" + demonstrativo in dict_df:
                    dict_df[codigo_cvm + "|" + demonstrativo] = df[
                        df["CD_CVM"] == str(codigo_cvm)
                    ]
                else:
                    dict_df[codigo_cvm + "|" + demonstrativo] = pd.concat(
                        [
                            dict_df[codigo_cvm + "|" + demonstrativo],
                            df[df["CD_CVM"] == str(codigo_cvm)],
                        ]
                    )

    def __processa_arquivos_do_ano(self, ano):
        if not len(self.codigos_cvm) > 0:
            logging(logging.ERROR, "Lista de empresas selecionadas vazia...")
            return
        else:
            url_itr = (
                "http://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_"
                + str(ano)
                + ".zip"
            )
            url_dfp = (
                "https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_"
                + str(ano)
                + ".zip"
            )

            arquivo_zip_itr = self.__retorna_ponteiro_arquivo_zip(url_itr)
            arquivo_zip_dfp = self.__retorna_ponteiro_arquivo_zip(url_dfp)

            dict_df = {}

            for demonstrativo in self.demonstrativos_interesse:
                self.__atualiza_dict_df_demonstrativo(
                    "itr",
                    arquivo_zip_itr,
                    demonstrativo,
                    ano,
                    self.codigos_cvm,
                    dict_df,
                )
                self.__atualiza_dict_df_demonstrativo(
                    "dfp",
                    arquivo_zip_dfp,
                    demonstrativo,
                    ano,
                    self.codigos_cvm,
                    dict_df,
                )
                print(
                    f"Dados (de todas as empresas de interesse) do demonstrativo {demonstrativo} para o ano {ano} foram armazenados."
                )

            for i in range(0, len(self.codigos_cvm)):
                codigo_cvm = self.codigos_cvm[i]
                writer = pd.ExcelWriter(
                    f"demonstrativos_empresa_{str(codigo_cvm)}_ano_{ano}.xlsx",
                    engine="xlsxwriter",
                )

                for demonstrativo in self.demonstrativos_interesse:
                    dict_df[codigo_cvm + "|" + demonstrativo].to_excel(
                        writer, sheet_name=demonstrativo, encoding="ISO-8859-1"
                    )

                writer.close()
                print(
                    f"Arquivo Excel com os demonstrativos da empresa {codigo_cvm} para o ano {ano} já exportado."
                )

    def __adicionar_dados_4_trimestre(self, dre):
        dre_infos_12_meses = dre[
            (dre["DT_INI_EXERC"].str[4:8] == "-01-")
            & (dre["DT_FIM_EXERC"].str[4:8] == "-12-")
        ]
        dre_infos_9_meses = dre[
            (dre["DT_INI_EXERC"].str[4:8] == "-01-")
            & (dre["DT_FIM_EXERC"].str[4:8] == "-09-")
        ]

        for row in dre_infos_12_meses.iterrows():
            # codigo_cvm = row['CD_CVM']
            ordem = row["ORDEM_EXERC"]
            codigo_conta = row["CD_CONTA"]
            descricao_conta = row["DS_CONTA"]
            valor_ajustado_12_meses = row["VL_AJUSTADO"]
            nova_data_inicio = row["DT_INI_EXERC"][0:4] + "-10-01"

            try:
                valor_ajustado_9_meses = dre_infos_9_meses[
                    (dre_infos_9_meses["CD_CONTA"] == codigo_conta)
                    & (dre_infos_9_meses["ORDEM_EXERC"] == ordem)
                ].iloc[0]["VL_AJUSTADO"]
                # print(f"Achou valor para a conta {codigo_conta} {descricao_conta}")
                # print(f"Valor para os 9 meses: {valor_ajustado_9_meses}")
                # print(f"Valor para os 12 meses: {valor_ajustado_12_meses}")
                # print(f"Vai setar a nova data inicial para: {nova_data_inicio}\n\n")
                row_temp = row.copy()
                row_temp["VL_AJUSTADO"] = (
                    valor_ajustado_12_meses - valor_ajustado_9_meses
                )
                row_temp["DT_INI_EXERC"] = nova_data_inicio
                dre = pd.concat([dre, row_temp])
            except:
                print(
                    f"Não encontrou valor para a conta {codigo_conta} - '{descricao_conta}' para os 9 meses. Encontrou para os 12."
                )

        return dre

    def buscar_demonstrativos(
        self,
        codigos_cvm,
        empresas_selecionadas,
        anos_selecionados,
        periodos_selecionados,
    ):
        start_time = time.time()
        self.codigos_cvm = codigos_cvm
        self.periodos_selecionados = periodos_selecionados
        self.anos_selecionados = anos_selecionados
        self.empresas_selecionadas = empresas_selecionadas

        # with Pool() as pool:
        #    pool.map(self.processa_arquivos_do_ano, anos_selecionados)

        for ano in anos_selecionados:
            self.__processa_arquivos_do_ano(ano)

        print("O tempo de execução foi de %s segundos" % (time.time() - start_time))

        caminho = os.getcwd()
        arquivos = os.listdir(caminho)
        self.arquivos_xlsx = [f for f in arquivos if f[-4:] == "xlsx"]

    def gerar_dre_completo(self):
        # Criar o dataframe DRE
        dre_completo = pd.DataFrame()

        # Juntar todos os arquivos xlsx em uma grande tabela DRE
        for arquivo_xlsx in self.arquivos_xlsx:
            dre = pd.read_excel(arquivo_xlsx, sheet_name="DRE")
            dre = self.__adicionar_dados_4_trimestre(dre)
            dre_completo = pd.concat([dre_completo, dre])

        self.dre_completo = pd.pivot_table(
            dre_completo,
            index=["DENOM_CIA", "DS_CONTA"],
            columns=["DT_INI_EXERC", "DT_FIM_EXERC"],
            values=["VL_AJUSTADO"],
        )

    def retonar_dre_completo(self):
        return self.dre_completo

    def retonar_empresas(self):
        return self.df_dados_empresas_disponiveis

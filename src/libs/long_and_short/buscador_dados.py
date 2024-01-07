# import random
# import yfinance as yf
# import pandas as pd
# import pprint
# from datetime import datetime, timedelta

# FORMATO_DATA = "%Y-%m-%d"
# ADJ_CLOSE = "Adj Close"
# PERIODO = "PERIODO"


# class BuscadorDados:
#     def __init__(
#         self, prioridade_nos_dados=PERIODO, dados_fechamento=ADJ_CLOSE
#     ) -> None:
#         print(">> Iniciando BuscadorDados")

#         self.dados_fechamento = dados_fechamento
#         self.prioridade_nos_dados = prioridade_nos_dados

#         self.pp = pprint.PrettyPrinter(width=200, compact=True)  # indent=4,
#         self.data_inicial = None
#         self.data_final = None
#         self.quantidade_ativos = None
#         self.df = None
#         self.df_yahoo = None

#         self.lista_ativos = None
#         self.lista_ativos_completa = None

#         self.__inicializa_lista_ativos_completa()

#     def busca_ativos_aleatoriamente(
#         self,
#         data_inicial,
#         data_final,
#         quantidade_ativos="10",
#         prioridade_nos_dados=PERIODO,
#         dados_fechamento=ADJ_CLOSE,
#     ):
#         print("Buscando ativos aleatoriamente")

#         self.data_inicial = datetime.strptime(data_inicial, FORMATO_DATA) - timedelta(
#             days=1
#         )
#         self.data_final = datetime.strptime(data_final, FORMATO_DATA) + timedelta(
#             days=1
#         )
#         self.quantidade_ativos = quantidade_ativos
#         self.prioridade_nos_dados = prioridade_nos_dados
#         self.dados_fechamento = dados_fechamento
#         self.lista_ativos = None
#         self.__valida_paramentros()

#     def busca_ativos_especificos(
#         self,
#         data_inicial,
#         data_final,
#         lista_ativos,
#         prioridade_nos_dados=PERIODO,
#         dados_fechamento=ADJ_CLOSE,
#     ):
#         print("Buscando ativos específicos")

#         self.data_inicial = datetime.strptime(data_inicial, FORMATO_DATA) - timedelta(
#             days=1
#         )
#         self.data_final = datetime.strptime(data_final, FORMATO_DATA) + timedelta(
#             days=1
#         )
#         self.prioridade_nos_dados = prioridade_nos_dados
#         self.dados_fechamento = dados_fechamento
#         self.lista_ativos = lista_ativos
#         self.quantidade_ativos = len(lista_ativos)

#     def __valida_paramentros(self):
#         if self.quantidade_ativos not in [
#             "1",
#             "2",
#             "3",
#             "4",
#             "5",
#             "10",
#             "25",
#             "50",
#             "100",
#             "TODOS",
#         ]:
#             raise ValueError('Quantidade de ativos deve ser [10, 25, 50, 100, "TODOS"]')

#         if self.prioridade_nos_dados not in ["PERIODO", "ATIVOS"]:
#             raise ValueError('Prioridade nos dados deve ser ["PERIODO", "ATIVOS"]')

#         if self.dados_fechamento not in ["Close", "Adj Close"]:
#             raise ValueError('Dados de fechamento deve ser ["Close", "Adj Close"]')

#         # TODO: Implementar mais validações

#         print("Parâmetros válidos...")

#     def __inicializa_lista_ativos_completa(self):
#         # TODO: Programar para pegar do site

#         self.ibrx = [
#             "WEGE3.SA",
#             "AZUL4.SA",
#             "RAIL3.SA",
#             "BRFS3.SA",
#             "JBSS3.SA",
#             "MRFG3.SA",
#             "ABEV3.SA",
#             "ASAI3.SA",
#             "NTCO3.SA",
#             "LREN3.SA",
#             "MGLU3.SA",
#             "PETZ3.SA",
#             "VIIA3.SA",
#             "CYRE3.SA",
#             "CVCB3.SA",
#             "RENT3.SA",
#             "ALSO3.SA",
#             "MULT3.SA",
#             "BBDC4.SA",
#             "BBAS3.SA",
#             "BPAC11.SA",
#             "ITSA4.SA",
#             "ITUB4.SA",
#             "BBSE3.SA",
#             "B3SA3.SA",
#             "CIEL3.SA",
#             "KLBN11.SA",
#             "SUZB3.SA",
#             "VALE3.SA",
#             "GGBR4.SA",
#             "CSNA3.SA",
#             "USIM5.SA",
#             "RRRP3.SA",
#             "CSAN3.SA",
#             "PETR3.SA",
#             "PETR4.SA",
#             "PRIO3.SA",
#             "VBBR3.SA",
#             "HYPE3.SA",
#             "RADL3.SA",
#             "HAPV3.SA",
#             "RDOR3.SA",
#             "LWSA3.SA",
#             "TOTS3.SA",
#             "SBSP3.SA",
#             "CMIG4.SA",
#             "ELET3.SA",
#             "ELET6.SA",
#             "EQTL3.SA",
#         ]

#         self.ibov = [
#             "WEGE3.SA",
#             "EMBR3.SA",
#             "AZUL4.SA",
#             "CCRO3.SA",
#             "ECOR3.SA",
#             "GOLL4.SA",
#             "RAIL3.SA",
#             "BRFS3.SA",
#             "JBSS3.SA",
#             "MRFG3.SA",
#             "BEEF3.SA",
#             "SMTO3.SA",
#             "ABEV3.SA",
#             "ASAI3.SA",
#             "CRFB3.SA",
#             "PCAR3.SA",
#             "NTCO3.SA",
#             "RAIZ4.SA",
#             "SLCE3.SA",
#             "ARZZ3.SA",
#             "SOMA3.SA",
#             "LREN3.SA",
#             "MGLU3.SA",
#             "PETZ3.SA",
#             "VIIA3.SA",
#             "ALPA4.SA",
#             "CYRE3.SA",
#             "EZTC3.SA",
#             "MRVE3.SA",
#             "CVCB3.SA",
#             "COGN3.SA",
#             "RENT3.SA",
#             "YDUQ3.SA",
#             "ALSO3.SA",
#             "IGTI11.SA",
#             "MULT3.SA",
#             "BPAN4.SA",
#             "BBDC3.SA",
#             "BBDC4.SA",
#             "BBAS3.SA",
#             "BPAC11.SA",
#             "ITSA4.SA",
#             "ITUB4.SA",
#             "SANB11.SA",
#             "BBSE3.SA",
#             "B3SA3.SA",
#             "CIEL3.SA",
#             "DXCO3.SA",
#             "KLBN11.SA",
#             "SUZB3.SA",
#             "BRAP4.SA",
#             "CMIN3.SA",
#             "VALE3.SA",
#             "BRKM5.SA",
#             "GGBR4.SA",
#             "GOAU4.SA",
#             "CSNA3.SA",
#             "USIM5.SA",
#             "RRRP3.SA",
#             "CSAN3.SA",
#             "PETR3.SA",
#             "PETR4.SA",
#             "PRIO3.SA",
#             "UGPA3.SA",
#             "VBBR3.SA",
#             "HYPE3.SA",
#             "RADL3.SA",
#             "FLRY3.SA",
#             "HAPV3.SA",
#             "QUAL3.SA",
#             "RDOR3.SA",
#             "LWSA3.SA",
#             "CASH3.SA",
#             "TOTS3.SA",
#             "VIVT3.SA",
#             "TIMS3.SA",
#             "SBSP3.SA",
#             "CMIG4.SA",
#             "CPLE6.SA",
#             "CPFE3.SA",
#             "ELET3.SA",
#             "ELET6.SA",
#             "ENBR3.SA",
#             "ENGI11.SA",
#             "ENEV3.SA",
#             "EGIE3.SA",
#             "EQTL3.SA",
#             "TAEE11.SA",
#         ]

#         self.smll = [
#             "AERI3.SA",
#             "ARML3.SA",
#             "KEPL3.SA",
#             "MILS3.SA",
#             "ROMI3.SA",
#             "TASA4.SA",
#             "EMBR3.SA",
#             "POMO4.SA",
#             "RAPT4.SA",
#             "RCSL3.SA",
#             "TUPY3.SA",
#             "GGPS3.SA",
#             "SEQL3.SA",
#             "VLID3.SA",
#             "AZUL4.SA",
#             "ECOR3.SA",
#             "GOLL4.SA",
#             "HBSA3.SA",
#             "LOGN3.SA",
#             "STBP3.SA",
#             "PTBL3.SA",
#             "INTB3.SA",
#             "MLAS3.SA",
#             "POSI3.SA",
#             "BRFS3.SA",
#             "CAML3.SA",
#             "JALL3.SA",
#             "MDIA3.SA",
#             "MRFG3.SA",
#             "BEEF3.SA",
#             "SMTO3.SA",
#             "GMAT3.SA",
#             "PCAR3.SA",
#             "TTEN3.SA",
#             "AGRO3.SA",
#             "SLCE3.SA",
#             "ARZZ3.SA",
#             "CEAB3.SA",
#             "ESPA3.SA",
#             "SBFG3.SA",
#             "SOMA3.SA",
#             "GUAR3.SA",
#             "AMAR3.SA",
#             "PETZ3.SA",
#             "LJQQ3.SA",
#             "VIIA3.SA",
#             "ALPA4.SA",
#             "GRND3.SA",
#             "VIVA3.SA",
#             "VULC3.SA",
#             "MYPK3.SA",
#             "LEVE3.SA",
#             "CURY3.SA",
#             "CYRE3.SA",
#             "DIRR3.SA",
#             "EVEN3.SA",
#             "EZTC3.SA",
#             "GFSA3.SA",
#             "JHSF3.SA",
#             "LAVV3.SA",
#             "MRVE3.SA",
#             "TEND3.SA",
#             "TRIS3.SA",
#             "MEAL3.SA",
#             "ZAMP3.SA",
#             "CVCB3.SA",
#             "SMFT3.SA",
#             "ANIM3.SA",
#             "COGN3.SA",
#             "MOVI3.SA",
#             "SEER3.SA",
#             "YDUQ3.SA",
#             "ALSO3.SA",
#             "BRPR3.SA",
#             "IGTI11.SA",
#             "LOGG3.SA",
#             "SYNE3.SA",
#             "SIMH3.SA",
#             "ABCB4.SA",
#             "BPAN4.SA",
#             "BRSR6.SA",
#             "MODL3.SA",
#             "WIZS3.SA",
#             "BOAS3.SA",
#             "CLSA3.SA",
#             "RANI3.SA",
#             "DXCO3.SA",
#             "BRAP4.SA",
#             "CBAV3.SA",
#             "FHER3.SA",
#             "UNIP6.SA",
#             "FESA4.SA",
#             "GOAU4.SA",
#             "USIM3.SA",
#             "USIM5.SA",
#             "RRRP3.SA",
#             "ENAT3.SA",
#             "RECV3.SA",
#             "BLAU3.SA",
#             "PNVL3.SA",
#             "PGMN3.SA",
#             "AALR3.SA",
#             "DASA3.SA",
#             "FLRY3.SA",
#             "PARD3.SA",
#             "MATD3.SA",
#             "ODPV3.SA",
#             "ONCO3.SA",
#             "QUAL3.SA",
#             "BMOB3.SA",
#             "ENJU3.SA",
#             "IFCM3.SA",
#             "LWSA3.SA",
#             "CASH3.SA",
#             "MBLY3.SA",
#             "SQIA3.SA",
#             "TRAD3.SA",
#             "AMBP3.SA",
#             "CSMG3.SA",
#             "ORVR3.SA",
#             "SAPR11.SA",
#             "AESB3.SA",
#             "ALUP11.SA",
#             "ENBR3.SA",
#             "LIGT3.SA",
#             "MEGA3.SA",
#         ]

#         self.etf = ["SMAL11.SA", "GOLD11.SA", "IVVB11.SA", "BOVA11.SA"]
#         self.lista_ativos_completa = list(
#             set(self.ibrx + self.ibov + self.smll + self.etf)
#         )

#     def __configura_quantidade_ativos(self) -> None:
#         if self.quantidade_ativos == "TODOS":
#             self.quantidade_ativos = len(self.lista_ativos_completa)

#         print(f"Inicialmente vai trabalhar com {self.quantidade_ativos} ativos.")

#     def __busca_ativos_aleatoriamente(self):
#         # Pega aleatoriamente {quantidade_ativos} dentro da lista
#         self.lista_ativos = random.sample(
#             self.lista_ativos_completa, int(self.quantidade_ativos)
#         )

#         print(f"Vai trabalhar com {self.quantidade_ativos} ativos.")
#         print(f"Vai trabalhar com os seguintes ativos:")
#         self.pp.pprint(self.lista_ativos)

#     def __busca_no_yfinance(self):
#         self.df_yahoo = yf.download(
#             self.lista_ativos, start=self.data_inicial, end=self.data_final
#         )
#         self.df = self.df_yahoo[self.dados_fechamento].copy()

#     def __trata_dados_do_yfinance(self):
#         """
#         Trata os dados do DataFrame retornado pelo Yahoo Finance.
#         """
#         if self.prioridade_nos_dados == "PERIODO":
#             self.df.dropna(axis=1, inplace=True)
#             self.lista_ativos = self.df.columns.to_list()
#             self.quantidade_ativos = len(self.lista_ativos)
#             print(
#                 "Limpando colunas (ATIVOS) inválidas - filtrando somente os ativos existentes no período."
#             )
#             self.pp.pprint(self.lista_ativos)
#         else:
#             self.df.dropna(axis=0, inplace=True)
#             print("Limpando linhas (DIAS) inválidas - diminuindo o período dos dados")

#         print(f"Número de ativos atualizado: {self.quantidade_ativos}.")
#         print(
#             "Data inicial: "
#             + self.df.first_valid_index().strftime("%d/%m/%Y")
#             + " (era "
#             + (self.data_inicial + timedelta(days=1)).strftime("%d/%m/%Y")
#             + ")"
#         )
#         print(
#             "Data final: "
#             + self.df.last_valid_index().strftime("%d/%m/%Y")
#             + " (era "
#             + (self.data_final - timedelta(days=1)).strftime("%d/%m/%Y")
#             + ")"
#         )

#     def retorna_dados(self) -> pd.DataFrame:
#         self.__configura_quantidade_ativos()
#         if not self.lista_ativos:
#             self.__busca_ativos_aleatoriamente()

#         self.__busca_no_yfinance()
#         self.__trata_dados_do_yfinance()
#         return self.df.copy()

#     def retorna_pares_ativos(self, retornar_invertidos=False) -> pd.DataFrame:
#         print(f"Considerando {self.quantidade_ativos} ativos.")
#         print(f"Considerando os seguintes ativos:")
#         print(self.lista_ativos)
#         print("")

#         lista_pares = [
#             (t1, t2)
#             for i, t1 in enumerate(self.lista_ativos)
#             for t2 in self.lista_ativos[i + 1 :]
#         ]

#         if retornar_invertidos == False:
#             print(f"Retornando {len(lista_pares)} pares.")
#             return lista_pares
#         else:
#             lista_pares_duplicados_invertidos = lista_pares.copy()

#             for i in lista_pares:
#                 lista_pares_duplicados_invertidos.append((i[1], i[0]))

#             print(f"Retornando {len(lista_pares_duplicados_invertidos)} pares.")
#             return lista_pares_duplicados_invertidos

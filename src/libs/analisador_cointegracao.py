import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# from sklearn.linear_model import LinearRegression
# import statsmodels.api as sm
# from statsmodels.tsa.stattools import adfuller


class AnalisadorCointegracao:
    # def set_df(self, df):
    #     self.df = df

    # def set_configuracoes(self, confianca_minima, distancia_da_media_interesse,
    #                       quantidade_comprar, plotar_cointegracao):
    #     self.plotar_cointegracao = plotar_cointegracao
    #     self.confianca_minima = confianca_minima
    #     self.distancia_da_media_interesse = distancia_da_media_interesse
    #     self.quantidade_comprar = quantidade_comprar

    def __init__(
        self,
        df,
        lista_pares,
        confianca_minima=0.9,
        distancia_da_media_interesse=1.8,  # NÚMERO DE DESVIOS
        quantidade_comprar=100,
        plotar_cointegracao=True,
    ):
        print(">> Iniciando AnalisadorCointegracao")

        self.plotar_cointegracao = plotar_cointegracao
        self.confianca_minima = confianca_minima
        self.distancia_da_media_interesse = distancia_da_media_interesse
        self.quantidade_comprar = quantidade_comprar

        self.df = df.tail(60)
        self.lista_pares = lista_pares

        # self.df_pc_change = self.df.pct_change()
        # self.__atualiza_dados_ativos()
        # self.__atualiza_pares_combinados()

    # def __atualiza_pares_combinados(self):
    #     self.lista_pares = None
    #     self.__preenche_pares_combinados()
    #     self.quantidade_pares = len(self.lista_pares)
    #     self.__adiciona_lista_pares_invetidos()

    # def __atualiza_dados_ativos(self):
    #     self.lista_ativos = list(self.df.columns)
    #     self.quantidade_ativos = len(self.lista_ativos)

    # def __preenche_pares_combinados(self):
    #      # Cria uma lista com os pares de ativos para comparação
    #     self.lista_pares = [(t1, t2) for i, t1 in enumerate(self.lista_ativos) for t2 in self.lista_ativos[i + 1:]]
    #     self.quantidade_pares = len(self.lista_pares)
    #     print("")
    #     print(f"Gerou {self.quantidade_pares} pares de ativos.")

    def gera_analise(self):
        for i in self.lista_pares:
            self.stock1 = i[0]
            self.stock2 = i[1]

            # import analisador_beta
            # ab = analisador_beta.AnalisadorBeta(self.stock1, self.stock2,
            #                                     self.df.first_valid_index().strftime("%Y-%m-%d"),
            #                                     self.df.last_valid_index().strftime("%Y-%m-%d"))

            # print("BETA 1> " + str(ab.retornar_beta_1()))
            # print("BETA 2> " + str(ab.retornar_beta_2()))
            # print("BETA 3> " + str(ab.retornar_beta_3()))

            self.x_independent = self.df[[self.stock1]].pct_change()
            self.x_independent.dropna(inplace=True)
            self.x_independent = self.x_independent.values.reshape(-1, 1)

            self.y_dependent = self.df[[self.stock2]].pct_change()
            self.y_dependent.dropna(inplace=True)
            self.y_dependent = self.y_dependent.values.reshape(-1, 1)

            reg = LinearRegression().fit(self.y_dependent, self.x_independent)
            self.beta = float(reg.coef_)
            self.b = float(reg.intercept_)

            print("BETA ORIGINAL> " + str(self.beta))
            print("B ORIGINAL> " + str(self.b))

            mod = sm.OLS(self.y_dependent, self.x_independent)
            resultado = mod.fit()
            print(resultado.summary())

            self.y_predict = reg.predict(self.x_independent)

            self.df_do_par_atual = self.df.copy(deep=True).iloc[1:]
            self.df_do_par_atual.loc[:, [self.stock1, self.stock2]]
            self.df_do_par_atual["Residual"] = self.y_dependent - self.y_predict

            self.mean = self.df_do_par_atual["Residual"].mean()
            self.std = self.df_do_par_atual["Residual"].std()

            test_series = adfuller(self.df_do_par_atual["Residual"])
            self.confidence = 1 - test_series[1]

            self.ultimo_residual = self.df_do_par_atual["Residual"].iloc[-1]

            # if self.confidence > float(self.confianca_minima) and abs(self.ultimo_residual) > (self.mean + self.std * float(self.distancia_da_media_interesse)):
            self.imprimir_relatorio()

            #    if self.plotar_cointegracao:
            # self.plotar_dados()
        print(">> FIM <<")

    def retornar_grafico_1(self):
        fig, axis = plt.subplots(1, 1, figsize=(10, 6))

        axis.scatter(self.x_independent, self.y_dependent, s=5)
        axis.plot(self.x_independent, self.y_predict, color="red", label="Linear Model")
        axis.set_xlabel(self.stock1)
        axis.set_ylabel(self.stock2)
        axis.legend()

        return fig.figure

    def retornar_grafico_2(self):
        k = 2  # Factor to shift the standard deviation
        up = self.mean + self.std * k
        down = self.mean - self.std * k

        fig, axis = plt.subplots(1, 1, figsize=(10, 6))

        # # PLOTA A REGRESSAO LINEAR
        # axis[0].scatter(self.x_independent, self.y_dependent, s=5)
        # axis[0].plot(self.x_independent, self.y_predict, color="red", label='Linear Model')
        # axis[0].set_xlabel(self.stock1)
        # axis[0].set_ylabel(self.stock2)
        # axis[0].legend()

        # PLOTA O RESIDUAL
        axis = self.df_do_par_atual["Residual"].plot(x="Major", y="", label="Resíduo")
        axis.axhline(y=self.mean, color="y", linestyle="--", linewidth=1, label="Média")
        axis.axhline(y=up, color="b", linestyle="--", linewidth=1, label=f"+/-{k} STD")
        axis.axhline(y=down, color="b", linestyle="--", linewidth=1, label="_nolegend_")
        axis.set_title("Análise do Resíduo")
        axis.legend(loc="upper right", ncol=2)

        return fig.figure

    def plotar_dados(self):
        k = 2  # Factor to shift the standard deviation
        up = self.mean + self.std * k
        down = self.mean - self.std * k

        _, axis = plt.subplots(1, 2, figsize=(15, 4))

        # PLOTA A REGRESSAO LINEAR
        axis[0].scatter(self.x_independent, self.y_dependent, s=5)
        axis[0].plot(
            self.x_independent, self.y_predict, color="red", label="Linear Model"
        )
        axis[0].set_xlabel(self.stock1)
        axis[0].set_ylabel(self.stock2)
        axis[0].legend()

        # PLOTA O RESIDUAL
        axis[1] = self.df_do_par_atual["Residual"].plot(
            x="Major", y="", label="Resíduo"
        )
        axis[1].axhline(
            y=self.mean, color="y", linestyle="--", linewidth=1, label="Média"
        )
        axis[1].axhline(
            y=up, color="b", linestyle="--", linewidth=1, label=f"+/-{k} STD"
        )
        axis[1].axhline(
            y=down, color="b", linestyle="--", linewidth=1, label="_nolegend_"
        )
        axis[1].set_title("Análise do Resíduo")
        axis[1].legend(loc="upper right", ncol=2)

        plt.show()

    def imprimir_relatorio(self):
        # print("====================")
        # print(f"Último RESIDUAL ABSOLUTO: {abs(ultimo_residual)}")
        # print(f"INTERESSE: {distancia_da_media_interesse} DP: " + str((mean + std * distancia_da_media_interesse)))
        print("====================")
        print("REALIZAR O TRADE:")
        print("Data da análise: " + datetime.date.today().strftime("%d/%m/%Y"))
        print(
            "Data inicial dos dados: "
            + self.df.first_valid_index().strftime("%d/%m/%Y")
        )  # + " (era " + self.data_inicial.strftime("%d/%m/%Y") + ")")
        print(
            "Data final dos dados: " + self.df.last_valid_index().strftime("%d/%m/%Y")
        )  # + " (era " + self.data_final.strftime("%d/%m/%Y") + ")")

        if self.ultimo_residual > 0:
            stock_vender = self.stock1
            stock_comprar = self.stock2
        else:
            stock_comprar = self.stock1
            stock_vender = self.stock2

        valor_gasto_compra = str(
            round(float(self.df[stock_comprar].iloc[-1] * self.quantidade_comprar), 2)
        )
        quantidade_vender = float(self.beta * float(self.quantidade_comprar))
        valor_recebido_venda = str(
            round(float(self.df[stock_vender].iloc[-1] * quantidade_vender), 2)
        )
        print(
            f"COMPRAR {self.quantidade_comprar} {stock_comprar} -> R$ - {valor_gasto_compra}"
        )
        print(
            f"VENDER {quantidade_vender} {stock_vender} -> R$ + {valor_recebido_venda}"
        )

        # print('ADF Statistic: %f' % test_series[0])
        # print('p-value: %f' % test_series[1])
        # print('Critical values:')
        # for key, value in test_series[4].items():
        #     print('\t%s: %.3f' % (key, value))
        print(f"Confiança (Dickey-Fuller): {self.confidence:.2%}")
        print("beta = %f" % self.beta)

    # def calculate_residual(self, df, time_period):
    #     # values converted into a numpy array
    #     # '-1' to calculate the dimension of rows, and '1' to have only 1 column
    #     x_independent = df.iloc[-time_period:,1].values.reshape(-1, 1)
    #     y_dependent   = df.iloc[-time_period:,0].values.reshape(-1, 1)
    #     # performing the linear regression
    #     reg = LinearRegression().fit(x_independent, y_dependent)

    #     # get the predicted Y given X from the model
    #     y_predict  = reg.predict(x_independent)

    #     # attaching the residual (Y_dependent-Y_predict) from a numpy array to a pandas series
    #     residual = pd.DataFrame(np.array(y_dependent - y_predict), columns=['Residual'])

    #     return residual

    # def check_stationary(self, df, time_periods, min_confidence=95):
    #     # initialising an empty list that will receive the output
    #     stationary_intervals = []

    #     # loop over the list for all time periods
    #     for t in time_periods:
    #         # call the function to calculate the residuals
    #         residual, beta = self.calculate_residual(df, t)
    #         # performing the Augmented Dickey-Fuller test in the residual
    #         residual_test = adfuller(residual['Residual'])
    #         # calculating the condidence in percentage from the p-value (index 1 of the output test)
    #         confidence = 100 * (1 - residual_test[1])
    #         # testing for stationarity given a threshold
    #         if confidence >= min_confidence:
    #             stationary_intervals.append(True)
    #         else:
    #             stationary_intervals.append(False)

    #     # return the interval and if it is stationary
    #     return stationary_intervals

    # def plot_residual(self, df, time_period):

    #     df = df.iloc[-time_period:].copy()

    #     std  = df['Z-Score'].std()

    #     up = 2 * std
    #     down = -2 * std
    #     stop_up = 3 * std
    #     stop_down = -3 * std

    #     plt.title("Z-Score for t = %i" %time_period)
    #     df['Z-Score'].plot(x="Major", y="", figsize=(14,6))
    #     plt.axhline(y=0, color='y', linestyle='-')
    #     plt.axhline(y=up,   color='b', linestyle='-')
    #     plt.axhline(y=down, color='b', linestyle='-')
    #     plt.axhline(y=stop_up,   color='r', linestyle='-')
    #     plt.axhline(y=stop_down, color='r', linestyle='-')

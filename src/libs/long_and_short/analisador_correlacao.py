import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class AnalisadorCorrelacao:
    def __init__(self, df, lista_pares, dados_fechamento="Adj Close",
                 plotar_correlacoes='SIM', numero_maximo_plotagens=5, correlacao_minima='.8',
                 filtrar_correlacoes_interesse_no_heatmap='SIM', limite_ativos_para_heatmap=25):
        print(">> Iniciando Analisador Correlação")

        self.df = df
        self.lista_pares = lista_pares
        self.dados_fechamento = dados_fechamento
        self.quantidade_de_ativos = len(df.axes[1])

        self.plotar_correlacoes = plotar_correlacoes
        self.numero_maximo_plotagens = numero_maximo_plotagens
        self.correlacao_minima = correlacao_minima
        self.filtrar_correlacoes_interesse_no_heatmap = filtrar_correlacoes_interesse_no_heatmap
        self.limite_ativos_para_heatmap = limite_ativos_para_heatmap

    def retornar_grafico_1(self, stock1, stock2):
        df_par = None
        df_par = self.df[[stock1, stock2]]
            
        mean_stock1 = self.df[stock1].mean()
        mean_stock2 = self.df[stock2].mean()
                
        fig1 = df_par.plot(linewidth=1)
        fig1.axhline(y=mean_stock1, color='#49ce8b', linestyle='--', linewidth=2, label=f'Média {stock1}')
        fig1.axhline(y=mean_stock2, color='#033660', linestyle='--', linewidth=2, label=f'Média {stock2}')
        fig1.set_title(f"{stock1} e {stock2} ({self.dados_fechamento})" + " Correlação=" + str(round(self.__retornar_correlacao_baseada_perc_change(df_par), 2)))
        fig1.legend()
        return fig1.figure
    
    def retornar_grafico_2(self, stock1, stock2):
        df_par = None
        df_par = self.df[[stock1, stock2]]
        normalized_df_par = df_par / df_par.iloc[0]
        fig2 = normalized_df_par.plot(linewidth=1)
        fig2.set_title(f"{stock1} norm e {stock2} norm")
        fig2.legend()        
        return fig2.figure
    
    def retornar_grafico_3(self, stock1, stock2):
        df_par = None
        df_par = self.df[[stock1, stock2]]
        normalized_df_par = df_par / df_par.iloc[0]
        divisao_df = normalized_df_par[stock1] / normalized_df_par[stock2]
        mean_divisao_df = divisao_df.mean()
        fig3 = divisao_df.plot(linewidth=1)
        fig3.axhline(y=1, color='#49ce8b', linestyle='--',
                        linewidth=2, label=f'1')
        fig3.axhline(y=mean_divisao_df, color='#033660',
                        linestyle='--', linewidth=2, label=f'Média')
        fig3.set_title(f"RATIO {stock1} norm / {stock2} norm")
        fig3.legend()
        return fig3.figure
    
    def retornar_grafico_4(self, stock1, stock2):
        df_par = None
        df_par = self.df[[stock1, stock2]]        
        correlacao_df = self.__retorna_df_correcao_periodos(df_par)
        mean_correlacao_df = correlacao_df["Correlação"].mean()
        fig4 = correlacao_df.plot(style=['rs-', '-'], linewidth=1)
        fig4.axhline(y=mean_correlacao_df, color='#033660',linestyle='--', linewidth=2, label=f'Média')
        fig4.set_title(f"Correlação {stock1} e {stock2} nos últimos X dias")
        fig4.invert_xaxis()
        fig4.legend()
        return fig4.figure

    def executa_analise(self):
        print(f"PLOTAR_CORRELACOES? {self.plotar_correlacoes}")
        print(f"CORRELACAO_MINIMA? {self.correlacao_minima}")
        print(f"NUMERO_MAXIMO_PLOTAGENS? {self.numero_maximo_plotagens}")

        numero_plotagens = 0
        for i in self.lista_pares:
            stock1 = i[0]
            stock2 = i[1]

            # print(f"Iniciando análise da relação {stock1} e {stock2}")

            df_par = None
            df_par = self.df[[stock1, stock2]]

            if self.__possui_correlacao_de_interesse(df_par) and self.plotar_correlacoes == "SIM" \
                    and numero_plotagens < self.numero_maximo_plotagens:
                mean_stock1 = self.df[stock1].mean()
                mean_stock2 = self.df[stock2].mean()

                normalized_df_par = df_par / df_par.iloc[0]
                # print(plt.style.available)
                # ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh',
                #  'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8',
                #  'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette',
                #  'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook',
                #  'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk',
                #  'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']

                plt.style.use('ggplot')
                fig, axis = plt.subplots(2, 2, figsize=(15, 10))
                plt.rcParams['figure.dpi'] = 250

                fig1 = df_par.plot(ax=axis[0, 0], linewidth=1)
                fig1.axhline(y=mean_stock1, color='#49ce8b',
                             linestyle='--', linewidth=2, label=f'Média {stock1}')
                fig1.axhline(y=mean_stock2, color='#033660',
                             linestyle='--', linewidth=2, label=f'Média {stock2}')
                fig1.set_title(f"{stock1} e {stock2} ({self.dados_fechamento})" + " Correlação=" + str(
                    round(self.__retornar_correlacao_baseada_perc_change(df_par), 2)))
                fig1.legend()
                # plt.show()

                fig2 = normalized_df_par.plot(ax=axis[0, 1], linewidth=1)
                fig2.set_title(f"{stock1} norm e {stock2} norm")
                fig2.legend()
                # plt.show()

                divisao_df = normalized_df_par[stock1] / \
                    normalized_df_par[stock2]
                mean_divisao_df = divisao_df.mean()
                fig3 = divisao_df.plot(ax=axis[1, 0], linewidth=1)
                fig3.axhline(y=1, color='#49ce8b', linestyle='--',
                             linewidth=2, label=f'1')
                fig3.axhline(y=mean_divisao_df, color='#033660',
                             linestyle='--', linewidth=2, label=f'Média')
                fig3.set_title(f"RATIO {stock1} norm / {stock2} norm")
                fig3.legend()

                correlacao_df = self.__retorna_df_correcao_periodos(df_par)
                mean_correlacao_df = correlacao_df["Correlação"].mean()

                fig4 = correlacao_df.plot(ax=axis[1, 1], style=['rs-', '-'], linewidth=1)
                fig4.axhline(y=mean_correlacao_df, color='#033660',linestyle='--', linewidth=2, label=f'Média')
                fig4.set_title(f"Correlação {stock1} e {stock2} nos últimos X dias")
                fig4.invert_xaxis()
                fig4.legend()

                fig.tight_layout(pad=2.0)
                numero_plotagens += 1
                print(">>> FIM <<<")
                return fig #.show()

    # def __retorna_correlacao(self, df_par):
    #     df_correlacao = df_par.corr()
    #     # print(df_correlacao)
    #     if df_correlacao.size != 4:
    #         raise ValueError("Dataframe de tamanho inválido.")
    #     return df_correlacao.iloc[0][1]

    def __retornar_correlacao_baseada_perc_change(self, df_par):
        df_temp = df_par.copy()
        df_temp["%1"] = df_temp[df_temp.columns[0]].pct_change()
        df_temp["%2"] = df_temp[df_temp.columns[1]].pct_change()
        df_temp.drop(df_par.columns, axis=1, inplace=True)
        df_temp = df_temp[1:]
        df_correlacao = df_temp.corr()
        # print("Y")
        # pp.pprint(df_correlacao)
        if df_correlacao.size != 4:
            raise ValueError("Dataframe de tamanho inválido.")
        return df_correlacao.iloc[0][1]

    def __imprime_correlacoes_em_periodos_menores(self, df_par):
        periodos_em_dias = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 
                            550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
        periodo_maximo = len(df_par)
        periodos_para_analise = list(
            filter(lambda x: x < periodo_maximo, list(reversed(periodos_em_dias))))
        for i in periodos_para_analise:
            correlacao = self.__retornar_correlacao_baseada_perc_change(
                df_par.head(i))
            print(f">> Correlação histórica: {correlacao} em {i} dias úteis")

    def __possui_correlacao_de_interesse(self, df_par):
        # print("X")
        # pp.pprint(df_par)
        correlacao = self.__retornar_correlacao_baseada_perc_change(df_par)
        condicao = (abs(float(correlacao)) > float(self.correlacao_minima))
        if condicao:
            print(f"{df_par.columns[0]} e {df_par.columns[1]}:")
            print(
                f">> Correlação de interesse encontrada: {correlacao} em {len(df_par)} dias úteis")
            self.__imprime_correlacoes_em_periodos_menores(df_par)
        return condicao

    def __retorna_df_correcao_periodos(self, df_par):
        data = []
        data.append(
            [len(df_par), self.__retornar_correlacao_baseada_perc_change(df_par)])
        periodos_em_dias = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 
                            550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
        periodo_maximo = len(df_par)
        periodos_para_analise = list(
            filter(lambda x: x < periodo_maximo, periodos_em_dias))
        for i in periodos_para_analise:
            data.append(
                [i, self.__retornar_correlacao_baseada_perc_change(df_par.head(i))])

        df_correlacao = pd.DataFrame(data, columns=['Dias', 'Correlação'])
        df_correlacao.set_index('Dias', inplace=True)
        df_correlacao.sort_index(ascending=False, inplace=True)

        df_correlacao = df_correlacao.reindex(list(
            range(df_correlacao.index.min(), df_correlacao.index.max()+1)), fill_value=0)
        df_correlacao.replace(0, np.nan, inplace=True)
        df_correlacao["Interpolação"] = df_correlacao["Correlação"].interpolate(
            method="polynomial", order=5)

        return df_correlacao

    def cria_heatmap(self):
        df_para_heatmap = self.df.pct_change()
        df_para_heatmap.dropna(inplace=True)
        df_para_heatmap = df_para_heatmap.corr()
        df_para_heatmap = df_para_heatmap.where(np.tril(
            np.ones(df_para_heatmap.shape), k=0).astype(bool))  # parametro k faz o corte

        if self.filtrar_correlacoes_interesse_no_heatmap == "SIM":
            df_para_heatmap[(df_para_heatmap > -float(self.correlacao_minima))
                            & (df_para_heatmap < float(self.correlacao_minima))] = np.nan

        if (self.quantidade_de_ativos > float(self.limite_ativos_para_heatmap)):
            lista_correlacionados = df_para_heatmap.unstack()
            lista_correlacionados = lista_correlacionados.where((abs(lista_correlacionados) > float(
                self.correlacao_minima)) & (abs(lista_correlacionados) != 1.0)).dropna()
            lista_correlacionados_ordenados = lista_correlacionados.sort_values(
                kind="quicksort")
            print(
                f"Correlações de interesse (mostrando modo texto pois tem mais de {self.limite_ativos_para_heatmap} ativos):")
            print("")
            print(lista_correlacionados_ordenados)
        else:
            plt.figure(figsize=(self.quantidade_de_ativos,
                       self.quantidade_de_ativos))
            plt.title(f"Correlações de interesse", fontsize=20)
            sns.heatmap(df_para_heatmap, vmin=-1,
                        vmax=1, annot=True, cmap='BrBG')
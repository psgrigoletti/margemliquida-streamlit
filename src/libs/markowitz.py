# import scipy.optimize as sco
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Markowitz:
    __precos_fechamento = None
    __retornos_diarios = None
    __retornos_medios = None
    __matriz_covariancia = None
    __taxa_livre_de_risco = None
    __acoes = None
    __numero_de_portfolios_aleatorios = None

    def __init__(
        self, precos_fechamento, taxa_livre_de_risco, numero_de_portfolios_aleatorios
    ):
        self.__precos_fechamento = precos_fechamento
        self.__taxa_livre_de_risco = taxa_livre_de_risco
        self.__numero_de_portfolios_aleatorios = numero_de_portfolios_aleatorios

        self.__acoes = self.__precos_fechamento.columns
        self.__retornos_diarios = self.__precos_fechamento.pct_change()
        self.__retornos_medios = self.__retornos_diarios.mean()
        self.__matriz_covariancia = self.__retornos_diarios.cov()

    def __portfolio_annualised_performance(self, pesos):
        returns = np.sum(self.__retornos_medios * pesos) * 252
        std = np.sqrt(
            np.dot(pesos.T, np.dot(self.__matriz_covariancia, pesos))
        ) * np.sqrt(252)
        return std, returns

    def __random_portfolios(self):
        results = np.zeros((3, self.__numero_de_portfolios_aleatorios))
        weights_record = []
        for i in range(self.__numero_de_portfolios_aleatorios):
            weights = np.random.random(len(self.__acoes))
            weights /= np.sum(weights)
            weights_record.append(weights)
            (
                portfolio_std_dev,
                portfolio_return,
            ) = self.__portfolio_annualised_performance(weights)
            results[0, i] = portfolio_std_dev
            results[1, i] = portfolio_return
            results[2, i] = (
                portfolio_return - self.__taxa_livre_de_risco
            ) / portfolio_std_dev
            # TODO: implementar usando o https://www.investopedia.com/terms/s/sortinoratio.asp
            # comparar https://www.codearmo.com/blog/sharpe-sortino-and-calmar-ratios-python
        return results, weights_record

    def retornar_grafico_fronteira_eficiente_aleatorio(self):
        results, weights = self.__random_portfolios()

        max_sharpe_idx = np.argmax(results[2])
        sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
        max_sharpe_allocation = pd.DataFrame(
            weights[max_sharpe_idx],
            index=self.__precos_fechamento.columns,
            columns=["allocation"],
        )
        max_sharpe_allocation.allocation = [
            round(i * 100, 2) for i in max_sharpe_allocation.allocation
        ]
        max_sharpe_allocation = max_sharpe_allocation.T

        min_vol_idx = np.argmin(results[0])
        sdp_min, rp_min = results[0, min_vol_idx], results[1, min_vol_idx]
        min_vol_allocation = pd.DataFrame(
            weights[min_vol_idx],
            index=self.__precos_fechamento.columns,
            columns=["allocation"],
        )
        min_vol_allocation.allocation = [
            round(i * 100, 2) for i in min_vol_allocation.allocation
        ]
        min_vol_allocation = min_vol_allocation.T

        print("-" * 80)
        print("Maximum Sharpe Ratio Portfolio Allocation\n")
        print("Annualised Return:", round(rp, 2))
        print("Annualised Volatility:", round(sdp, 2))
        print("\n")
        print(max_sharpe_allocation)
        print("-" * 80)
        print("Minimum Volatility Portfolio Allocation\n")
        print("Retorno anual:", round(rp_min, 2))
        print("Volatility:", round(sdp_min, 2))
        print("\n")
        print(min_vol_allocation)

        fig7 = plt.figure(figsize=(25, 15))
        plt.scatter(
            results[0, :],
            results[1, :],
            c=results[2, :],
            cmap="YlGnBu",
            marker="o",
            s=10,
            alpha=0.3,
        )
        plt.colorbar()
        plt.scatter(sdp, rp, marker="*", color="r", s=500, label="Maximum Sharpe ratio")
        plt.scatter(
            sdp_min, rp_min, marker="*", color="g", s=500, label="Minimum volatility"
        )
        plt.title("Simulated Portfolio Optimization based on Efficient Frontier")
        plt.xlabel("Volatilidade anual")
        plt.ylabel("Retorno anual")
        plt.legend(labelspacing=1)
        return fig7

    def __neg_sharpe_ratio(self, weights):
        p_var, p_ret = self.portfolio_annualised_performance(weights)
        return -(p_ret - self.__taxa_livre_de_risco) / p_var

    def __max_sharpe_ratio(self):
        num_assets = len(self.__retornos_medios)
        args = (
            self.__retornos_medios,
            self.__matriz_covariancia,
            self.__taxa_livre_de_risco,
        )
        constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))
        result = sco.minimize(
            self.__neg_sharpe_ratio,
            num_assets
            * [
                1.0 / num_assets,
            ],
            args=args,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        return result

    def __portfolio_volatility(self, weights):
        return self.portfolio_annualised_performance(weights)[0]

    def min_variance(self):
        num_assets = len(self.__retornos_medios)
        args = (self.__retornos_medios, self.__matriz_covariancia)
        constraints = {"type": "eq", "fun": lambda x: np.sum(x) - 1}
        bound = (0.0, 1.0)
        bounds = tuple(bound for asset in range(num_assets))

        result = sco.minimize(
            self.__portfolio_volatility,
            num_assets
            * [
                1.0 / num_assets,
            ],
            args=args,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )

        return result

    def __efficient_return(self, target):
        num_assets = len(self.__retornos_medios)
        args = (self.__retornos_medios, self.__matriz_covariancia)

        def portfolio_return(weights):
            return self.portfolio_annualised_performance(weights)[1]

        constraints = (
            {"type": "eq", "fun": lambda x: portfolio_return(x) - target},
            {"type": "eq", "fun": lambda x: np.sum(x) - 1},
        )
        bounds = tuple((0, 1) for asset in range(num_assets))
        result = sco.minimize(
            self.portfolio_volatility,
            num_assets
            * [
                1.0 / num_assets,
            ],
            args=args,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints,
        )
        return result

    def __efficient_frontier(self, returns_range):
        efficients = []
        for ret in returns_range:
            efficients.append(self.__efficient_return(ret))
        return efficients

    def display_simulated_ef_with_random(self):
        results, _ = self.__random_portfolios()

        max_sharpe = self.__max_sharpe_ratio()
        sdp, rp = self.portfolio_annualised_performance(
            max_sharpe["x"], self.__retornos_medios
        )
        max_sharpe_allocation = pd.DataFrame(
            max_sharpe.x, index=self.__precos_fechamento.columns, columns=["allocation"]
        )
        max_sharpe_allocation.allocation = [
            round(i * 100, 2) for i in max_sharpe_allocation.allocation
        ]
        max_sharpe_allocation = max_sharpe_allocation.T

        min_vol = self.min_variance()
        sdp_min, rp_min = self.portfolio_annualised_performance(
            min_vol["x"], self.__retornos_medios
        )
        min_vol_allocation = pd.DataFrame(
            min_vol.x, index=self.__precos_fechamento.columns, columns=["allocation"]
        )
        min_vol_allocation.allocation = [
            round(i * 100, 2) for i in min_vol_allocation.allocation
        ]
        min_vol_allocation = min_vol_allocation.T

        self.retornar_texto_ef_with_random(
            rp, sdp, max_sharpe_allocation, rp_min, sdp_min, min_vol_allocation
        )
        self.retornar_grafico_ef_with_random(results, sdp, rp, sdp_min, rp_min)

    def retornar_texto_ef_with_random(
        self, rp, sdp, max_sharpe_allocation, rp_min, sdp_min, min_vol_allocation
    ):
        retorno_textual = "-" * 80
        retorno_textual += "Maximum Sharpe Ratio Portfolio Allocation\n"
        retorno_textual += "Retorno anual:" + round(rp, 2)
        retorno_textual += "Volatilidade anual:" + round(sdp, 2)
        retorno_textual += "\n"
        retorno_textual += max_sharpe_allocation
        retorno_textual += "-" * 80
        retorno_textual += "Minimum Volatility Portfolio Allocation\n"
        retorno_textual += "Retorno anual:", round(rp_min, 2)
        retorno_textual += "Volatidade anual:", round(sdp_min, 2)
        retorno_textual += "\n"
        retorno_textual += min_vol_allocation
        return retorno_textual

    def display_ef_with_selected(self):
        max_sharpe = self.__max_sharpe_ratio()
        sdp, rp = self.portfolio_annualised_performance(max_sharpe["x"])
        max_sharpe_allocation = pd.DataFrame(
            max_sharpe.x, index=self.__precos_fechamento.columns, columns=["allocation"]
        )
        max_sharpe_allocation.allocation = [
            round(i * 100, 2) for i in max_sharpe_allocation.allocation
        ]
        max_sharpe_allocation = max_sharpe_allocation.T

        min_vol = self.min_variance()
        sdp_min, rp_min = self.portfolio_annualised_performance(min_vol["x"])
        min_vol_allocation = pd.DataFrame(
            min_vol.x, index=self.__precos_fechamento.columns, columns=["allocation"]
        )
        min_vol_allocation.allocation = [
            round(i * 100, 2) for i in min_vol_allocation.allocation
        ]
        min_vol_allocation = min_vol_allocation.T

        an_vol = np.std(self.__retornos_medios) * np.sqrt(252)
        an_rt = self.__retornos_medios * 252

        # print(self.retornar_texto_ef_with_selected(rp, sdp, max_sharpe_allocation, rp_min, sdp_min, min_vol_allocation, an_rt, an_vol))
        # return self.retornar_grafico_ef_with_selected(an_vol, an_rt, sdp, rp, sdp_min, rp_min)

    def retornar_texto_ef_with_selected(
        self,
        rp,
        sdp,
        max_sharpe_allocation,
        rp_min,
        sdp_min,
        min_vol_allocation,
        an_rt,
        an_vol,
    ):
        retorno_textual = "-" * 80
        retorno_textual += "\nMaximum Sharpe Ratio Portfolio Allocation"
        retorno_textual += "\nAnnualised Return:" + str(round(rp, 2))
        retorno_textual += "\nAnnualised Volatility: " + str(round(sdp, 2))
        retorno_textual += "\n"
        retorno_textual += str(max_sharpe_allocation) + "\n"
        retorno_textual += "-" * 80
        retorno_textual += "\nMinimum Volatility Portfolio Allocation"
        retorno_textual += "\nAnnualised Return: " + str(round(rp_min, 2))
        retorno_textual += "\nAnnualised Volatility: " + str(round(sdp_min, 2))
        retorno_textual += "\n"
        retorno_textual += str(min_vol_allocation) + "\n"
        retorno_textual += "-" * 80
        retorno_textual += "\nIndividual Stock Returns and Volatility\n"
        for i, txt in enumerate(self.__precos_fechamento.columns):
            retorno_textual += (
                "["
                + str(txt)
                + "]: annuaised return: "
                + str(round(an_rt[i], 2))
                + ", annualised volatility: "
                + str(round(an_vol[i], 2))
                + "\n"
            )
        retorno_textual += "-" * 80
        return retorno_textual


class GraficosMarkowitz:
    def __init__(self, markowitz: Markowitz):
        self.__markowitz = markowitz

    def retornar_grafico_de_precos_normalizados(self):
        normalizado = (
            self.__markowitz.__precos_fechamento
            / self.__markowitz.__precos_fechamento.iloc[0]
        )
        fig = normalizado.plot(figsize=(12, 8), ylabel="Preço", xlabel="Período")
        return fig.figure

    def retornar_grafico_de_precos(self):
        fig = self.__markowitz.__precos_fechamento.plot(
            figsize=(12, 8), ylabel="Preço", xlabel="Período"
        )
        return fig.figure

    def retornar_grafico_retornos_diarios(self):
        fig = plt.figure(figsize=(12, 8))
        for c in self.__markowitz.__retornos_diarios.columns.values:
            plt.plot(
                self.__markowitz.__retornos_diarios.index,
                self.__markowitz.__retornos_diarios[c],
                lw=3,
                alpha=0.8,
                label=c,
            )
        plt.legend(loc="best", fontsize=14)
        plt.ylabel("Retornos diários")
        return fig

    def retornar_matriz_correlacao(self):
        mascara_grafico = np.triu(self.__markowitz.__correlacao)
        fig = plt.figure(
            num=None, figsize=(10, 10), dpi=100, facecolor="w", edgecolor="k"
        )
        _ = sns.heatmap(
            self.__markowitz.__correlacao,
            annot=True,
            vmin=-1,
            vmax=1,
            cmap="viridis",
            linewidths=0.5,
            mask=mascara_grafico,
        )
        plt.title("Matriz de correlação entre os ativos")
        return fig

    def retornar_matriz_risco_retorno(self):
        fig = plt.figure(
            num=None, figsize=(10, 10), dpi=80, facecolor="w", edgecolor="k"
        )
        _ = sns.heatmap(
            self.__markowitz.__matriz_covariancia,
            annot=True,
            vmin=-1,
            vmax=1,
            cmap="viridis",
            linewidths=0.5,
        )
        plt.title("Matriz de correlação")
        return fig

    def retornar_grafico_vol_e_retornos_medios(self):
        volatilidade = pd.DataFrame(
            self.__markowitz.__retornos_diarios.std(), columns=["Volatilidade"]
        )
        retornos_medios = pd.DataFrame(
            self.__markowitz.__retornos_medios, columns=["Retorno"]
        )
        matriz_risco_retorno = pd.concat([retornos_medios, volatilidade], axis=1)
        fig, _ = plt.subplots(figsize=(5, 5))

        sns.scatterplot(data=matriz_risco_retorno, x="Volatilidade", y="Retorno")

        for i in range(matriz_risco_retorno.shape[0]):
            plt.text(
                x=matriz_risco_retorno.Volatilidade[i],
                y=matriz_risco_retorno.Retorno[i],
                s=matriz_risco_retorno.index[i],
                fontdict=dict(color="red", size=20),
                bbox=dict(facecolor="yellow", edgecolor="black"),
            )
        return fig

    def retornar_grafico_ef_with_selected(
        self, an_vol, an_rt, sdp, rp, sdp_min, rp_min
    ):
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.scatter(an_vol, an_rt, marker="o", s=200)

        for i, txt in enumerate(self.__markowitz.__precos_fechamento.columns):
            ax.annotate(
                txt, (an_vol[i], an_rt[i]), xytext=(10, 0), textcoords="offset points"
            )
        ax.scatter(sdp, rp, marker="*", color="r", s=500, label="Maximum Sharpe ratio")
        ax.scatter(
            sdp_min, rp_min, marker="*", color="g", s=500, label="Minimum volatility"
        )
        target = np.linspace(rp_min, 0.34, 50)
        efficient_portfolios = self.__markowitz.__efficient_frontier(target)
        ax.plot(
            [p["fun"] for p in efficient_portfolios],
            target,
            linestyle="-.",
            color="black",
            label="efficient frontier",
        )
        ax.set_title("Portfolio Optimization with Individual Stocks")
        ax.set_xlabel("annualised volatility")
        ax.set_ylabel("annualised returns")
        ax.legend(labelspacing=0.8)
        return fig

    def retornar_grafico_ef_with_random(self, results, sdp, rp, sdp_min, rp_min):
        fig = plt.figure(figsize=(25, 15))
        plt.scatter(
            results[0, :],
            results[1, :],
            c=results[2, :],
            cmap="YlGnBu",
            marker="o",
            s=10,
            alpha=0.3,
        )
        plt.colorbar()
        plt.scatter(
            sdp,
            rp,
            marker="*",
            color="r",
            s=500,
            label="Retorno máximo (Maximum Sharpe ratio)",
            linewidths=5,
        )
        plt.scatter(
            sdp_min,
            rp_min,
            marker="*",
            color="g",
            s=500,
            label="Volatilidade mínima",
            linewidths=5,
        )
        target = np.linspace(rp_min, 0.32, 50)
        plt.plot(
            [p["fun"] for p in self.__markowitz.__efficient_frontier(target)],
            target,
            linestyle="-.",
            color="black",
            label="Fronteira eficiente",
        )
        plt.title("Calculated Portfolio Optimization based on Efficient Frontier")
        plt.xlabel("Volatilidade anual")
        plt.ylabel("Retorno anual")
        plt.legend(labelspacing=1)
        return fig

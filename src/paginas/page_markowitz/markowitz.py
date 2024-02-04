import datetime
import pprint
from enum import Enum

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import riskfolio
import yfinance as yf

pd.options.display.float_format = "{:.4%}".format

print("matplotlib: ", matplotlib.__version__)
print("riskfolio: ", riskfolio.__version__)
print("yfinance: ", yf.__version__)
print("pandas: ", pd.__version__)


class Objetivo(Enum):
    MIN_RISK = "MinRisk"
    MAX_RET = "MaxRet"
    SHARPE = "Sharpe"


class Markowitz:
    def __init__(self, tickers, data_inicial, data_final):
        self._tickers = tickers
        self._data_inicial = data_inicial
        self._data_final = data_final
        self._df = None
        self._y = None
        self._method_mu = "hist"
        self._method_cov = "hist"
        self._model = None
        self._w = None
        self._w_fronteira = None
        self._rm = None
        self._obj = None  # Função objetivo, pode ser MinRisk, MaxRet, Utility, Sharpe
        self._hist = None  # Usar cenários históricos para medidas de risco que dependem de cenários
        self._rf = None  # Taxa livre de risco
        self._l = (
            None  # Fator de aversão ao risco, útil apenas para o objetivo 'Utility'
        )
        self._tickers.sort()

    def buscar_dados(self):
        self._df = yf.download(
            tickers=self._tickers, start=self._data_inicial, end=self._data_final
        )
        self._df = self._df.loc[:, ("Adj Close", slice(None))]
        self._df.columns = self._tickers

        self._df.ffill(inplace=True)

        nan_values = self._df.isna().any().any()
        if nan_values:
            print("Existem valores NaN no DataFrame.")
        else:
            print("Não há valores NaN no DataFrame.")
        # Calculating returns
        self._y = self._df[self._tickers].pct_change().dropna()

    def simular(self, objetivo: Objetivo):
        # self._y = self._df.pct_change().dropna()
        self._portfolio = riskfolio.Portfolio(returns=self._y)
        self._portfolio.assets_stats(
            method_mu=self._method_mu, method_cov=self._method_cov, d=0.94
        )

        self._model = "Classic"
        self._rm = "MV"
        self._obj = (
            objetivo  # Função objetivo, pode ser MinRisk, MaxRet, Utility, Sharpe
        )
        self._hist = True  # Usar cenários históricos para medidas de risco que dependem de cenários
        self._rf = 0  # Taxa livre de risco
        self._l = 0  # Fator de aversão ao risco, útil apenas para o objetivo 'Utility'

        # Otimização
        self._w = self._portfolio.optimization(
            model=self._model,
            rm=self._rm,
            obj=self._obj,
            rf=self._rf,
            l=self._l,
            hist=self._hist,
        )
        print("Pesos: ")
        pprint.pprint(self._w.T)

    def gerar_grafico_conjunto_oportunidades(self):
        pass

    def gerar_grafico_fronteira(self):
        self._points = 50  # Número de pontos da fronteira

        self._w_fronteira = self._portfolio.efficient_frontier(
            model=self._model,
            rm=self._rm,
            points=self._points,
            rf=self._rf,
            hist=self._hist,
        )
        mu = self._portfolio.mu  # retorno esperado
        cov = self._portfolio.cov  # matriz de covariância
        returns = self._portfolio.returns  # retorno dos ativos

        _ = riskfolio.plot_frontier(
            w_frontier=self._w_fronteira,
            mu=mu,
            cov=cov,
            returns=returns,
            rm=self._rm,
            rf=self._rf,
            alpha=0.05,
            cmap="viridis",
            w=self._w,
            s=16,
            c="r",
            height=6,
            width=10,
            ax=None,
            t_factor=12,
        )
        plt.show(block=True)

    def gerar_grafico_historico(self):
        _ = riskfolio.plot_series(
            returns=self._y, w=self._w, height=6, width=10, ax=None
        )
        plt.show(block=True)

    def gerar_grafico_composicao_carteira(self):
        _ = riskfolio.plot_pie(
            w=self._w,
            title="Composição da carteira",
            others=0.05,
            nrow=25,
            cmap="tab20",
            height=6,
            width=10,
            ax=None,
        )
        plt.show(block=True)

    def gerar_grafico_drawdown(self):
        _ = riskfolio.plot_drawdown(
            returns=self._y, w=self._w, alpha=0.05, height=6, width=10, ax=None
        )
        plt.show(block=True)

    def gerar_grafico_histograma(self):
        _ = riskfolio.plot_hist(
            returns=self._y, w=self._w, alpha=0.05, bins=50, height=6, width=10, ax=None
        )
        plt.show(block=True)

    def gerar_grafico_tabela_resumo(self):
        print("========gerar_grafico_tabela_resumo=========")
        print("Retornos")
        pprint.pprint(self._y)
        pprint.pprint(self._portfolio.returns)
        print("=================")
        print("Pesos")
        pprint.pprint(self._w)

        print("=================")

        _ = riskfolio.jupyter_report(
            returns=self._y,
            w=self._w,
            solver="MOSEK",  # , MAR=13 / 100, alpha=0.05, ax=None, t_factor=12
        )
        plt.show(block=True)

    def gerar_grafico_area(self):
        _ = riskfolio.plot_frontier_area(
            w_frontier=self._w_fronteira, cmap="tab20", height=6, width=10, ax=None
        )
        plt.show(block=True)

    def gerar_grafico_contribuicao_risco(self):
        _ = riskfolio.plot_risk_con(
            w=self._w,
            cov=self._portfolio.cov,
            returns=self._portfolio.returns,
            rm=self._rm,
            rf=0,
            alpha=0.05,
            color="tab:blue",
            height=6,
            width=10,
            t_factor=252,
            ax=None,
        )
        plt.show(block=True)


markowitz = Markowitz(
    tickers=["PETR4.SA", "^BVSP", "WEGE3.SA"],
    data_inicial="2023-01-01",
    data_final="2023-01-15",
)
markowitz.buscar_dados()
# markowitz.simular(Objetivo.MIN_RISK.value)
# markowitz.gerar_grafico_fronteira()
# markowitz.gerar_grafico_composicao_carteira()
# markowitz.simular(Objetivo.MAX_RET.value)
# markowitz.gerar_grafico_fronteira()
# markowitz.gerar_grafico_composicao_carteira()
markowitz.simular(Objetivo.SHARPE.value)
markowitz.gerar_grafico_composicao_carteira()
markowitz.gerar_grafico_fronteira()
markowitz.gerar_grafico_area()
markowitz.gerar_grafico_contribuicao_risco()
markowitz.gerar_grafico_historico()
# markowitz.gerar_grafico_histograma()
# markowitz.gerar_grafico_drawdown()
markowitz.gerar_grafico_tabela_resumo()

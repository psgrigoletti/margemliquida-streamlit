import riskfolio
import streamlit as st


class Markowitz:
    def __init__(self):
        self._mu = None
        self._cov = None
        self._returns = None
        self._pesos = None
        self._retornos = None
        self._frontier = None
        self._rf = None

    def simular_minima_variancia(self):
        port = riskfolio.Portfolio(returns=self._retornos)
        method_mu = "hist"
        method_cov = "hist"
        port.assets_stats(method_mu=method_mu, method_cov=method_cov)
        model = "Classic"
        rm = "MV"
        obj = "MinRisk"  # Funcao objetivo, pode ser MinRisk, MaxRet, Utility ou Sharpe
        hist = True
        rf = 0
        l = 0
        self._pesos = port.optimization(
            model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist
        )
        points = 10
        self._frontier = port.efficient_frontier(
            model=model, rm=rm, points=points, rf=rf, hist=hist
        )
        self._mu = port.mu
        self._cov = port.cov
        self._returns = port.returns

    def criar_grafico_fronteira_minima_variancia(self, Y):
        self.simular_minima_variancia()

        fig1 = riskfolio.plot_frontier(
            w_frontier=self._frontier,
            mu=self._mu,
            cov=self._cov,
            returns=self._returns,
            rf=self._rf,
            alpha=0.05,
            cmap="viridis",
            w=self._pesos,
            s=16,
            c="r",
            height=6,
            width=10,
            ax=None,
            t_factor=12,
        )
        return fig1.figure

    def criar_grafico_composicao_carteira_minima_variancia(self, Y):
        self._pesos = self.simular_minima_variancia()

        fig2 = riskfolio.plot_pie(
            w=self._pesos,
            others=0.05,
            nrow=25,
            cmap="tab20",
            height=6,
            width=10,
            ax=None,
        )
        return fig2.figure

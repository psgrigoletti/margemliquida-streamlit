import streamlit as st
import yfinance as yf
import backtrader as bt
import pandas as pd
import backtrader.analyzers as btanal
import backtrader.strategies as btstrats

from st_pages import add_page_title

import matplotlib
matplotlib.use('agg')

# Função que salva imagem


def saveplots(cerebro, numfigs=1, iplot=True, start=None, end=None,
              width=16, height=9, dpi=300, tight=True, use=None, file_path='', **kwargs):

    from backtrader import plot
    if cerebro.p.oldsync:
        plotter = plot.Plot_OldSync(**kwargs)
    else:
        plotter = plot.Plot(**kwargs)

    figs = []
    for stratlist in cerebro.runstrats:
        for si, strat in enumerate(stratlist):
            rfig = plotter.plot(strat, figid=si * 100,
                                numfigs=numfigs, iplot=iplot,
                                start=start, end=end, use=use)
            figs.append(rfig)

    for fig in figs:
        for f in fig:
            f.savefig(file_path, bbox_inches='tight')
    return figs

# Estratégias


estrategias = {}


class MovingAverageCross(bt.Strategy):
    params = (('fast', 50),
              ('slow', 200))

    def __init__(self):
        self.fastma = bt.indicators.SimpleMovingAverage(
            period=self.params.fast)
        self.slowma = bt.indicators.SimpleMovingAverage(
            period=self.params.slow)
        self.crossover = bt.indicators.CrossOver(self.fastma, self.slowma)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.close()


estrategias['MovingAverageCross'] = MovingAverageCross


class TurtleTrading(bt.Strategy):

    params = (('sizing', 0.02),
              ('atr_period', 20),
              ('entry_breakout_period', 55),
              ('exit_breakout_period', 20))

    def __init__(self):
        self.atr = bt.indicators.ATR(period=self.params.atr_period)
        self.entry_breakout = bt.indicators.Highest(
            self.data.high(-self.params.entry_breakout_period), period=self.params.entry_breakout_period)
        self.exit_breakout = bt.indicators.Lowest(
            self.data.low(-self.params.exit_breakout_period), period=self.params.exit_breakout_period)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.entry_breakout[0]:
                self.buy(size=self.broker.get_cash() *
                         self.params.sizing / self.data.close[0])
        else:
            if self.data.close[0] < self.exit_breakout[0]:
                self.close()


estrategias['TurtleTrading'] = TurtleTrading


class MMSCruzamento(bt.SignalStrategy):
    def __init__(self):
        mms = bt.ind.SMA(period=50)
        preco = self.data
        cruzamento = bt.ind.CrossOver(preco, mms)
        self.signal_add(bt.SIGNAL_LONG, cruzamento)


estrategias['MMSCruzamento'] = MMSCruzamento


class RSI(bt.Strategy):

    params = (('period', 14),
              ('upper', 70),
              ('lower', 30))

    def __init__(self):
        self.rsi = bt.indicators.RSI(period=self.params.period)

    def next(self):
        if not self.position:
            if self.rsi < self.params.lower:
                self.buy()
        elif self.rsi > self.params.upper:
            self.close()


estrategias['RSI'] = RSI


class RSI_MMA(bt.Strategy):
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=21)
        self.mm_rapida = bt.indicators.SMA(self.data.close, period=20)
        self.mm_lenta = bt.indicators.SMA(self.data.close, period=100)
        # self.crossup = bt.ind.CrossUp(self.mm_rapida, self.mm_lenta)

    def next(self):
        if not self.position:
            if self.rsi < 40 and self.mm_rapida > self.mm_lenta:
                self.buy(size=1)
        else:
            if self.rsi > 60:
                self.sell(size=1)


estrategias['RSI_MMA'] = RSI_MMA

# Página
st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

col1, col2 = st.columns(2)

with col1:
    ativo = st.text_input("Ticker", value='PETZ3.SA')
    caixa_inicial = st.text_input("Caixa inicial", value=30000)
with col2:
    estrategia = st.selectbox("Estratégia", estrategias.keys())
    comissao = st.text_input("Comissão", value=0.003)

cerebro = bt.Cerebro()
cerebro.addstrategy(estrategias.get(estrategia))

data = bt.feeds.PandasData(dataname=yf.download(ativo, '2020-01-01',
                                                '2023-05-01', auto_adjust=True))
if st.button("Executar"):
    cerebro.adddata(data)
    cerebro.broker.setcommission(commission=float(comissao))
    cerebro.broker.setcash(float(caixa_inicial))
    cerebro.addanalyzer(btanal.PeriodStats, _name='periodsstats',
                        timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanal.SharpeRatio_A, _name='sharperatio')
    cerebro.addanalyzer(btanal.DrawDown, _name='drawdown')
    cerebro.addanalyzer(btanal.TradeAnalyzer, _name='tradeanalyzer')

    resultado = cerebro.run()
    resultados = resultado[0]
    saveplots(cerebro, file_path='example.png')  # run it
    st.markdown("---")

    tab1, tab2 = st.tabs(tabs=['Gráfico', 'Estatísticas'])
    with tab1:
        st.image('example.png', use_column_width=True)
    with tab2:
        st.markdown("Estatísticas (período diário):")
        st.write(resultados.analyzers.periodsstats.get_analysis())
        st.markdown("Sharpe Ratio (período anual):")
        # riskfreerate = 0.01 (default)
        st.write(resultados.analyzers.sharperatio.get_analysis())
        st.markdown("Drawdown (período anual):")
        st.write(resultados.analyzers.drawdown.get_analysis())
        st.markdown("Trade Analyser (período anual):")
        st.write(resultados.analyzers.tradeanalyzer.get_analysis())

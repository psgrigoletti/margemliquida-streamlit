import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import riskfolio as rp
import yfinance as yf

warnings.filterwarnings("ignore")
pd.options.display.float_format = "{:.4%}".format

# Date range
start = "2016-01-01"
end = "2019-12-30"

# Tickers of assets
assets = [
    "JCI",
    "TGT",
    "CMCSA",
    "CPB",
    "MO",
    "APA",
]
assets.sort()

# Downloading data
data = yf.download(assets, start=start, end=end)
data = data.loc[:, ("Adj Close", slice(None))]
data.columns = assets

# Calculating returns
Y = data[assets].pct_change().dropna()


# Building the portfolio object
port = rp.Portfolio(returns=Y)
# Calculating optimal portfolio

# Select method and estimate input parameters:

method_mu = "hist"  # Method to estimate expected returns based on historical data.
method_cov = "hist"  # Method to estimate covariance matrix based on historical data.

port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

# Estimate optimal portfolio:

model = "Classic"  # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
rm = "MV"  # Risk measure used, this time will be variance
obj = "Sharpe"  # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
hist = True  # Use historical scenarios for risk measures that depend on scenarios
rf = 0  # Risk free rate
l = 0  # Risk aversion factor, only useful when obj is 'Utility'

w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)

returns = port.returns

# ax = rp.jupyter_report(
#     returns,
#     w,
#     rm=rm,
#     rf=0,
#     alpha=0.05,
#     others=0.05,
#     nrow=25,
#     height=6,
#     width=14,
#     t_factor=252,
#     ini_days=1,
#     days_per_year=252,
#     bins=50,
# )
# plt.show(block=True)

# import numpy as np
# import pandas as pd
# from riskfolio import EfficientFrontier, plot_drawdown

# Cria uma série de retornos históricos
returns = np.array([0.05, 0.02, 0.07, 0.03, 0.06, 0.04])

# Cria um portfólio eficiente
ef = rp.Portfolio.efficient_frontier(returns, risk_free_rate=0.02)

# Calcula o drawdown do portfólio eficiente
drawdown = ef.calculate_drawdown()

# Plota o gráfico de drawdown
rp.plot_drawdown(drawdown)

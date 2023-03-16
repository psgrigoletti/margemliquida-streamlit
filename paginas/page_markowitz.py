import datetime
import streamlit as st
from st_pages import add_page_title
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import scipy.optimize as sco

## Construção da página
        
st.set_page_config(layout="wide")
add_page_title()
mensagens = st.container()

def portfolio_annualised_performance(pesos, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * pesos) *252
    std = np.sqrt(np.dot(pesos.T, np.dot(cov_matrix, pesos))) * np.sqrt(252)
    return std, returns

def random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate):
    results = np.zeros((3, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(len(acoes))
        weights /= np.sum(weights)
        weights_record.append(weights)
        portfolio_std_dev, portfolio_return = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev
        # TODO: implementar usando o https://www.investopedia.com/terms/s/sortinoratio.asp
        # comparar https://www.codearmo.com/blog/sharpe-sortino-and-calmar-ratios-python
    return results, weights_record

def display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate):
    results, weights = random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate)
    
    max_sharpe_idx = np.argmax(results[2])
    sdp, rp = results[0, max_sharpe_idx], results[1, max_sharpe_idx]
    max_sharpe_allocation = pd.DataFrame(weights[max_sharpe_idx], index=tabela.columns, columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2) for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    
    min_vol_idx = np.argmin(results[0])
    sdp_min, rp_min = results[0, min_vol_idx], results[1, min_vol_idx]
    min_vol_allocation = pd.DataFrame(weights[min_vol_idx], index=tabela.columns, columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2) for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    
    print("-"*80)
    print("Maximum Sharpe Ratio Portfolio Allocation\n")
    print("Annualised Return:", round(rp, 2))
    print("Annualised Volatility:", round(sdp, 2))
    print("\n")
    print(max_sharpe_allocation)
    print("-"*80)
    print("Minimum Volatility Portfolio Allocation\n")
    print("Retorno anual:", round(rp_min,2))
    print("Volatility:", round(sdp_min,2))
    print("\n")
    print(min_vol_allocation)
    
    fig7 = plt.figure(figsize=(25, 15))
    plt.scatter(results[0,:],results[1,:],c=results[2,:],cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar()
    plt.scatter(sdp,rp,marker='*',color='r',s=500, label='Maximum Sharpe ratio')
    plt.scatter(sdp_min,rp_min,marker='*',color='g',s=500, label='Minimum volatility')
    plt.title('Simulated Portfolio Optimization based on Efficient Frontier')
    plt.xlabel('Volatilidade anual')
    plt.ylabel('Retorno anual')
    plt.legend(labelspacing=1)
    return fig7
    
@st.cache_data
def buscar_precos_fechamento(acoes, data_inicial, data_final):
    return yf.download(list(map((lambda x: x + ".SA"), acoes)), start=data_inicial, end=data_final)['Adj Close']

acoes = st.multiselect(
    'Selecione as ações que compõe a carteira:',
    ['TAEE11', 'CPLE6', 'WIZS3', 'ITSA4', 'ABCB4', 'FLRY3', 'OFSA3', 'SAPR11'],
    ['TAEE11', 'CPLE6', 'WIZS3'])

col1, col2, col3, col4 = st.columns([1,1,1,1])
data_inicial = col1.date_input("Data inicial:", datetime.date(2018, 1, 1))
data_final = col2.date_input("Data final:", datetime.datetime.now())
selic = col3.number_input("Selic atual (taxa livre de risco) (percentual):", 13.75)
numero_de_portfolios_aleatorios = col4.number_input("Número de portifólios aleatórios:", 5000)

if st.button("Pesquisar", help="Pesquisar"):
    mensagens.empty()
    tabela = buscar_precos_fechamento(acoes, data_inicial, data_final)
    returns = tabela.pct_change()
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_portfolios = numero_de_portfolios_aleatorios
    risk_free_rate = selic
    
   
    with st.expander("Gráfico de preços:"):
        fig = tabela.plot(figsize=(25, 15), ylabel="Preço", xlabel="Período")
        st.pyplot(fig.figure)
        
    with st.expander("Gráfico normalizado:"):
        normalizado = tabela / tabela.iloc[0]
        fig2 = normalizado.plot(figsize=(25, 15), ylabel="Preço", xlabel="Período")
        st.pyplot(fig2.figure)
        
    with st.expander("Retornos diários:"):
        retornos_diarios = tabela.pct_change() # Percentage change between the current and a prior element.

        fig3 = plt.figure(figsize=(25, 15))
        for c in retornos_diarios.columns.values:
            plt.plot(retornos_diarios.index, retornos_diarios[c], lw=3, alpha=0.8,label=c)
        plt.legend(loc='best', fontsize=14)
        plt.ylabel('Retornos diários')
        st.pyplot(fig3.figure)
    
    with st.expander("Volatilidade e os Retornos Médios:"):
        volatilidade = pd.DataFrame(retornos_diarios.std(), columns=['Volatilidade'])
        retornos_medios = pd.DataFrame(retornos_diarios.mean(), columns=['Retorno'])
        matrix_risco_retorno = pd.concat([retornos_medios, volatilidade], axis = 1)
        #matrix_risco_retorno

        fig4, ax = plt.subplots(figsize = (10, 10))

        sns.scatterplot(data = matrix_risco_retorno, x='Volatilidade', y='Retorno')

        for i in range(matrix_risco_retorno.shape[0]):
            plt.text(x = matrix_risco_retorno.Volatilidade[i], 
                    y=matrix_risco_retorno.Retorno[i], 
                    s=matrix_risco_retorno.index[i], 
                    fontdict = dict(color = 'red', size=20), 
                    bbox=dict(facecolor = 'yellow', edgecolor='black'))
        
        st.pyplot(fig4)
        
    with st.expander("Matriz de Correlação:"):
        tabela_correlacao = tabela.corr()
        mascara_grafico = np.triu(tabela_correlacao)

        fig5 = plt.figure(num=None, figsize=(10, 10), dpi=100, facecolor='w', edgecolor='k')

        res = sns.heatmap(tabela_correlacao, annot=True, vmin=-1, vmax=1, cmap='viridis', linewidths=0.5, mask=mascara_grafico)
        plt.title('Matriz de correlação entre os ativos')
        st.pyplot(fig5)
        
    with st.expander("Risco x Retorno:"):
        fig6 = plt.figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='k')
        res = sns.heatmap(tabela.cov(), annot=True, vmin=-1, vmax=1, cmap='viridis', linewidths=0.5)
        plt.title('Matriz de correlação')
        st.pyplot(fig6)

    with st.expander("Fronteira Eficiente 1:"):
        fig7 = display_simulated_ef_with_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate)
        st.pyplot(fig7)
        
def neg_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate):
    p_var, p_ret = portfolio_annualised_performance(weights, mean_returns, cov_matrix)
    return -(p_ret - risk_free_rate) / p_var

def max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix, risk_free_rate)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0,1.0)
    bounds = tuple(bound for asset in range(num_assets))
    result = sco.minimize(neg_sharpe_ratio, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
    return result

def portfolio_volatility(weights, mean_returns, cov_matrix):
    return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[0]

def min_variance(mean_returns, cov_matrix):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0,1.0)
    bounds = tuple(bound for asset in range(num_assets))

    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)

    return result

def efficient_return(mean_returns, cov_matrix, target):
    num_assets = len(mean_returns)
    args = (mean_returns, cov_matrix)

    def portfolio_return(weights):
        return portfolio_annualised_performance(weights, mean_returns, cov_matrix)[1]

    constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                   {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0,1) for asset in range(num_assets))
    result = sco.minimize(portfolio_volatility, num_assets*[1./num_assets,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
    return result

def efficient_frontier(mean_returns, cov_matrix, returns_range):
    efficients = []
    for ret in returns_range:
        efficients.append(efficient_return(mean_returns, cov_matrix, ret))
    return efficients

def apresentar_fronteira_eficiente_calculada_usando_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate):
    results, _ = random_portfolios(num_portfolios,mean_returns, cov_matrix, risk_free_rate)
    
    max_sharpe = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate)
    sdp, rp = portfolio_annualised_performance(max_sharpe['x'], mean_returns, cov_matrix)
    max_sharpe_allocation = pd.DataFrame(max_sharpe.x,index=tabela.columns,columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    #max_sharpe_allocation

    min_vol = min_variance(mean_returns, cov_matrix)
    sdp_min, rp_min = portfolio_annualised_performance(min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(min_vol.x,index=tabela.columns,columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    
    print("-"*80)
    print("Maximum Sharpe Ratio Portfolio Allocation\n")
    print("Retorno anual:", round(rp,2))
    print("Volatilidade anual:", round(sdp,2))
    print("\n")
    print(max_sharpe_allocation)
    print("-"*80)
    print("Minimum Volatility Portfolio Allocation\n")
    print("Retorno anual:", round(rp_min,2))
    print("Volatidade anual:", round(sdp_min,2))
    print("\n")
    print(min_vol_allocation)
    
    fig8 = plt.figure(figsize=(25, 15))
    plt.scatter(results[0,:],results[1,:],c=results[2,:],cmap='YlGnBu', marker='o', s=10, alpha=0.3)
    plt.colorbar()
    plt.scatter(sdp,rp,marker='*',color='r',s=500, label='Retorno máximo (Maximum Sharpe ratio)', linewidths=5)
    plt.scatter(sdp_min,rp_min,marker='*',color='g',s=500, label='Volatilidade mínima', linewidths=5)

    target = np.linspace(rp_min, 0.32, 50)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)
    plt.plot([p['fun'] for p in efficient_portfolios], target, linestyle='-.', color='black', label='Fronteira eficiente')
    plt.title('Calculated Portfolio Optimization based on Efficient Frontier')
    plt.xlabel('Volatilidade anual')
    plt.ylabel('Retorno anual')
    plt.legend(labelspacing=1)        
    return fig8

with st.expander("Fronteira Eficiente 2:"):
    fig8 = apresentar_fronteira_eficiente_calculada_usando_random(mean_returns, cov_matrix, num_portfolios, risk_free_rate)
    st.pyplot(fig8)
    
def display_ef_with_selected(mean_returns, cov_matrix, risk_free_rate):
    max_sharpe = max_sharpe_ratio(mean_returns, cov_matrix, risk_free_rate)
    sdp, rp = portfolio_annualised_performance(max_sharpe['x'], mean_returns, cov_matrix)
    max_sharpe_allocation = pd.DataFrame(max_sharpe.x,index=tabela.columns,columns=['allocation'])
    max_sharpe_allocation.allocation = [round(i*100,2)for i in max_sharpe_allocation.allocation]
    max_sharpe_allocation = max_sharpe_allocation.T
    #max_sharpe_allocation

    min_vol = min_variance(mean_returns, cov_matrix)
    sdp_min, rp_min = portfolio_annualised_performance(min_vol['x'], mean_returns, cov_matrix)
    min_vol_allocation = pd.DataFrame(min_vol.x,index=tabela.columns,columns=['allocation'])
    min_vol_allocation.allocation = [round(i*100,2)for i in min_vol_allocation.allocation]
    min_vol_allocation = min_vol_allocation.T
    
    an_vol = np.std(retornos_diarios) * np.sqrt(252)
    an_rt = mean_returns * 252
    
    retorno_textual = "-" * 80
    retorno_textual+= "\nMaximum Sharpe Ratio Portfolio Allocation"
    retorno_textual+= "\nAnnualised Return:" + str(round(rp,2))
    retorno_textual+= "\nAnnualised Volatility: " + str(round(sdp,2))
    retorno_textual+= "\n"
    retorno_textual+= str(max_sharpe_allocation) + "\n"
    retorno_textual+= "-" * 80
    retorno_textual+= "\nMinimum Volatility Portfolio Allocation"
    retorno_textual+= "\nAnnualised Return: " + str(round(rp_min,2))
    retorno_textual+= "\nAnnualised Volatility: " + str(round(sdp_min,2))
    retorno_textual+= "\n"
    retorno_textual+= str(min_vol_allocation) + "\n"
    retorno_textual+= "-" * 80 
    retorno_textual+= "\nIndividual Stock Returns and Volatility\n"
    for i, txt in enumerate(tabela.columns):
        retorno_textual+= "[" + str(txt) + "]: annuaised return: " + str(round(an_rt[i],2)) +", annualised volatility: " + str(round(an_vol[i],2)) +  "\n"
    retorno_textual+= "-" * 80
    
    st.text(retorno_textual)
    
    fig9, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(an_vol,an_rt,marker='o',s=200)

    for i, txt in enumerate(tabela.columns):
        ax.annotate(txt, (an_vol[i],an_rt[i]), xytext=(10,0), textcoords='offset points')
    ax.scatter(sdp,rp,marker='*',color='r',s=500, label='Maximum Sharpe ratio')
    ax.scatter(sdp_min,rp_min,marker='*',color='g',s=500, label='Minimum volatility')

    target = np.linspace(rp_min, 0.34, 50)
    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)
    ax.plot([p['fun'] for p in efficient_portfolios], target, linestyle='-.', color='black', label='efficient frontier')
    ax.set_title('Portfolio Optimization with Individual Stocks')
    ax.set_xlabel('annualised volatility')
    ax.set_ylabel('annualised returns')
    ax.legend(labelspacing=0.8)
    return fig9
    
with st.expander("Otimização de Carteira:"):
    fig9 = display_ef_with_selected(mean_returns, cov_matrix, risk_free_rate)
    st.pyplot(fig9)
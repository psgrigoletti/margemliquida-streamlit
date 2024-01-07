import logging
from datetime import date

import pandas as pd
import streamlit as st
import yfinance as yf

# import plotly.graph_objects as go


@st.cache_data(show_spinner="Carregando dados...", ttl=60 * 5)
def buscar_panorama(tickers, df_info):
    count = 0
    for ticker in tickers:
        cotacoes = yf.download(ticker, period="5d")["Adj Close"]
        variacao = ((cotacoes.iloc[-1] / cotacoes.iloc[-2]) - 1) * 100
        df_info["Ult. Valor"][count] = round(cotacoes.iloc[-1], 2)
        df_info["%"][count] = round(variacao, 2)
        count += 1
    return df_info


@st.cache_data(show_spinner="Carregando dados...", ttl=60 * 5)
def buscar_dados_intraday(dict_tickers, indice):
    logging.log(logging.DEBUG, "Buscando dados intraday...")
    ticker_diario = yf.download(
        dict_tickers.get(indice)["ticker"], period="1d", interval="5m"
    )
    return ticker_diario


def gerar_descricao(dict_tickers, df_info, numero_item):
    hint = dict_tickers.get(df_info["Ativo"][numero_item])["descricao"]
    nome = df_info["Ativo"][numero_item].replace("$", "\$")
    codigo_yf = dict_tickers.get(df_info["Ativo"][numero_item])["ticker"]

    return (
        "**["
        + nome
        + "]"
        + f'(https://br.financas.yahoo.com/quote/{codigo_yf}?p={codigo_yf}, "'
        + hint
        + '")**'
    )


def gerar_valor(dict_tickers, df_info, numero_item):
    valor = df_info["Ult. Valor"][numero_item]
    valor_br = str(valor).replace(",", "").replace(".", ",")

    return str(valor_br) + dict_tickers.get(df_info["Ativo"][numero_item])["texto_pos"]


def main():
    st.title(":coffee: Panorama de Mercado")
    st.write(
        "**Fonte**: https://finance.yahoo.com/ via [yfinance](https://pypi.org/project/yfinance/)"
    )
    mensagens = st.container()

    if st.button("Carregar dados..."):
        st.subheader("Cotações pelo Mundo em " + date.today().strftime("%d/%m/%Y"))
        st.write(
            "Observação: atraso de 15 minutos, dados do [Yahoo Finanças](https://br.financas.yahoo.com/). Fechamento do dia anterior comparado com cotação atual."
        )

        dict_tickers = {
            "Bovespa": {
                "ticker": "^BVSP",
                "texto_pos": " pontos",
                "descricao": "O índice Bovespa, também conhecido como Ibovespa, é o principal índice de ações da bolsa de valores brasileira, a B3 (Brasil, Bolsa, Balcão). A unidade de medida do Ibovespa é em pontos. Ele é calculado a partir do desempenho das ações mais negociadas na B3, ponderado pelo valor de mercado das empresas. O Ibovespa é uma referência importante para o mercado financeiro brasileiro e é utilizado como indicador do desempenho médio das ações negociadas na bolsa.",
            },
            # "IFIX": {'ticker': "^IFIX", 'texto_pos': ' pontos', 'descricao': "IFIX é um índice de desempenho que representa o desempenho médio dos fundos imobiliários negociados na bolsa de valores brasileira, a B3. O nome \"IFIX\" é uma sigla que significa \"Índice de Fundos Imobiliários\". O índice é calculado pela própria B3 e é composto por uma carteira teórica de fundos imobiliários listados na bolsa."},
            "S&P500": {
                "ticker": "^GSPC",
                "texto_pos": " pontos",
                "descricao": "O S&P 500 é um índice de ações das 500 maiores empresas negociadas nas bolsas de valores dos Estados Unidos, selecionadas com base em sua capitalização de mercado, liquidez e representatividade setorial. A unidade de medida do S&P 500 é em pontos. O índice é calculado com base na soma dos valores de mercado das ações das 500 empresas componentes, ponderados pelo seu peso relativo no índice. O S&P 500 é um dos principais indicadores do mercado financeiro dos Estados Unidos e é amplamente utilizado como referência para o desempenho do mercado de ações americano.",
            },
            "NASDAQ": {
                "ticker": "^IXIC",
                "texto_pos": " pontos",
                "descricao": "A NASDAQ é uma bolsa de valores eletrônica dos Estados Unidos, onde são negociadas ações de empresas de tecnologia e outras indústrias relacionadas. A NASDAQ também possui vários índices de ações, o mais conhecido dos quais é o NASDAQ Composite, que inclui todas as empresas listadas na bolsa. A unidade de medida do NASDAQ Composite é em pontos, calculados com base no valor de mercado de todas as ações incluídas no índice. Além do NASDAQ Composite, a NASDAQ também possui outros índices, como o NASDAQ 100, que inclui as 100 maiores empresas não financeiras listadas na bolsa.",
            },
            "DAX": {
                "ticker": "^GDAXI",
                "texto_pos": " pontos",
                "descricao": "O DAX é o principal índice de ações da bolsa de valores da Alemanha, a Frankfurt Stock Exchange (FSE). A unidade de medida do DAX é em pontos. Ele é calculado com base no desempenho das 30 maiores empresas listadas na FSE, ponderadas pelo valor de mercado das empresas. O DAX é um dos principais indicadores do mercado financeiro europeu e é frequentemente utilizado como uma referência para o desempenho das ações alemãs. O índice é considerado um barômetro importante para a economia alemã e é acompanhado de perto por investidores em todo o mundo.",
            },
            "Nikkei 225": {
                "ticker": "^N225",
                "texto_pos": " pontos",
                "descricao": "A Nikkei 225 é o principal índice de ações da bolsa de valores do Japão, a Tokyo Stock Exchange (TSE). A unidade de medida da Nikkei 225 é em pontos. Ele é calculado com base no desempenho das 225 empresas listadas na TSE, ponderadas pelo preço de suas ações. A Nikkei 225 é considerada um dos principais indicadores do mercado financeiro japonês e é amplamente acompanhada por investidores em todo o mundo. A composição do índice inclui empresas de diversos setores da economia, como eletrônicos, automóveis, finanças e telecomunicações, entre outros.",
            },
            "FTSE 100": {
                "ticker": "^FTSE",
                "texto_pos": " pontos",
                "descricao": "A FTSE 100 é o principal índice de ações da bolsa de valores do Reino Unido, a London Stock Exchange (LSE). A unidade de medida da FTSE 100 é em pontos. Ele é calculado com base no desempenho das 100 maiores empresas listadas na LSE, ponderadas pelo valor de mercado das empresas. A FTSE 100 é frequentemente considerada como um indicador do desempenho da economia britânica e é amplamente acompanhada por investidores em todo o mundo. A composição do índice inclui empresas de diversos setores, como finanças, energia, mineração, farmacêutico, entre outros. O FTSE 100 é um dos principais índices de ações europeus e é considerado um dos principais índices de referência para investidores que desejam acompanhar o mercado de ações do Reino Unido.",
            },
            "PETRÓLEO CRU": {
                "ticker": "CL=F",
                "texto_pos": " USD/BBL",
                "descricao": "O Petróleo Cru, também conhecido como WTI (West Texas Intermediate) ou Brent, é uma commodity negociada nos mercados financeiros internacionais. A unidade de medida do Petróleo Cru é em dólares americanos por barril (bbl). O preço do petróleo é influenciado por diversos fatores, como a oferta e a demanda global, a produção de petróleo dos países produtores, a política dos países exportadores, as condições climáticas, entre outros. O preço do petróleo é um dos indicadores mais importantes da economia global, já que o petróleo é uma das commodities mais amplamente utilizadas em todo o mundo, seja para a produção de energia, combustíveis, plásticos, entre outros produtos.",
            },
            "OURO": {
                "ticker": "GC=F",
                "texto_pos": " ",
                "descricao": "O ouro é uma commodity negociada nos mercados financeiros internacionais, e a unidade de medida padrão do ouro é a onça troy (oz t), que equivale a cerca de 31,1 gramas. O preço do ouro é influenciado por diversos fatores, como a demanda global por joias, a estabilidade política e econômica dos países, as condições do mercado financeiro global, a inflação, entre outros. O ouro é considerado uma reserva de valor, sendo muitas vezes utilizado como uma forma de proteger o patrimônio em tempos de instabilidade econômica ou política. O preço do ouro é um dos indicadores mais importantes dos mercados financeiros globais, e é amplamente acompanhado por investidores em todo o mundo.",
            },
            "Bitcoin USD": {
                "ticker": "BTC-USD",
                "texto_pos": " USD",
                "descricao": "O Bitcoin é uma criptomoeda negociada nos mercados financeiros internacionais e a unidade de medida padrão do preço do Bitcoin é em dólares americanos (USD) por unidade. O preço do Bitcoin é altamente volátil e é influenciado por diversos fatores, como a oferta e a demanda dos investidores, a adoção global da criptomoeda, as regulamentações governamentais, a confiança do mercado, entre outros. O Bitcoin é uma forma de ativo digital que permite transações financeiras sem a necessidade de intermediários, como bancos ou governos, e é considerado por muitos como uma alternativa ao sistema financeiro tradicional.",
            },
            "Ethereum USD": {
                "ticker": "ETH-USD",
                "texto_pos": " USD",
                "descricao": "O Ethereum é uma criptomoeda negociada nos mercados financeiros internacionais, e a unidade de medida padrão do preço do Ethereum é em dólares americanos (USD) por unidade. O preço do Ethereum é altamente volátil e é influenciado por diversos fatores, como a oferta e a demanda dos investidores, a adoção global da criptomoeda, as regulamentações governamentais, a confiança do mercado, entre outros. O Ethereum é uma plataforma blockchain descentralizada que permite a criação de aplicativos descentralizados e contratos inteligentes. A criptomoeda é utilizada para pagar pelos serviços na rede Ethereum, incluindo taxas de transação e remuneração para os mineradores. ",
            },
            "Binance USD": {
                "ticker": "BNB-USD",
                "texto_pos": " USD",
                "descricao": "BNB-USD é o par de negociação que representa a taxa de câmbio entre a criptomoeda Binance Coin (BNB) e o dólar americano (USD). O Binance Coin é uma criptomoeda desenvolvida pela exchange de criptomoedas Binance, que pode ser usada para pagar taxas de negociação na plataforma e para participar de campanhas e projetos lançados pela exchange.",
            },
            "EURO/R$": {
                "ticker": "EURBRL=X",
                "texto_pos": " R$",
                "descricao": "Euro/R$ é o par de moedas que representa a taxa de câmbio entre o euro e o real brasileiro. A unidade de medida padrão para o par de moedas Euro/R$ é o valor do euro em reais. Ou seja, se a taxa de câmbio do Euro/R$ for 6,00, significa que um euro vale 6 reais. ",
            },
            "USD/R$": {
                "ticker": "USDBRL=X",
                "texto_pos": " R$",
                "descricao": "USD/R$ é o par de moedas que representa a taxa de câmbio entre o dólar americano e o real brasileiro. A unidade de medida padrão para o par de moedas USD/R$ é o valor do dólar em reais. Ou seja, se a taxa de câmbio do USD/R$ for 5,00, significa que um dólar vale 5 reais.",
            },
            "CAD/R$": {
                "ticker": "CADBRL=X",
                "texto_pos": " R$",
                "descricao": "CAD/R$ é o par de moedas que representa a taxa de câmbio entre o dólar canadense e o real brasileiro. A unidade de medida padrão para o par de moedas CAD/R$ é o valor do dólar canadense em reais. Ou seja, se a taxa de câmbio do CAD/R$ for 4,00, significa que um dólar canadense vale 4 reais.",
            },
        }

        ativos = dict_tickers.keys()
        tickers = list(map(lambda item: item["ticker"], dict_tickers.values()))

        df_info = pd.DataFrame({"Ativo": ativos, "Ticker": tickers})
        df_info["Ult. Valor"] = ""
        df_info["%"] = ""

        df_info = buscar_panorama(tickers, df_info)

        colunas = [col1, col2, col3, col4] = st.columns(4)

        numero_item = 0
        for c in colunas:
            with c:
                for linha in [0, 1, 2, 3]:
                    if numero_item < len(tickers):
                        descricao = gerar_descricao(dict_tickers, df_info, numero_item)
                        valor = gerar_valor(dict_tickers, df_info, numero_item)
                        variacao = str(df_info["%"][numero_item]) + "%"

                        st.metric(descricao, valor, delta=variacao)
                        numero_item += 1

        # st.markdown("---")
        # st.subheader("Gráfico diário (5 minutos)")

        # col4, _, _ = st.columns(3)

        # indice = col4.selectbox("Selecione", ativos)
        # ticker_diario = buscar_dados_intraday(dict_tickers, indice)

        # fig = go.Figure(data=[go.Candlestick(x=ticker_diario.index, open=ticker_diario['Open'],
        #                 high=ticker_diario['High'], close=ticker_diario['Close'], low=ticker_diario['Low'])])
        # fig.update_layout(title=indice, xaxis_rangeslider_visible=False)
        # st.plotly_chart(fig, use_container_width=True)

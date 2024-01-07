""" Módulo que tenta abstrair um pouco o acesso aos
    dados da Carteira Global.
"""
import logging

import pandas as pd
import requests


class CarteiraGlobal:
    """Classe que tenta abstrair um pouco o acesso aos
    dados da Carteira Global."""

    def __init__(self):
        logging.log(logging.INFO, "Inicializando CarteiraGlobal")
        self.token = None
        self.headers = None
        self.timeout = 10

    def setar_token(self, token: str):
        """Configura o token"""
        self.token = token
        self.headers = {"x-api-key": token}

    def setar_timeout(self, timeout: int):
        """Configura o timeout das requisições"""
        self.timeout = timeout

    def _fazer_requisicao(self, url: str) -> str:
        req = requests.get(url, headers=self.headers, timeout=self.timeout)
        return req.json()

    def retornar_lista_fundos(self) -> pd.DataFrame:
        """Retorna um dataframe com fundos"""
        url = "https://api.carteiraglobal.com/funds"
        response = self._fazer_requisicao(url)
        df = pd.DataFrame(response)
        return df

    def retornar_lista_indices(self):
        """Retorna um dataframe com índices"""
        url = "https://api.carteiraglobal.com/index"
        response = self._fazer_requisicao(url)
        df = pd.DataFrame(response)
        return df

    def retonar_dados_indice(self, identificador, data_inicial, data_final):
        """Retorna um dataframe com dados de um índice"""
        url = f"https://api.carteiraglobal.com/index/{identificador}/report?init_date={data_inicial}&end_date={data_final}"
        response = self._fazer_requisicao(url)
        df = pd.DataFrame(response)
        df.rename(columns={"date_report": "Date"}, inplace=True)
        df["Date"] = pd.to_datetime(df["Date"] + " 00:00:00")
        df = df.set_index("Date", drop=True)
        df.drop(["index"], axis=1, inplace=True)
        df.rename(columns={"quote_value": "Close"}, inplace=True)
        df["Close"] = df["Close"].astype(float)
        return df

    def retornar_lista_fiis(self):
        """Retorna um dataframe com FIIs"""
        url = "https://api.carteiraglobal.com/equity/fiis"
        response = self._fazer_requisicao(url)
        df = pd.DataFrame(response)
        df["ticker-nome"] = df["ticker"].str[:] + " - " + df["name"].str[:]
        tickers = df["ticker"].tolist()
        tickers = [t for t in tickers if "11" in t]
        tickers = [t for t in tickers if not t[-1].isalpha()]
        tickers.sort()
        return tickers

    def retornar_lista_acoes(self):
        """Retorna um dataframe com ações"""
        url = "https://api.carteiraglobal.com/equity/stocks"
        response = self._fazer_requisicao(url)
        df = pd.DataFrame(response)
        rows = df["rows"]
        # rows = df[df['rows']]
        tickers = [r["ticker"] for r in rows]  #  + " - " + r['name']
        # tickers = [t for t in tickers if len(t) <= 6]
        # tickers = [t for t in tickers if not t[-1].isalpha()]
        tickers.sort()
        # df['ticker-nome'] = df['ticker'].str[:] + " - " + df['name'].str[:]
        return tickers

    def retonar_cotacoes_fechamento(self, tickers, data_inicial, data_final):
        df = None

        for t in tickers:
            try:
                t_sem_sa = t.replace(".SA", "").upper()
                retorno = self.retornar_cotacoes(t_sem_sa, data_inicial, data_final)
                retorno.rename(columns={"Close": t_sem_sa}, inplace=True)
                retorno = retorno[t_sem_sa]
                if df is not None:
                    df = df.merge(
                        retorno,
                        left_index=True,
                        right_index=True,
                        how="outer",
                    )
                else:
                    df = pd.DataFrame(retorno)
            except:
                logging.log(logging.ERROR, f"Erro ao buscar cotações de {t_sem_sa}")

        if df is not None:
            df.ffill(inplace=True)
        return df

    def retonar_dados_fiis(self, ticker):
        logging.log(logging.INFO, "Executando retonar_dados_fiis")
        url = f"https://api.carteiraglobal.com/equity/fiis/{ticker}"
        req = requests.get(url, headers=self.headers)
        if req.status_code == 200:
            response = req.json()
            logging.log(logging.INFO, "Resposta retonar_dados_fiis:")
            logging.log(logging.INFO, response)
            return response
            # df = pd.DataFrame(response)
            # return df
        else:
            logging.log(
                logging.INFO, "Resposta diferente de HTTP 200: " + str(req.status_code)
            )
            raise Exception("Resposta diferente de HTTP 200: " + str(req.status_code))

    def retonar_dados_acoes(self, ticker):
        logging.log(logging.INFO, "Executando retonar_dados_acoes")
        url = f"https://api.carteiraglobal.com/equity/stocks/{ticker}"
        req = requests.get(url, headers=self.headers)
        if req.status_code == 200:
            response = req.json()
            logging.log(logging.INFO, "Resposta retonar_dados_acoes:")
            logging.log(logging.INFO, response)
            return response
            # df = pd.DataFrame(response)
            # return df
        else:
            logging.log(
                logging.INFO, "Resposta diferente de HTTP 200: " + str(req.status_code)
            )
            raise Exception("Resposta diferente de HTTP 200: " + str(req.status_code))

    def retornar_cotacoes(self, ticker, data_inicial, data_final):
        t_sem_sa = ticker.replace(".SA", "").upper()
        url = f"https://api.carteiraglobal.com/equity/{t_sem_sa}/report?init_date={data_inicial}&end_date={data_final}"
        req = requests.get(url, headers=self.headers)
        response = req.json()
        print(f"Buscando cotações de {ticker} (fonte: Carteira Global)")
        cotacoes = pd.DataFrame(response)
        cotacoes = cotacoes[
            [
                "date_report",
                "open_quote_value",
                "max_quote_value",
                "min_quote_value",
                "quote_value",
                "volume",
            ]
        ]
        cotacoes.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
        cotacoes["Date"] = pd.to_datetime(cotacoes["Date"])
        cotacoes = cotacoes.set_index("Date", drop=False)
        cotacoes.dropna(inplace=True)
        return cotacoes

    def retornar_dividendos(
        self, ticker: str, data_inicial: str, data_final, buscar_dy=True
    ):
        """Retorna um dataframe com os dividendos de um ticker"""

        url = f"https://api.carteiraglobal.com/equity/{ticker}/event?init_date={data_inicial}&end_date={data_final}"
        response = self._fazer_requisicao(url)
        div = pd.DataFrame(response)
        div = div[
            (div["event_type_name"] == "Dividendo")
            | (div["event_type_name"] == "Juros sobre Capital Próprio")
        ]
        div = div[["date_com", "date_pmt", "quote_value"]]
        div.columns = ["Data base", "Data pagamento", "Dividends"]
        div["Data base"] = pd.to_datetime(div["Data base"])
        div = div.set_index("Data base", drop=False)
        if buscar_dy:
            div["Close"] = self.retornar_cotacoes(ticker, data_inicial, data_final)[
                "Close"
            ]
            div["DY"] = (div["Dividends"] / div["Close"]) * 100.0
        div.dropna(inplace=True)
        return div

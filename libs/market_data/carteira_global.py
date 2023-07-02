import pandas as pd
import requests
import logging

class CarteiraGlobal:
    token = None
    headers = None
    
    def __init__(self):
        logging.log(logging.INFO, "Inicializando objeto da classe CarteiraGlobal")
    
    def setar_token(self, token):
        self.token = token
        self.headers = {'x-api-key': token}
        
    def retornar_lista_fiis(self):
        url = f"https://api.carteiraglobal.com/equity/fiis"
        req = requests.get(url, headers = self.headers)
        response = req.json()
        df = pd.DataFrame(response)
        df['ticker-nome'] = df['ticker'].str[:] + " - " + df['name'].str[:]
        tickers = df['ticker'].tolist()
        tickers = [t for t in tickers if '11' in t]
        tickers = [t for t in tickers if not t[-1].isalpha()]
        tickers.sort()
        return tickers

    def retornar_lista_acoes(self):
        url = f"https://api.carteiraglobal.com/equity/stocks"
        req = requests.get(url, headers = self.headers)
        response = req.json()
        df = pd.DataFrame(response)
        rows = df['rows']
        #rows = df[df['rows']]
        tickers = [r['ticker'] for r in rows] #  + " - " + r['name']
        #tickers = [t for t in tickers if len(t) <= 6]
        #tickers = [t for t in tickers if not t[-1].isalpha()]
        tickers.sort()
        #df['ticker-nome'] = df['ticker'].str[:] + " - " + df['name'].str[:]
        print(tickers)
        return tickers
        
    def retonar_dados_fiis(self, ticker):
        logging.log(logging.INFO, "Executando retonar_dados_fiis")
        url = f"https://api.carteiraglobal.com/equity/fiis/{ticker}"
        req = requests.get(url, headers = self.headers)
        if req.status_code == 200:        
            response = req.json()
            logging.log(logging.INFO, "Resposta retonar_dados_fiis:")
            logging.log(logging.INFO, response)                
            return response
            # df = pd.DataFrame(response)
            # return df
        else:
            logging.log(logging.INFO, "Resposta diferente de HTTP 200: " + str(req.status_code))
            raise Exception("Resposta diferente de HTTP 200: " + str(req.status_code)) 
                
    def retonar_dados_acoes(self, ticker):
        logging.log(logging.INFO, "Executando retonar_dados_acoes")        
        url = f"https://api.carteiraglobal.com/equity/stocks/{ticker}"
        req = requests.get(url, headers = self.headers)
        if req.status_code == 200:
            response = req.json()
            logging.log(logging.INFO, "Resposta retonar_dados_acoes:")                
            logging.log(logging.INFO, response)                
            return response
            # df = pd.DataFrame(response)
            # return df    
        else:
            logging.log(logging.INFO, "Resposta diferente de HTTP 200: " + str(req.status_code))            
            raise Exception("Resposta diferente de HTTP 200: " + str(req.status_code)) 
            
    
    def retornar_cotacoes(self, ticker, data_inicial, data_final):
        url = f"https://api.carteiraglobal.com/equity/{ticker}/report?init_date={data_inicial}&end_date={data_final}"
        req = requests.get(url, headers = self.headers)
        response = req.json()
        cotacoes = pd.DataFrame(response)
        cotacoes = cotacoes[['date_report', 'open_quote_value', 'max_quote_value', 'min_quote_value', 'quote_value', 'volume']]
        cotacoes.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        cotacoes['Date'] = pd.to_datetime(cotacoes['Date'])        
        cotacoes = cotacoes.set_index('Date', drop = False)
        cotacoes.dropna(inplace=True)
        return cotacoes    

    def retornar_dividendos(self, ticker, data_inicial, data_final, buscar_dy=True):
        url = f"https://api.carteiraglobal.com/equity/{ticker}/event?init_date={data_inicial}&end_date={data_final}"
        req = requests.get(url, headers = self.headers)
        response = req.json()
        dividendos = pd.DataFrame(response)
        dividendos = dividendos[(dividendos["event_type_name"] == "Dividendo") | 
                                (dividendos["event_type_name"] == "Juros sobre Capital Próprio")]
        dividendos = dividendos[['date_com', 'date_pmt', 'quote_value']]
        dividendos.columns = ['Data base', 'Data pagamento', 'Dividends']
        dividendos['Data base'] = pd.to_datetime(dividendos['Data base'])
        dividendos = dividendos.set_index('Data base', drop = False)
        if buscar_dy:
            dividendos['Close'] = self.retornar_cotacoes(ticker, data_inicial, data_final)['Close']
            dividendos['DY'] = (dividendos['Dividends']/dividendos['Close'])*100.0
        dividendos.dropna(inplace=True)
        return dividendos
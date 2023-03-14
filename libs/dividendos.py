# import yfinance as yf
# import locale
import logging
import plotly.graph_objects as go
from datetime import date
from .carteira_global import CarteiraGlobal

class Dividendos:
    chave_carteira_global = None
    
    MONTHS = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5 : 'Mai', 6: 'Jun',
              7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
    
    FULL_MONTHS = {1: '01-Janeiro', 2: '02-Fevereiro', 3: '03-Março', 4: '04-Abril', 5 : '05-Maio', 6: '06-Junho',
                   7: '07-Julho', 8: '08-Agosto', 9: '09-Setembro', 10: '10-Outubro', 11: '11-Novembro', 12: '12-Dezembro'}

    def __init__(self):
        logging.log(logging.INFO, "Inicializando objeto da classe Dividendos")
        # locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    
    def setar_chave_carteira_global(self, chave_carteira_global):
        self.chave_carteira_global = chave_carteira_global
   
    def retornar_dados(self, ticker, data_inicial, data_final):
        #papel = yf.Ticker(ticker + ".SA")
        #historico = papel.history(start = data_inicial, end = data_final)[['Dividends', 'Close']]
        
        cg = CarteiraGlobal()
        cg.setar_token(self.chave_carteira_global)
        historico = cg.retornar_dividendos(ticker, data_inicial, data_final) 
        historico = historico[historico['Dividends'] != 0]

        historico["Mês"] = historico.index.month
        historico["Ano"] = historico.index.year
        historico["AnoMês"] = historico.index.year.astype(str) + "-" + historico.index.month.astype(str)      
        historico['NomeMês'] = historico['Mês'].apply(lambda x: self.FULL_MONTHS[x])
        historico["SomaDividendos"] = historico['Dividends'].rolling('365D').sum()
        #historico['DividendYield'] = round((historico["SomaDividendos"] / historico["Close"]) * 100.0, 2)
        return historico
    
    def retornar_grafico_tendencia(self, ticker, df):
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=df.index,
                            y=df["Dividends"],
                            name="Dividendo (R$)",
                            texttemplate = "R$ %{value:.2f}",
                            hovertemplate = "<b>" + ticker + "</b><br>Data: %{x}<br>" + "Dividendo" + ": " + "R$ " + " %{y:.2f}",
                            # textposition="inside",
                            # textangle=0,
                            textfont={'family': "Arial", 'size': 15, 'color': "Black"},
                            ))

        fig.add_trace(go.Scatter(x=df.index,
                            y=df["DY"],
                            name="Dividend Yield (%)", #text=df_anual[c], 
                            texttemplate = "%{value:.2f}%",
                            hovertemplate = "<b>" + ticker + "</b><br>Data: %{x}<br>" + "DY" + ": " + " %{y:.2f}%",
                            # textposition="inside",
                            # textangle=0,
                            textfont={'family': "Arial", 'size': 15, 'color': "Black"},
                            ))

        fig.update_layout(
            xaxis_title="Data",
            legend_title="Tipo:",    
            title={'text': '<b>' + ticker + " - Tendência dos Dividendos e Dividend Yield",
                'y':0.9, 'x':0.5,
                'xanchor': 'center', 'yanchor': 'top'},
            legend=dict(x=0, y=-0.5),
            barmode='group',
            bargap=0.2, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1) # gap between bars of the same location coordinate.

        # Pega a data em que o gráfico foi gerado
        today = date.today().strftime('%d/%m/%Y')

        fig.add_annotation(x=1, y=0, 
                        text=f"Fonte dos dados: https://api.carteiraglobal.com/ <br>Data da geração: {today}", showarrow=False,
                        xref='paper', yref='paper', 
                        xshift=0, yshift=-110, font=dict(size=12, color="grey"), align="left")

        return fig        
        
        
    def retornar_grafico_evolucao(self, ticker, df):
        fig = go.Figure()

        fig.add_trace(go.Bar(x=df.index,
                            y=df["Dividends"],
                            name="Dividendo (R$)",
                            texttemplate = "R$ %{value:.2f}",
                            hovertemplate = "<b>" + ticker + "</b><br>Data: %{x}<br>" + "Dividendo" + ": " + "R$ " + " %{y:.2f} ",
                            textposition="inside",
                            textangle=0,
                            textfont={'family': "Arial", 'size': 15, 'color': "Black"},
                            ))

        fig.add_trace(go.Bar(x=df.index,
                            y=df["DY"],
                            name="Dividend Yield (%)", #text=df_anual[c], 
                            texttemplate = "%{value:.2f}%",
                            hovertemplate = "<b>" + ticker + "</b><br>Data: %{x}<br>" + "DY" + ": " + " %{y:.2f}%",
                            textposition="inside",
                            textangle=0,
                            textfont={'family': "Arial", 'size': 15, 'color': "Black"},
                            ))

        fig.update_layout(
            xaxis_title="Data",
            legend_title="Tipo:",    
            title={'text': '<b>' + ticker + " - Evolução dos Dividendos e Dividend Yield",
                'y':0.9, 'x':0.5,
                'xanchor': 'center', 'yanchor': 'top'},
            legend=dict(x=0, y=-0.5),
            barmode='group',
            bargap=0.2, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1) # gap between bars of the same location coordinate.

        # Pega a data em que o gráfico foi gerado
        today = date.today().strftime('%d/%m/%Y')

        fig.add_annotation(x=1, y=0, 
                        text=f"Fonte dos dados: https://api.carteiraglobal.com/ <br>Data da geração: {today}", showarrow=False,
                        xref='paper', yref='paper', 
                        xshift=0, yshift=-110, font=dict(size=12, color="grey"), align="left")

        return fig
    
    def retornar_grafico_anual(self, ticker, df):
        df = df.groupby(['Ano'])[['Dividends']].sum(numeric_only=True)
        fig = go.Figure()

        fig.add_trace(go.Bar(x=df.index,
                             y=df["Dividends"],
                             name="Dividendo (R$)",
                             texttemplate = "R$ %{value:.2f}",
                             hovertemplate = "<b>" + ticker + "</b><br>Ano: %{label}<br>" + "Dividendo" + ": " + "R$ " + "%{y:.2f} ",
                             textposition="inside",
                             textangle=0,
                             textfont={'family': "Arial", 'size': 15, 'color': "Black"}))

        fig.update_xaxes(tickvals=df.index) 

        fig.update_layout(
            xaxis = {
                'title': "Ano",
            },
            title={'text': '<b>' + ticker + " - Dividendos pagos por ano",
                'y':0.9, 'x':0.5,
                'xanchor': 'center', 'yanchor': 'top'})
        
        # Pega a data em que o gráfico foi gerado
        today = date.today().strftime('%d/%m/%Y')

        fig.add_annotation(x=1, y=0, 
                        text=f"Fonte dos dados: https://api.carteiraglobal.com/ <br>Data da geração: {today}", showarrow=False,
                        xref='paper', yref='paper', 
                        xshift=0, yshift=-110, font=dict(size=12, color="grey"), align="left")

        return fig
    
    def retornar_grafico_mensal(self, ticker, df):
        df = df.groupby(['NomeMês'])[['Dividends']].sum(numeric_only=True)
        fig = go.Figure()

        fig.add_trace(go.Bar(x=df.index,
                            y=df["Dividends"],
                            name="Dividendo (R$)",
                            texttemplate = "R$ %{value:.2f}",
                            hovertemplate = "<b>" + ticker + "</b><br>Mês: %{label}<br>" + "Dividendo" + ": " + "R$ " + "%{y:.2f} ",
                            textposition="inside",
                            textangle=0,
                            textfont={'family': "Arial", 'size': 15, 'color': "Black"},
                            ))

        fig.update_xaxes(tickvals=df.index) 

        fig.update_layout(
            xaxis = {
                'title': "Mês",
            },
            title={'text': '<b>' + ticker + " - Dividendos pagos por mês",
                'y':0.9, 'x':0.5,
                'xanchor': 'center', 'yanchor': 'top'})
        
        # Pega a data em que o gráfico foi gerado
        today = date.today().strftime('%d/%m/%Y')

        fig.add_annotation(x=1, y=0, 
                        text=f"Fonte dos dados: https://api.carteiraglobal.com/ <br>Data da geração: {today}", showarrow=False,
                        xref='paper', yref='paper', 
                        xshift=0, yshift=-110, font=dict(size=12, color="grey"), align="left")

        return fig    
    
    def retornar_grafico_quantidade_pagamentos_anual(self, ticker, df):
        df = df.groupby(['Ano'])[['Dividends']].count()
        df.columns = ['Quantidade']

        fig = go.Figure()

        fig.add_trace(go.Bar(x=df.index,
                             y=df['Quantidade'],
                             name="Quantidade",
                             texttemplate = "%{value}",
                             hovertemplate = "<b>" + ticker + "</b><br>Ano: %{x}<br>" + "Quantidade" + ": " + "%{y}",
                             textposition="inside",
                             textangle=0,
                             textfont={'family': "Arial", 'size': 15, 'color': "Black"}))

        fig.update_xaxes(tickvals=df.index) 

        fig.update_layout(
            xaxis = {
                'title': "Ano",
            },
            title={'text': '<b>' + ticker + " - Número de vezes que pagou dividendos por ano",
                'y':0.9, 'x':0.5,
                'xanchor': 'center', 'yanchor': 'top'})
        
        # Pega a data em que o gráfico foi gerado
        today = date.today().strftime('%d/%m/%Y')

        fig.add_annotation(x=1, y=0, 
                        text=f"Fonte dos dados: https://api.carteiraglobal.com/ <br>Data da geração: {today}", showarrow=False,
                        xref='paper', yref='paper', 
                        xshift=0, yshift=-110, font=dict(size=12, color="grey"), align="left")

        return fig
    
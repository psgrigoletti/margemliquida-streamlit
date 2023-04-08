import pandas_market_calendars as mcal
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import datetime
import random
import numpy as np

class Resultado:
    def __init__(self):
      self.dias_apos = None
      self.variacoes = []
      self.soma_variacoes = 0
      self.periodos_encontrados = 0
      self.media = 0
      self.media_dias_positivos = 0
      self.media_dias_negativos = 0
      self.payoff = 0
      self.drawdown_maximo = 0 
      self.maxima = 0
      self.minima = 0

    def __str__(self):
      return f" max: {self.maxima}, min {self.minima}, " + \
             f"media: {self.media}, media_dias_positivos {self.media_dias_positivos}, media_dias_negativos: {self.media_dias_negativos}"

class DiasConsecutivos:
    def __init__(self, start_date, end_date, ticker: str, dias_apos: list, direcao, dias_consecutivos):
        self.non_business_days = None
        self.start_date = start_date
        self.end_date = end_date
        
        # Define o layout do gráfico
        self.data_inicial_formatada = pd.Timestamp(self.start_date).strftime('%d/%m/%Y')
        self.data_final_formatada = pd.Timestamp(self.end_date).strftime('%d/%m/%Y')
        
        self.ticker = ticker.upper()
        if not self.ticker.endswith(".SA"):
            self.ticker += ".SA"
        
        self.direcao = direcao
        self.direcoes = ['Baixa', 'Alta']
        self.n_days = dias_consecutivos

        self.resultados = {}
        self.df = None
        self.periodos = []
        self.dias_apos = dias_apos
        self.dias_apos.sort()
        
        self.quantidade_periodos_encontrados = 0
        
        self.__inicializa_resultados()    
        self.__busca_dias_sem_cotacao()
        self.__baixar_dados_e_atualizar_df()
        self.__buscar_dias_consecutivos()

    def retornar_tabela(self):
        for d in self.dias_apos:
            self.resultados[d].periodos_encontrados = self.quantidade_periodos_encontrados
            self.resultados[d].variacoes = []
            for i in range(0, len(self.df)):
                if self.df[f'{self.direcao}_{self.n_days}_dias'][i]==True:
                    if i+d < len(self.df):
                        # TODO: NAO EH PEGAR O PCT... EH PEGAR O PRECO DE FECHAMENTO DO DIA I+1+D E VER QUANTO REPRESENTA COMPARADO COM O DIA I+1
                        variacao = sum(self.df["pct_change"][i+1:i+1+d])
                        self.resultados[d].variacoes.append(variacao*100)

        relatorio = "#### Estratégia: Dias Consecutivos\n"
        relatorio += "#### Tipo: Retorno à Média\n"
        relatorio += f"#### {self.ticker} - Resultados após períodos de {self.n_days} {self.direcao.lower()}s consecutivas, entre {self.data_inicial_formatada} e {self.data_final_formatada}\n"
        relatorio += f"#### Número de ocorrências: {self.quantidade_periodos_encontrados}\n"

        if self.direcao == self.direcoes[1]: # ALTA/UP
            resultado_esperado = "negativa (-)"
            resultado_nao_esperado = "positiva (+)"
        if self.direcao == self.direcoes[0]: # BAIXA/DOWN
            resultado_esperado = "positiva (+)"
            resultado_nao_esperado = "negativa (-)"
   
        tabela = []
        tabela.append(["| Dias |"])
        tabela.append(["| ---- |"])
        tabela.append(["| **Variação média** |"])
        tabela.append(["|  |"])
        tabela.append(["| [:green[ACERTOS]] **Número de acertos** |"])
        tabela.append([f"| [:green[ACERTOS]] **Variação {resultado_esperado} média** |"])
        tabela.append(["| [:green[ACERTOS]] **Melhor resultado** |"])
        tabela.append(["|  |"])
        tabela.append(["| [:red[ERROS]] **Número de erros** |"])
        tabela.append([f"| [:red[ERROS]] **Variação {resultado_nao_esperado} média** |"])
        tabela.append(["| [:red[ERROS]] **Pior resultado** |"])
        tabela.append(["|  |"])
        tabela.append(["| **Taxa de acerto** |"])
        tabela.append(["| **Expectativa matemática** |"])
   
        for k in self.resultados.keys():
            taxa = 0
            expectativa_matematica = 0
            media_melhores_resultado = 0
            media_piores_resultado = 0

            media = np.mean(self.resultados[k].variacoes)
            media = round(media, 2)
            if self.direcao == self.direcoes[1]: # ALTA/UP
                resultados_esperados = [x for x in self.resultados[k].variacoes if x < 0]
                resultados_nao_esperados = [x for x in self.resultados[k].variacoes if x > 0]

                melhor_resultado = round(min(self.resultados[k].variacoes), 2)
                pior_resultado = round(max(self.resultados[k].variacoes), 2) 
            if self.direcao == self.direcoes[0]: # BAIXA/DOWN
                resultados_esperados = [x for x in self.resultados[k].variacoes if x > 0]
                resultados_nao_esperados = [x for x in self.resultados[k].variacoes if x < 0]

                melhor_resultado = round(max(self.resultados[k].variacoes), 2)
                pior_resultado = round(min(self.resultados[k].variacoes), 2) 

            media_melhores_resultado = round((sum(resultados_esperados)/len(resultados_esperados)),2)
            media_piores_resultado = round((sum(resultados_nao_esperados)/len(resultados_nao_esperados)),2)
            taxa = round((len(resultados_esperados)/(len(resultados_esperados)+len(resultados_nao_esperados)))*100,2)

            expectativa_matematica_ganhos = taxa * media_melhores_resultado
            expectativa_matematica_perdas = abs((1 - taxa) * media_piores_resultado)
            expectativa_matematica = round(expectativa_matematica_ganhos - expectativa_matematica_perdas, 2)

            tabela[0].append(f" {k} dia |")
            tabela[1].append(" ----: |")
            tabela[2].append(f" {media}% |")
            tabela[3].append(" |")
            tabela[4].append(f" {len(resultados_esperados)} |")
            tabela[5].append(f" {media_melhores_resultado}% |")
            tabela[6].append(f" {melhor_resultado}% |")
            tabela[7].append(" |")
            tabela[8].append(f" {len(resultados_nao_esperados)} |")
            tabela[9].append(f" {media_piores_resultado}% |")
            tabela[10].append(f" {pior_resultado}% |")
            tabela[11].append(" |")
            tabela[12].append(f" {taxa}% |")
            if expectativa_matematica>=0:
                tabela[13].append(f" **:green[{expectativa_matematica}%]** |")
            else:
                tabela[13].append(f" **:red[{expectativa_matematica}%]** |")
                
        for t in tabela:
            relatorio += " ".join(t) + "\n"

        return relatorio 

    def retornar_relatorio(self):
        for d in self.dias_apos:
            self.resultados[d].periodos_encontrados = self.quantidade_periodos_encontrados
            self.resultados[d].variacoes = []
            for i in range(0, len(self.df)):
                if self.df[f'{self.direcao}_{self.n_days}_dias'][i]==True:
                    if i+d < len(self.df):
                        # TODO: NAO EH PEGAR O PCT... EH PEGAR O PRECO DE FECHAMENTO DO DIA I+1+D E VER QUANTO REPRESENTA COMPARADO COM O DIA I+1
                        variacao = sum(self.df["pct_change"][i+1:i+1+d])
                        self.resultados[d].variacoes.append(variacao*100)

        relatorio = "#### Estratégia: Dias Consecutivos\n"
        relatorio += "#### Tipo: Retorno à Média\n"
        relatorio += f"#### {self.ticker} - Resultados após períodos de {self.n_days} {self.direcao.lower()}s consecutivas, entre {self.data_inicial_formatada} e {self.data_final_formatada}\n"
        relatorio += f"#### Número de ocorrências: {self.quantidade_periodos_encontrados}\n"
        
        if self.direcao == "Alta":
            objetivo = "Baixa"
        else:
            objetivo = "Alta"
        
        relatorio += f"##### Objetivo: {objetivo}\n"
   
        for k in self.resultados.keys():
            taxa = 0
            expectativa_matematica = 0
            media_melhores_resultado = 0
            media_piores_resultado = 0

            media = np.mean(self.resultados[k].variacoes)
            media = round(media, 2)
            if self.direcao == self.direcoes[1]: # ALTA/UP
                resultado_esperado = "negativa (-)"
                resultados_esperados = [x for x in self.resultados[k].variacoes if x < 0]
                resultado_nao_esperado = "positiva (+)"
                resultados_nao_esperados = [x for x in self.resultados[k].variacoes if x > 0]

                melhor_resultado = round(min(self.resultados[k].variacoes), 2)
                pior_resultado = round(max(self.resultados[k].variacoes), 2) 
            
            if self.direcao == self.direcoes[0]: # BAIXA/DOWN
                resultado_esperado = "positiva (+)"
                resultados_esperados = [x for x in self.resultados[k].variacoes if x > 0]
                resultado_nao_esperado = "negativa (-)"
                resultados_nao_esperados = [x for x in self.resultados[k].variacoes if x < 0]

                melhor_resultado = round(max(self.resultados[k].variacoes), 2)
                pior_resultado = round(min(self.resultados[k].variacoes), 2) 

            media_melhores_resultado = round((sum(resultados_esperados)/len(resultados_esperados)),2)
            media_piores_resultado = round((sum(resultados_nao_esperados)/len(resultados_nao_esperados)),2)
            taxa = round((len(resultados_esperados)/(len(resultados_esperados)+len(resultados_nao_esperados)))*100,2)

            expectativa_matematica_ganhos = taxa * media_melhores_resultado
            expectativa_matematica_perdas = abs((1 - taxa) * media_piores_resultado)
            expectativa_matematica = round(expectativa_matematica_ganhos - expectativa_matematica_perdas, 2)

            lista_variacoes_arredondada = [round(x, 2) for x in self.resultados[k].variacoes]
            
            relatorio += f"##### {k} dia depois:\n"
            relatorio += "```\n"
            relatorio += f"Variações: {lista_variacoes_arredondada}\n"
            relatorio += f"Variação média : {media}%\n"
            relatorio += "\n"
            relatorio += f"[ACERTOS] Número de acertos: {len(resultados_esperados)}\n"
            relatorio += f"[ACERTOS] Variação {resultado_esperado} média: {media_melhores_resultado}%\n"
            relatorio += f"[ACERTOS] Melhor resultado: {melhor_resultado}%\n"
            relatorio += "\n"
            relatorio += f"[ERROS] Número de erros: {len(resultados_nao_esperados)}\n"
            relatorio += f"[ERROS] Variação {resultado_nao_esperado} média: {media_piores_resultado}%\n"
            relatorio += f"[ERROS] Pior resultado: {pior_resultado}%\n"
            relatorio += "\n"
            relatorio += f"Taxa de acerto: {taxa}%\n"
            relatorio += f"Expectativa matemática: {expectativa_matematica}%\n```\n"

        return relatorio 

    def retornar_grafico(self):
        fig = go.Figure(data=[go.Candlestick(x=self.df.index, open=self.df['Open'],
                                            high=self.df['High'], low=self.df['Low'],
                                            close=self.df['Close'], name=self.ticker)])

        # Itera sobre a lista de tuplas e adiciona os retângulos ao gráfico
        for tupla in self.periodos:
            data_inicial_rect = tupla[0]
            data_final_rect = tupla[1]
            menor_y = round(min(self.df.loc[pd.to_datetime(data_inicial_rect):pd.to_datetime(data_final_rect)]["Low"]),2)-1
            maior_y = round(max(self.df.loc[pd.to_datetime(data_inicial_rect):pd.to_datetime(data_final_rect)]["High"]),2)+1
            cor = random.choice(["RoyalBlue", "Green", "Blue", "Red", "Yellow", "Pink"])
            cor_linha = "Green" if self.direcao == self.direcoes[0] else "Red"
            fig.add_shape(type="rect",
                        x0=data_inicial_rect, 
                        y0=menor_y,
                        x1=data_final_rect, 
                        y1=maior_y,
                        fillcolor=cor,
                        opacity=0.3,
                        line=dict(color=cor_linha, width=2))

        # Define o layout do gráfico
        fig.update_layout(title=f'{self.ticker} - Períodos de {self.n_days} {self.direcao.lower()}s consecutivas, entre {self.data_inicial_formatada} e {self.data_final_formatada}',
                        xaxis_title='Data',
                        yaxis_title='Preço (R$)', showlegend=True,
                        font=dict(size=12))

        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1 mês", step="month", stepmode="backward"),
                    dict(count=6, label="6 meses", step="month", stepmode="backward"),
                    dict(count=1, label="Este ano", step="year", stepmode="todate"),
                    dict(count=1, label="1 ano", step="year", stepmode="backward"),
                    dict(step="all", label="Tudo")
                ])
            )
        )

        fig.update_xaxes(
            rangebreaks=[
                dict(bounds=["sat", "mon"]), # hide weekends
                dict(values=self.non_business_days)  # hide
            ]
        )

        # Exibe o gráfico
        return fig #.show()        
    
    def __busca_dias_sem_cotacao(self):
        b3 = mcal.get_calendar('B3')

        # Obtém todos os dias úteis no período de tempo especificado
        business_days = b3.schedule(start_date=self.start_date, end_date=self.end_date).index.strftime('%Y-%m-%d').tolist()

        # Obtém todos os dias do período de tempo especificado
        all_days = pd.date_range(start=self.start_date, end=self.end_date, freq='D').strftime('%Y-%m-%d').tolist()

        # Obtém todos os dias não úteis (incluindo sábados, domingos e feriados) no período de tempo especificado
        self.non_business_days = list(set(all_days) - set(business_days))
        self.non_business_days.sort()
        
    def __inicializa_resultados(self):
        for d in self.dias_apos:
            r = Resultado()
            r.dias_apos = d
            self.resultados[d] = r
            
    def __baixar_dados_e_atualizar_df(self):
        self.df = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        self.df[f'{self.direcao}_{self.n_days}_dias'] = False
        self.df['inicio_dias'] = None
        self.df["pct_change"] = self.df["Close"].pct_change()
        
    def __buscar_dias_consecutivos(self):
        for i in range(self.n_days, len(self.df)):
            temp1 = self.df.copy(deep=True)
            temp1 = temp1.iloc[i - self.n_days: i]['Close']

            temp2 = self.df.copy(deep=True)
            temp2 = temp2.iloc[i - self.n_days+1: i+1]['Close']

            menor_data_achou = min(temp1.index)
            maior_data_achou = max(temp2.index)
            temp1 = temp1.reset_index()['Close']
            temp2 = temp2.reset_index()['Close']

            if self.direcao == self.direcoes[1]: # ALTA/UP
                if all(temp1 < temp2):
                    self.df.loc[maior_data_achou, f'{self.direcao}_{self.n_days}_dias'] = True
                    self.df.loc[maior_data_achou, 'inicio_dias'] = menor_data_achou
            elif self.direcao == self.direcoes[0]: # BAIXA/DOWN
                if all(temp1 > temp2):
                    self.df.loc[maior_data_achou, f'{self.direcao}_{self.n_days}_dias'] = True      
                    self.df.loc[maior_data_achou, 'inicio_dias'] = menor_data_achou
            else:
                raise Exception("Nenhuma direção definida.")
        
            self.quantidade_periodos_encontrados = len(self.df[self.df[f'{self.direcao}_{self.n_days}_dias']==True])
            datas = self.df[self.df[f'{self.direcao}_{self.n_days}_dias']==True].index
            self.periodos = [(self.df.loc[i]['inicio_dias'], i) for i in datas]
            # print(f"Períodos com {self.n_days} {self.direcao}s consecutivos: {self.quantidade_periodos_encontrados}")
            # print(f"Datas: {list(datas)}")
            # print(f"Períodos: {list(self.periodos)}")
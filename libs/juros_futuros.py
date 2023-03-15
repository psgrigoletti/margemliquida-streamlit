from datetime import datetime, date, timedelta
import requests
from time import sleep
from requests import ConnectTimeout, ReadTimeout
import pandas as pd
import plotly.graph_objects as go
from utils.data_hora_utils import DataHoraUtils
import urllib3

urllib3.disable_warnings()


class JurosFuturos:
    difuturo_por_titulo = None
    difuturo_por_titulo_transposto = None
    difuturo_por_vencimento_transposto = None
    difuturo_por_dias_uteis_transposto = None
    anbima_df = None

    def __init__(self):
        self.feriados_brasil = DataHoraUtils.retornar_feriados_no_brasil()

    def __buscar_proximas_series(self, anos_futuros=2, anos_anteriores=0):
        nomes_series = []
        data_atual = datetime.today()
        mes_atual = data_atual.month
        ano_atual = data_atual.year
        meses = {'1': 'F', '2': 'G', '3': 'H', '4': 'J', '5': 'K', '6': 'M',
                 '7': 'N', '8': 'Q', '9': 'U', '10': 'V', '11': 'X', '12': 'Z'}

        # Atualmente não é possível buscar séries passadas
        #
        # print("Busca dados anos anteriores")
        # for i in range(ano_atual - anos_anteriores - 1, ano_atual - 1):
        #     ano = str(i)
        #     nomes_series.append("DI1F" + ano[2:4])
        #     print(nomes_series)

        print("Busca dados ano atual")
        for i, letra in meses.items():
            if int(i) >= int(mes_atual):
                nomes_series.append("DI1" + letra + str(ano_atual)[2:4])
            # print(nomes_series)

        print("Busca dados anos futuros")
        for i in range(ano_atual + 1, ano_atual + anos_futuros + 1):
            ano = str(i)
            nomes_series.append("DI1F" + ano[2:4])
            # print(nomes_series)

        return nomes_series

    def __buscar_dias_uteis_ate_vencimento_titulo(self, titulo):
        dias_semana = {"SEGUNDA": 0, "TERCA": 1, "QUARTA": 2,
                       "QUINTA": 3, "SEXTA": 4, "SABADO": 5, "DOMINGO": 6}

        dia_vencimento = self.__buscar_vencimento_titulo(titulo)
        start = date.today()
        end = dia_vencimento.date()

        dias_uteis = sum(1 for day in self.__iterdates(start, end) if day.weekday() not in (
            dias_semana.get("SABADO"), dias_semana.get("DOMINGO")) and day not in self.feriados_brasil)
        dias_de_semana = sum(1 for day in self.__iterdates(start, end) if day.weekday(
        ) not in (dias_semana.get("SABADO"), dias_semana.get("DOMINGO")))
        feriados_na_semana = dias_de_semana - dias_uteis
        # print(f"Dias úteis entre {start} e {end}: {dias_uteis}")
        # print(f"Dias de semana entre {start} e {end}: {dias_de_semana}")
        # print(f"Feriados entre {start} e {end}: {feriados_na_semana}")
        return dias_uteis

    def __ajustar_data(self, df):
        meses = {'Jan': '01', 'Fev': '02', 'Mar': '03', 'Abr': '04', 'Mai': '05', 'Jun': '06',
                 'Jul': '07', 'Ago': '08', 'Set': '09', 'Out': '10', 'Nov': '11', 'Dez': '12'}

        for mes, numero in meses.items():
            df = df.str.replace(mes, numero)

        df = df.str.replace(" ", "/")
        df = pd.to_datetime(df, format="%d/%m/%Y")
        return df

    def __buscar_dados_futuros(self, titulo):
        sleep(0.1)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        url = "https://br.advfn.com/bolsa-de-valores/bmf/{}/historico/mais-dados-historicos".format(
            titulo)
        print("Abrindo " + url)
        html = requests.get(url, headers=headers, verify=False, timeout=5)
        dif = pd.read_html(html.text, decimal=',', thousands='.')[1]
        dif = dif[["Data", "Fechamento"]]
        dif = dif.rename(columns={"Fechamento": titulo})
        dif[['Data']] = dif[['Data']].apply(lambda x: self.__ajustar_data(x))
        dif = dif.set_index("Data")
        return dif

    def __iterdates(self, date1, date2):
        one_day = timedelta(days=1)
        current = date1

        while current < date2:
            yield current
            current += one_day

    def __buscar_vencimento_titulo(self, titulo):
        meses = {'01': 'F', '02': 'G', '03': 'H', '04': 'J', '05': 'K', '06': 'M',
                 '07': 'N', '08': 'Q', '09': 'U', '10': 'V', '11': 'X', '12': 'Z'}
        meses = {y: x for x, y in meses.items()}
        ano = "20" + titulo[-2:]
        mes = meses.get(titulo[3])

        dias = pd.date_range(start=mes + '/1/' + ano, periods=7, freq='BMS')
        dias = filter(lambda dia: datetime.fromtimestamp(
            dia.timestamp()) not in self.feriados_brasil, dias)
        dia = list(dias)[0]
        return dia

    def atualizar_dados(self, anos, anos_anteriores, semanas):
        self.semanas = semanas
        self.__atualizar_dados_advfn(anos, anos_anteriores)
        self.__atualizar_dados_anbima()
        self.__atualizar_dados_por_titulo()
        self.__atualizar_dados_por_vencimento()
        self.__atualizar_dados_por_dias_uteis()

    def __atualizar_dados_advfn(self, anos, anos_anteriores):
        self.series_advfn = []
        nomes_series = self.__buscar_proximas_series(anos, anos_anteriores)
        print(nomes_series)

        for nome_serie in nomes_series:
            try:
                s = self.__buscar_dados_futuros(nome_serie)
                s = s.loc[~s.index.duplicated(keep='first')]
                self.series_advfn.append(s)
            except ConnectTimeout:
                print("Timeout ao buscar dados de " +
                      nome_serie + ". Buscando próxima série...")
            except ReadTimeout:
                print("Timeout ao buscar dados de " +
                      nome_serie + ". Buscando próxima série...")

    def __atualizar_dados_anbima(self):
        hoje = date.today().strftime('%d/%m/%Y')
        ontem = date.today() - timedelta(days=1)
        ontem = ontem.strftime('%d/%m/%Y')

        url = 'https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp'
        payload = {'Idioma': 'US', 'Dt_Ref': ontem, 'saida': 'xml'}

        from urllib import request, parse
        data = parse.urlencode(payload).encode()
        # this will make the method "POST"
        req = request.Request(url, data=data)

        with request.urlopen(req) as response:
            xml = response.read()

        vertices = pd.read_xml(xml, xpath="//TERM_STRUCTURE")
        vertices.drop('Indexed', axis=1, inplace=True)
        vertices.drop('BEI', axis=1, inplace=True)
        vertices.dropna(inplace=True)
        vertices = vertices.replace({',': ''}, regex=True)
        vertices['Prefixed'] = vertices['Prefixed'].astype(float)
        vertices['Business_Day'] = vertices['Business_Day'].astype(int)
        vertices.rename({'Prefixed': 'Taxa'}, axis=1, inplace=True)
        vertices.rename({'Business_Day': 'DiasUteis'}, axis=1, inplace=True)
        # vertices

        circular = pd.read_xml(xml, xpath="//CIRCULAR ")
        circular = circular.replace({',': ''}, regex=True)
        circular['Rate'] = circular['Rate'].astype(float)
        circular['Business_Day'] = circular['Business_Day'].astype(int)
        circular.rename({'Rate': 'Taxa'}, axis=1, inplace=True)
        circular.rename({'Business_Day': 'DiasUteis'}, axis=1, inplace=True)
        circular.dropna(inplace=True)
        # circular

        self.anbima_df = pd.concat([vertices, circular]).sort_values(
            by="DiasUteis").drop_duplicates().reset_index(drop=True)
        self.anbima_df.set_index('DiasUteis', inplace=True)

    def __atualizar_dados_por_titulo(self):
        self.difuturo_por_titulo = pd.concat(self.series_advfn, axis=1)
        self.difuturo_por_titulo.index = pd.to_datetime(
            self.difuturo_por_titulo.index)
        dayofweek = self.difuturo_por_titulo.index.dayofweek
        self.semanal_por_titulo = self.difuturo_por_titulo.iloc[(dayofweek == 0) | (
            self.difuturo_por_titulo.index == self.difuturo_por_titulo.index.max())].copy()
        self.semanal_por_titulo.sort_index(ascending=False, inplace=True)
        self.difuturo_por_titulo = self.semanal_por_titulo.head(self.semanas+1)
        self.difuturo_por_titulo_transposto = self.difuturo_por_titulo.transpose(
            copy=True)

    def __atualizar_dados_por_dias_uteis(self):
        self.difuturo_por_dias_uteis_transposto = self.difuturo_por_titulo_transposto.copy(
            deep=True)
        self.difuturo_por_dias_uteis_transposto['Vencimento'] = self.difuturo_por_dias_uteis_transposto.index
        self.difuturo_por_dias_uteis_transposto['Vencimento'] = self.difuturo_por_dias_uteis_transposto['Vencimento'].apply(
            lambda x: self.__buscar_dias_uteis_ate_vencimento_titulo(x))
        self.difuturo_por_dias_uteis_transposto = self.difuturo_por_dias_uteis_transposto.loc[(
            self.difuturo_por_dias_uteis_transposto['Vencimento'] > 0)].copy()
        self.difuturo_por_dias_uteis_transposto = self.difuturo_por_dias_uteis_transposto.set_index(
            'Vencimento')
        self.difuturo_por_dias_uteis_transposto.sort_index(
            ascending=False, inplace=True)

    def __atualizar_dados_por_vencimento(self):
        self.difuturo_por_vencimento_transposto = self.difuturo_por_titulo_transposto.copy(
            deep=True)
        self.difuturo_por_vencimento_transposto['Vencimento'] = self.difuturo_por_vencimento_transposto.index
        self.difuturo_por_vencimento_transposto['Vencimento'] = self.difuturo_por_vencimento_transposto['Vencimento'].apply(
            lambda x: self.__buscar_vencimento_titulo(x))
        self.difuturo_por_vencimento_transposto = self.difuturo_por_vencimento_transposto.set_index(
            'Vencimento')
        self.difuturo_por_vencimento_transposto.sort_index(
            ascending=False, inplace=True)

    def retornar_grafico_por_data_vencimento(self):
        hoje = date.today().strftime('%d/%m/%Y')

        layout = go.Layout(
            annotations=[
                dict(x=1.12, y=1.05, align="right", valign="top", text='Semanas:', showarrow=False, xref="paper", yref="paper",
                     xanchor="center", yanchor="top"),
                dict(text=f"Fonte dos dados: ADVFN - https://br.advfn.com/ <br>Data: {hoje}", showarrow=False, x=0, y=-0.15,
                     xref='paper', yref='paper', xanchor='left', yanchor='bottom', xshift=-10, yshift=-150,
                     font=dict(size=10, color="grey"), align="left")
            ]
        )

        fig = go.Figure(layout=layout)

        fig.update_layout(title_text="Curva de Juros", title_font_size=20)
        fig.update_layout(autosize=False, width=900, height=700)

        fig.update_xaxes(title_text="Data de vencimento do título")
        fig.update_xaxes(tickangle=45)
        fig.update_xaxes(rangeslider_visible=True)

        fig.update_yaxes(title_text="Taxas (em %)")

        for numero, i in enumerate(self.difuturo_por_vencimento_transposto):
            ontem = date.today() - timedelta(days=1)

            if i.date() == ontem:
                texto_legenda = "(ADVFN) Ontem: " + i.strftime('%d/%m/%Y')
            else:
                texto_legenda = "(ADVFN) Semana " + \
                    str(numero) + ": " + i.strftime('%d/%m/%Y')

            # suavizado, conectando gaps https://plotly.com/python/line-charts/
            fig.add_trace(go.Scatter(x=self.difuturo_por_vencimento_transposto.index,
                                     y=self.difuturo_por_vencimento_transposto[i], mode='lines',
                                     name=texto_legenda, line_shape='spline', connectgaps=True))

        fig.update_layout()
        return fig

    def retornar_grafico_por_titulo(self):
        hoje = date.today().strftime('%d/%m/%Y')

        layout = go.Layout(
            annotations=[
                dict(x=1.12, y=1.05, align="right", valign="top", text='Semanas:', showarrow=False, xref="paper", yref="paper",
                     xanchor="center", yanchor="top"),
                dict(text=f"Fonte dos dados: ADVFN - https://br.advfn.com/ <br>Data: {hoje}", showarrow=False, x=0, y=-0.15,
                     xref='paper', yref='paper', xanchor='left', yanchor='bottom', xshift=-10, yshift=-150,
                     font=dict(size=10, color="grey"), align="left")
            ]
        )

        fig = go.Figure(layout=layout)

        fig.update_layout(title_text="Curva de Juros", title_font_size=20)
        fig.update_layout(autosize=False, width=900, height=700)

        fig.update_xaxes(title_text="Títulos")
        fig.update_xaxes(tickangle=45)
        fig.update_xaxes(rangeslider_visible=True)

        fig.update_yaxes(title_text="Taxas (em %)")

        for numero, i in enumerate(self.difuturo_por_titulo_transposto):
            # suavizado, conectando gaps https://plotly.com/python/line-charts/

            ontem = date.today() - timedelta(days=1)

            if i.date() == ontem:
                texto_legenda = "(ADVFN) Ontem: " + i.strftime('%d/%m/%Y')
            else:
                texto_legenda = "(ADVFN) Semana " + \
                    str(numero) + ": " + i.strftime('%d/%m/%Y')

            fig.add_trace(go.Scatter(x=self.difuturo_por_titulo_transposto.index,
                                     y=self.difuturo_por_titulo_transposto[i], mode='lines',
                                     name=texto_legenda, line_shape='spline', connectgaps=True))

        fig.update_layout()
        return fig

    def retornar_grafico_por_dias_uteis(self):
        hoje = date.today().strftime('%d/%m/%Y')
        ontem = date.today() - timedelta(days = 1)

        layout = go.Layout(
            annotations=[
                dict(x=1.12, y=1.05, align="right", valign="top", text='Semanas:', showarrow=False, xref="paper", yref="paper",
                     xanchor="center", yanchor="top"),
                dict(text=f"Fonte dos dados: ADVFN - https://br.advfn.com/, ANBIMA - https://www.anbima.com.br/ <br>Data: {hoje}",
                     showarrow=False, x=0, y=-0.15,
                     xref='paper', yref='paper', xanchor='left', yanchor='bottom', xshift=-10, yshift=-150,
                     font=dict(size=10, color="grey"), align="left")
            ]
        )

        fig = go.Figure(layout=layout)

        fig.update_layout(title_text="Curva de Juros", title_font_size=20)
        fig.update_layout(autosize=False, width=900, height=700)

        fig.update_xaxes(title_text="Dias úteis até o vencimento do título")
        fig.update_xaxes(tickangle=45)
        fig.update_xaxes(rangeslider_visible=True)

        fig.update_yaxes(title_text="Taxas (em %)")

        fig.add_trace(go.Scatter(x=self.anbima_df.index, y=self.anbima_df['Taxa'], name="(ANBIMA) Ontem: " + ontem.strftime(
            '%d/%m/%Y'), line_shape='spline', mode='lines+markers', connectgaps=True, marker_size=10))

        for numero, i in enumerate(self.difuturo_por_dias_uteis_transposto):
            # suavizado, conectando gaps https://plotly.com/python/line-charts/

            ontem = date.today() - timedelta(days=1)

            if i.date() == ontem:
                texto_legenda = "(ADVFN)   Ontem: " + i.strftime('%d/%m/%Y')
            else:
                texto_legenda = "(ADVFN)   Semana " + \
                    str(numero) + ": " + i.strftime('%d/%m/%Y')

            fig.add_trace(go.Scatter(x=self.difuturo_por_dias_uteis_transposto.index,
                                     y=self.difuturo_por_dias_uteis_transposto[i], mode='lines+markers',
                                     name=texto_legenda,
                                     line_shape='spline', connectgaps=True, marker_size=10))

        fig.update_layout()
        return fig
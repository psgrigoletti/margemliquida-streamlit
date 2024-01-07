import logging
from bcb import Expectativas
import plotly.graph_objects as go
import pandas as pd

class RelatorioFocus:
    em = None
    endpoint = None
    formato_data = '%Y-%m-%d'

    def __init__(self):
        self.em = Expectativas()
        self.em.describe()
        logging.info("Vai pegar o endpoint")
        self.endpoint = self.em.get_endpoint('ExpectativasMercadoAnuais')
        logging.info("Pegou o endpoint")

    def atualizar_atualizar_dados(self):
        self.buscar_dados_ipca()
        self.buscar_dados_selic()

    def buscar_dados_ipca(self):
        logging.info("Vai buscar Expectativas IPCA")

        self.ipca_expec_2023 = (self.endpoint.query()
                                .filter(self.endpoint.Indicador == 'IPCA', self.endpoint.DataReferencia == 2023)
                                .filter(self.endpoint.Data >= '2022-01-01')
                                .filter(self.endpoint.baseCalculo == '0')
                                .select(self.endpoint.Indicador, self.endpoint.Data, self.endpoint.Media, self.endpoint.Mediana, self.endpoint.DataReferencia)
                                .collect()
                                )
        logging.info("Buscou 2023")

        self.ipca_expec_2024 = (self.endpoint.query()
                                .filter(self.endpoint.Indicador == 'IPCA', self.endpoint.DataReferencia == 2024)
                                .filter(self.endpoint.Data >= '2022-01-01')
                                .filter(self.endpoint.baseCalculo == '0')
                                .select(self.endpoint.Indicador, self.endpoint.Data, self.endpoint.Media, self.endpoint.Mediana, self.endpoint.DataReferencia)
                                .collect()
                                )
        logging.info("Buscou 2024")
        
        self.ipca_expec_2025 = (self.endpoint.query()
                                .filter(self.endpoint.Indicador == 'IPCA', self.endpoint.DataReferencia == 2025)
                                .filter(self.endpoint.Data >= '2022-01-01')
                                .filter(self.endpoint.baseCalculo == '0')
                                .select(self.endpoint.Indicador, self.endpoint.Data, self.endpoint.Media, self.endpoint.Mediana, self.endpoint.DataReferencia)
                                .collect()
                                )
        logging.info("Buscou 2025")

        self.ipca_expec_2026 = (self.endpoint.query()
                                .filter(self.endpoint.Indicador == 'IPCA', self.endpoint.DataReferencia == 2026)
                                .filter(self.endpoint.Data >= '2022-01-01')
                                .filter(self.endpoint.baseCalculo == '0')
                                .select(self.endpoint.Indicador, self.endpoint.Data, self.endpoint.Media, self.endpoint.Mediana, self.endpoint.DataReferencia)
                                .collect()
                                )
        logging.info("Buscou 2026")

        # Formata a coluna de Data para formato datetime

        self.ipca_expec_2023['Data'] = pd.to_datetime(
            self.ipca_expec_2023['Data'], format=self.formato_data)
        self.ipca_expec_2024['Data'] = pd.to_datetime(
            self.ipca_expec_2024['Data'], format=self.formato_data)
        self.ipca_expec_2025['Data'] = pd.to_datetime(
            self.ipca_expec_2025['Data'], format=self.formato_data)
        self.ipca_expec_2026['Data'] = pd.to_datetime(
            self.ipca_expec_2026['Data'], format=self.formato_data)
        logging.info("Buscou tudo")

    def buscar_dados_selic(self):
        logging.info("Vai buscar Expectativas SELIC")
        
        self.selic_expec_2023 = (self.endpoint.query()
                                 .filter(self.endpoint.Indicador == 'Selic', self.endpoint.DataReferencia == 2023)
                                 .filter(self.endpoint.Data >= '2022-01-01')
                                 .filter(self.endpoint.baseCalculo == '0')
                                 .select(self.endpoint.Indicador, self.endpoint.Data, self.endpoint.Media, self.endpoint.Mediana, self.endpoint.DataReferencia)
                                 .collect()
                                 )
        logging.info("Buscou 2023")

        self.selic_expec_2024 = (self.endpoint.query()
                                 .filter(self.endpoint.Indicador == 'Selic', self.endpoint.DataReferencia == 2024)
                                 .filter(self.endpoint.Data >= '2022-01-01')
                                 .filter(self.endpoint.baseCalculo == '0')
                                 .select(self.endpoint.Indicador, self.endpoint.Data, self.endpoint.Media, self.endpoint.Mediana, self.endpoint.DataReferencia)
                                 .collect()
                                 )
        logging.info("Buscou 2024")

        self.selic_expec_2025 = (self.endpoint.query()
                                 .filter(self.endpoint.Indicador == 'Selic', self.endpoint.DataReferencia == 2025)
                                 .filter(self.endpoint.Data >= '2022-01-01')
                                 .filter(self.endpoint.baseCalculo == '0')
                                 .select(self.endpoint.Indicador, self.endpoint.Data, self.endpoint.Media, self.endpoint.Mediana, self.endpoint.DataReferencia)
                                 .collect()
                                 )
        logging.info("Buscou 2025")

        self.selic_expec_2026 = (self.endpoint.query()
                                 .filter(self.endpoint.Indicador == 'Selic', self.endpoint.DataReferencia == 2026)
                                 .filter(self.endpoint.Data >= '2022-01-01')
                                 .filter(self.endpoint.baseCalculo == '0')
                                 .select(self.endpoint.Indicador, self.endpoint.Data, self.endpoint.Media, self.endpoint.Mediana, self.endpoint.DataReferencia)
                                 .collect()
                                 )
        logging.info("Buscou 2026")

        # Formata a coluna de Data para formato datetime
        self.selic_expec_2023['Data'] = pd.to_datetime(
            self.selic_expec_2023['Data'], format=self.formato_data)
        self.selic_expec_2024['Data'] = pd.to_datetime(
            self.selic_expec_2024['Data'], format=self.formato_data)
        self.selic_expec_2025['Data'] = pd.to_datetime(
            self.selic_expec_2025['Data'], format=self.formato_data)
        self.selic_expec_2026['Data'] = pd.to_datetime(
            self.selic_expec_2026['Data'], format=self.formato_data)
        logging.info("Buscou tudo")

    def retornar_grafico_selic(self):
        self.buscar_dados_selic()
        fig = go.Figure()
        fig = fig.add_trace(go.Scatter(x=self.selic_expec_2023['Data'],
                            y=self.selic_expec_2023['Mediana'], name="Selic 2023"))

        fig = fig.add_trace(go.Scatter(x=self.selic_expec_2024['Data'],
                            y=self.selic_expec_2024['Mediana'], name="Selic 2024"))

        fig = fig.add_trace(go.Scatter(x=self.selic_expec_2025['Data'],
                            y=self.selic_expec_2025['Mediana'], name="Selic 2025"))

        fig = fig.add_trace(go.Scatter(x=self.selic_expec_2026['Data'],
                            y=self.selic_expec_2026['Mediana'], name="Selic 2026"))

        fig.update_layout(
            title='Focus - Relatório de Mercado - SELIC', title_x=0.5)
        return fig

    def retornar_grafico_ipca(self):
        fig = go.Figure()
        fig = fig.add_trace(go.Scatter(x=self.ipca_expec_2023['Data'],
                                       y=self.ipca_expec_2023['Mediana'],
                                       name="IPCA 2023"))

        fig = fig.add_trace(go.Scatter(x=self.ipca_expec_2024['Data'],
                                       y=self.ipca_expec_2024['Mediana'],
                                       name="IPCA 2024"))

        fig = fig.add_trace(go.Scatter(x=self.ipca_expec_2025['Data'],
                                       y=self.ipca_expec_2025['Mediana'],
                                       name="IPCA 2025"))

        fig = fig.add_trace(go.Scatter(x=self.ipca_expec_2026['Data'],
                                       y=self.ipca_expec_2026['Mediana'],
                                       name="IPCA 2026"))

        fig.update_layout(
            title='Focus - Relatório de Mercado - IPCA', title_x=0.5)
        return fig

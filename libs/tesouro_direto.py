from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import logging
import time

class TesouroDireto():
    
    TESOURO_IPCA = 'Tesouro IPCA+'
    TESOURO_IPCA_JUROS_SEMESTRAIS = 'Tesouro IPCA+ com Juros Semestrais'
    TESOURO_SELIC = 'Tesouro Selic'
    TESOURO_PREFIXADO = 'Tesouro Prefixado'
    TESOURO_PREFIXADO_JUROS_SEMESTRAIS = 'Tesouro Prefixado com Juros Semestrais'
    TAXA_COMPRA_MANHA = 'Taxa Compra Manha'
    PU_BASE_MANHA = 'PU Base Manha'
    VENCIMENTO_DO_TITULO = 'Vencimento do Titulo'
    DATA_BASE = 'Data Base'
    DATA_VENCIMENTO = 'Data Vencimento'
    DATA_VENDA = 'Data Venda'
    DATA_RESGATE = "Data Resgate"
            
    titulos = None
    tipos_titulos = None
    hoje = None
    selic2025 = None
    selic2027 = None
    pre2025 = None
    pre2029 = None
    pre2033 = None
    ipca2026 = None
    ipca2032 = None
    ipca2035 = None
    ipca2040 = None
    ipca2045 = None
    ipca2055 = None
            
    def __init__(self):
        logging.log(logging.INFO, "Inicializando objeto da classe TesouroDireto")
        # locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    def adicionar_range_slider(self, fig):
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

    def atualizar_graficos(self):
        logging.log(logging.INFO, "Buscando dados do site https://www.tesourotransparente.gov.br")        
        self.titulos = self.busca_titulos_tesouro_direto()
        self.titulos.sort_index(inplace=True)
        self.tipos_titulos = self.titulos.index.droplevel(level=1).droplevel(level=1).drop_duplicates().to_list()
        
        self.atualizar_dados_ipca()
        self.atualizar_dados_pre()
        self.atualizar_dados_selic()
        
        delta = 0
        # st.text(time.tzname)
        if time.tzname[0] == "UTC":
            delta = 3;
        agora = datetime.today()
        # st.text("Agora:")
        # st.text(agora)
        # st.text("Agora - delta:")
        agora = datetime.today() - timedelta(hours=delta, minutes=0) 
        # st.text(agora)
        # st.text("Agora formatado:")

        agora = datetime.today() - timedelta(hours=delta, minutes=0) 
        self.hoje = agora.strftime('%d/%m/%Y %H:%M:%S')
        
    def atualizar_dados_selic(self):
        self.selic2025 = self.titulos.loc[(self.TESOURO_SELIC, '2025-03-01')]
        self.selic2027 = self.titulos.loc[(self.TESOURO_SELIC, '2027-03-01')]

    def atualizar_dados_pre(self):
        self.pre2025 = self.titulos.loc[(self.TESOURO_PREFIXADO, '2025-01-01')]
        self.pre2029 = self.titulos.loc[(self.TESOURO_PREFIXADO, '2029-01-01')]
        self.pre2033 = self.titulos.loc[(self.TESOURO_PREFIXADO_JUROS_SEMESTRAIS, '2033-01-01')]

    def atualizar_dados_ipca(self):
        self.ipca2026 = self.titulos.loc[(self.TESOURO_IPCA, '2026-08-15')]
        self.ipca2032 = self.titulos.loc[(self.TESOURO_IPCA_JUROS_SEMESTRAIS, '2032-08-15')]
        self.ipca2035 = self.titulos.loc[(self.TESOURO_IPCA, '2035-05-15')]
        self.ipca2040 = self.titulos.loc[(self.TESOURO_IPCA_JUROS_SEMESTRAIS, '2040-08-15')]
        self.ipca2045 = self.titulos.loc[(self.TESOURO_IPCA, '2045-05-15')]
        self.ipca2055 = self.titulos.loc[(self.TESOURO_IPCA_JUROS_SEMESTRAIS, '2055-05-15')]
    
    def busca_titulos_tesouro_direto(self):
        url = 'https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv'
        df  = pd.read_csv(url, sep=';', decimal=',')
        df[self.DATA_VENCIMENTO] = pd.to_datetime(df[self.DATA_VENCIMENTO], dayfirst=True)
        df[self.DATA_BASE] = pd.to_datetime(df[self.DATA_BASE], dayfirst=True)
        multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
        df = df.set_index(multi_indice).iloc[: , 3:]  
        return df

    def busca_vendas_tesouro(self):
        url = "https://www.tesourotransparente.gov.br/ckan/dataset/f0468ecc-ae97-4287-89c2-6d8139fb4343/resource/e5f90e3a-8f8d-4895-9c56-4bb2f7877920/download/VendasTesouroDireto.csv"
        df  = pd.read_csv(url, sep=';', decimal=',')
        df[self.VENCIMENTO_DO_TITULO] = pd.to_datetime(df[self.VENCIMENTO_DO_TITULO], dayfirst=True)
        df[self.DATA_VENDA] = pd.to_datetime(df[self.DATA_VENDA], dayfirst=True)
        multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
        df = df.set_index(multi_indice).iloc[: , 3:]  
        return df

    def busca_recompras_tesouro(self):
        url = "https://www.tesourotransparente.gov.br/ckan/dataset/f30db6e4-6123-416c-b094-be8dfc823601/resource/30c2b3f5-6edd-499a-8514-062bfda0f61a/download/RecomprasTesouroDireto.csv"
        df  = pd.read_csv(url, sep=';', decimal=',')
        df[self.VENCIMENTO_DO_TITULO] = pd.to_datetime(df[self.VENCIMENTO_DO_TITULO], dayfirst=True)
        df[self.DATA_RESGATE] = pd.to_datetime(df[self.DATA_RESGATE], dayfirst=True)
        multi_indice = pd.MultiIndex.from_frame(df.iloc[:, :3])
        df = df.set_index(multi_indice).iloc[: , 3:]  
        return df

    def atualizar_eventos_grafico(self, fig):
        fig.add_trace(go.Scatter(
            x=[pd.to_datetime('01-01-2010', dayfirst=True),
               pd.to_datetime('01-01-2014', dayfirst=True),
               pd.to_datetime('31-08-2016', dayfirst=True), 
               pd.to_datetime('01-01-2018', dayfirst=True),
               pd.to_datetime('11-03-2020', dayfirst=True),
               pd.to_datetime('01-01-2023', dayfirst=True)],
            y=[7, 7.5, 8, 7, 1, 8],
            mode="markers+text",
            name="Eventos",
            text=["1º Governo Dilma", "2º Governo Dilma", "Impeachment Dilma", "Governo Bolsonaro", "Pandemia COVID", "3º Governo Lula"],
            textposition="top center"
        ))

    def retornar_grafico_precos_tesouro_selic(self):
        fig = go.Figure()
        fig = fig.add_trace(go.Scatter(x = self.selic2025.index,
                                       y = self.selic2025[self.PU_BASE_MANHA], 
                                       name="Tesouro Selic 2025"))
        fig = fig.add_trace(go.Scatter(x = self.selic2027.index,
                                       y = self.selic2027[self.PU_BASE_MANHA], 
                                       name="Tesouro Selic 2027"))
        fig.update_layout(
             title={
                'text': f"Tesouro SELIC - Preço (gerado em {self.hoje})",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
        fig.update_layout(legend=dict(x=0, y=-0.1, orientation="h",))
        return fig

    def retornar_grafico_taxas_tesouro_selic(self):
        fig = go.Figure()
        fig = fig.add_trace(go.Scatter(x = self.selic2025.index,
                                       y = self.selic2025[self.TAXA_COMPRA_MANHA], 
                                       name="Tesouro Selic 2025"))
        fig = fig.add_trace(go.Scatter(x = self.selic2027.index,
                                       y = self.selic2027[self.TAXA_COMPRA_MANHA], 
                                       name="Tesouro Selic 2027"))
        fig.update_layout(title={
                'text': f"Tesouro SELIC - Taxa (gerado em {self.hoje})",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
                     
        fig.update_layout(legend=dict(x=0, y=-0.1, orientation="h",))
        return fig

    def retornar_grafico_precos_tesouro_pre(self):
        fig = go.Figure()
        fig = fig.add_trace(go.Scatter(x = self.pre2025.index,
                                       y = self.pre2025[self.PU_BASE_MANHA], 
                                       name="Tesouro Prefixado 2025"))
        fig = fig.add_trace(go.Scatter(x = self.pre2029.index,
                                       y = self.pre2029[self.PU_BASE_MANHA], 
                                       name="Tesouro Prefixado 2029"))
        fig = fig.add_trace(go.Scatter(x = self.pre2033.index,
                                       y = self.pre2033[self.PU_BASE_MANHA], 
                                       name="Tesouro Prefixado com Juros Semestrais 2033"))
        fig.update_layout(title={
                'text': f"Tesouro Pré-Fixado - Preço (gerado em {self.hoje})",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
            
        fig.update_layout(legend=dict(x=0, y=-0.1, orientation="h",))
        return fig

    def retornar_grafico_taxas_tesouro_pre(self):
        fig = go.Figure()
        fig = fig.add_trace(go.Scatter(x = self.pre2025.index,
                                       y = self.pre2025[self.TAXA_COMPRA_MANHA], 
                                       name="Tesouro Prefixado 2025"))
        fig = fig.add_trace(go.Scatter(x = self.pre2029.index,
                                       y = self.pre2029[self.TAXA_COMPRA_MANHA], 
                                       name="Tesouro Prefixado 2029"))
        fig = fig.add_trace(go.Scatter(x = self.pre2033.index,
                                       y = self.pre2033[self.TAXA_COMPRA_MANHA], 
                                       name="Tesouro Prefixado com Juros Semestrais 2033"))                                  
        fig.update_layout(title={
                'text': f"Tesouro Pré-Fixado - Taxa (gerado em {self.hoje})",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
                
        fig.update_layout(legend=dict(x=0, y=-0.1, orientation="h",))
        return fig

    def retornar_grafico_precos_tesouro_ipca(self):
        fig = go.Figure()
        fig = fig.add_trace(go.Scatter(x = self.ipca2026.index,
                                       y = self.ipca2026[self.PU_BASE_MANHA], 
                                       name=self.TESOURO_IPCA + " 2025"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2032.index,
                                       y = self.ipca2032[self.PU_BASE_MANHA], 
                                       name="Tesouro IPCA+ com Juros Semestrais 2032"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2035.index,
                                       y = self.ipca2035[self.PU_BASE_MANHA], 
                                       name=self.TESOURO_IPCA + " 2035"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2040.index,
                                       y = self.ipca2040[self.PU_BASE_MANHA], 
                                       name="Tesouro IPCA+ com Juros Semestrais 2040"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2045.index,
                                       y = self.ipca2045[self.PU_BASE_MANHA], 
                                       name=self.TESOURO_IPCA + " 2045"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2055.index,
                                       y = self.ipca2055[self.PU_BASE_MANHA], 
                                       name="Tesouro IPCA+ com Juros Semestrais 2055"))
        fig.update_layout(title={
                'text': f"Tesouro IPCA+ - Preço (gerado em {self.hoje})",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
                
        fig.update_layout(legend=dict(x=0, y=-0.1, orientation="h",))
        return fig
        
    def retornar_grafico_taxas_tesouro_ipca(self):
        fig = go.Figure()

        fig = fig.add_trace(go.Scatter(x = self.ipca2026.index,
                                       y = self.ipca2026[self.TAXA_COMPRA_MANHA], 
                                       name=self.TESOURO_IPCA + " 2025"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2032.index,
                                       y = self.ipca2032[self.TAXA_COMPRA_MANHA], 
                                       name="Tesouro IPCA+ com Juros Semestrais 2032"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2035.index,
                                       y = self.ipca2035[self.TAXA_COMPRA_MANHA], 
                                       name=self.TESOURO_IPCA + " 2035"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2040.index,
                                       y = self.ipca2040[self.TAXA_COMPRA_MANHA], 
                                       name="Tesouro IPCA+ com Juros Semestrais 2040"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2045.index,
                                       y = self.ipca2045[self.TAXA_COMPRA_MANHA], 
                                       name=self.TESOURO_IPCA + " 2045"))
        fig = fig.add_trace(go.Scatter(x = self.ipca2055.index,
                                       y = self.ipca2055[self.TAXA_COMPRA_MANHA], 
                                       name="Tesouro IPCA+ com Juros Semestrais 2055"))
        fig.update_layout(title={
                'text': f"Tesouro IPCA+ - Taxa (gerado em {self.hoje})",
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'})
                
        self.atualizar_eventos_grafico(fig)
        fig.update_layout(legend=dict(x=0, y=-0.1, orientation="h",))
        return fig
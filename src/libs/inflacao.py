import sidrapy
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_hora_utils import DataHoraUtils


class Inflacao:
    ipca_12m = None
    ipca_gp_wider = None

    def __init__(self):
        pass

    def atualizar_dados(self):
        self.__atualizar_dados_12_meses()
        self.__atualizar_dados_grupos()

    def __atualizar_dados_grupos(self):
        # Importa as variações e os pesos dos grupos do IPCA
        ipca_gp_raw = sidrapy.get_table(
            table_code="7060",
            territorial_level="1",
            ibge_territorial_code="all",
            variable="63,66",
            period="all",
            classification="315/7170,7445,7486,7558,7625,7660,7712,7766,7786",
        )
        # Realiza a limpeza e manipulação da tabela
        ipca_gp = (
            ipca_gp_raw.loc[1:, ["V", "D2C", "D3N", "D4N"]]
            .rename(
                columns={
                    "V": "value",
                    "D2C": "date",
                    "D3N": "variable",
                    "D4N": "groups",
                }
            )
            .assign(
                variable=lambda x: x["variable"].replace(
                    {"IPCA - Variação mensal": "variacao", "IPCA - Peso mensal": "peso"}
                ),
                date=lambda x: pd.to_datetime(x["date"], format="%Y%m"),
                value=lambda x: x["value"].astype(float),
                groups=lambda x: x["groups"].astype(str),
            )
            .pipe(lambda x: x.loc[x["date"] > "2007-01-01"])
        )

        # Torna em formato wide e calcula a contribuição de cada grupo pro IPCA
        self.ipca_gp_wider = (
            ipca_gp.pivot_table(
                index=["date", "groups"], columns="variable", values="value"
            )
            .reset_index()
            .assign(contribuicao=lambda x: (x.peso * x.variacao) / 100)
        )

    def __atualizar_dados_12_meses(self):
        # Importa as variações do IPCA
        # Tabela 1737: https://sidra.ibge.gov.br/tabela/1737
        # Unidade Territorial - 1	Brasil
        # Variáveis: 63	IPCA - Variação mensal, 69	IPCA - Variação acumulada no ano, 2263	IPCA - Variação acumulada em 3 meses,
        #            2264	IPCA - Variação acumulada em 6 meses, 2265	IPCA - Variação acumulada em 12 meses

        ipca_raw = sidrapy.get_table(
            table_code="1737",
            territorial_level="1",
            ibge_territorial_code="all",
            variable="63,69,2263,2264,2265",
            period="last%20472",
        )

        # Realiza a limpeza e manipulação da tabela
        ipca = (
            ipca_raw.loc[1:, ["V", "D2C", "D3N"]]
            .rename(columns={"V": "value", "D2C": "date", "D3N": "variable"})
            .assign(
                variable=lambda x: x["variable"].replace(
                    {
                        "IPCA - Variação mensal": "Var. mensal (%)",
                        "IPCA - Variação acumulada no ano": "Var. acumulada no ano (%)",
                        "IPCA - Variação acumulada em 3 meses": "Var. MM3M (%)",
                        "IPCA - Variação acumulada em 6 meses": "Var. MM6M (%)",
                        "IPCA - Variação acumulada em 12 meses": "Var. MM12M (%)",
                    }
                ),
                date=lambda x: pd.to_datetime(x["date"], format="%Y%m"),
                value=lambda x: x["value"].astype(float),
            )
            .pipe(lambda x: x.loc[x["date"] > "2007-01-01"])
        )

        self.ipca_12m = ipca.pipe(lambda x: x.loc[x.variable == "Var. MM12M (%)"])

    def retornar_grafico_acumulado_12m(self):
        hoje = DataHoraUtils.retorna_data_atual_formato_ddmmyyyy()

        layout = go.Layout(
            annotations=[
                dict(
                    text=f"Fonte dos dados: SIDRA/IBGE<br>Data: {hoje}",
                    showarrow=False,
                    x=0,
                    y=1,
                    xref="paper",
                    yref="paper",
                    xanchor="left",
                    yanchor="bottom",
                    xshift=0,
                    yshift=0,
                    font=dict(size=10, color="grey"),
                    align="left",
                )
            ]
        )

        fig = go.Figure(layout=layout)
        fig = fig.add_trace(
            go.Scatter(x=self.ipca_12m["date"], y=self.ipca_12m["value"])
        )
        fig.update_layout(
            title={
                "text": "<b>IPCA acumulado em 12 meses",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            }
        )

        return fig

    def retornar_grafico_por_grupo(self):
        hoje = DataHoraUtils.retorna_data_atual_formato_ddmmyyyy()
        colors = [
            "#282f6b",
            "#b22200",
            "#eace3f",
            "#224f20",
            "#b35c1e",
            "#419391",
            "#839c56",
            "#3b89bc",
        ]

        fig = px.bar(
            self.ipca_gp_wider,
            x="date",
            y="contribuicao",
            color="groups",
            color_discrete_sequence=colors,
        )

        fig.update_layout(
            title={
                "text": f"Contribuições de cada setor no IPCA (Gráfico gerado em {hoje})",
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            }
        )

        fig.update_layout(
            legend=dict(title="Grupos"),
            xaxis=dict(title="Data"),
            yaxis=dict(title="Contribuição"),
        )

        return fig

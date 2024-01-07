import io

# import locale
import logging
import os
import time
import zipfile
from datetime import datetime
from multiprocessing import Pool

import pandas as pd
import plotly.graph_objects as go
import requests
import xlsxwriter


class AnaliseFundamentalista:
    demonstrativos_interesse = ["BPA", "DRE", "BPP"]
    codigos_cvm = []

    def gera_df_anual(self, df, filtros_indice):
        df_anual = df.copy(deep=True)

        for filtro in filtros_indice:
            df_anual = df_anual[
                df_anual.index.get_level_values(filtro["indice"]).str[4:8]
                == filtro["mes"]
            ]

        df_anual.index = df_anual.index.get_level_values(1).str[:4]
        return df_anual

    def retorna_trimestre(self, df, possui_data_inicio_exercicio=True):
        if (
            possui_data_inicio_exercicio
            and df["MES_INICIAL"] == "01"
            and df["MES_FINAL"] == "03"
        ) or ((not possui_data_inicio_exercicio) and df["MES_FINAL"] == "03"):
            return str(df["ANO"]) + "-01-01"
        if (
            possui_data_inicio_exercicio
            and df["MES_INICIAL"] == "04"
            and df["MES_FINAL"] == "06"
        ) or ((not possui_data_inicio_exercicio) and df["MES_FINAL"] == "06"):
            return str(df["ANO"]) + "-04-01"
        if (
            possui_data_inicio_exercicio
            and df["MES_INICIAL"] == "07"
            and df["MES_FINAL"] == "09"
        ) or ((not possui_data_inicio_exercicio) and df["MES_FINAL"] == "09"):
            return str(df["ANO"]) + "-07-01"
        if (
            possui_data_inicio_exercicio
            and df["MES_INICIAL"] == "10"
            and df["MES_FINAL"] == "12"
        ) or ((not possui_data_inicio_exercicio) and df["MES_FINAL"] == "12"):
            return str(df["ANO"]) + "-10-01"
        else:
            return None

    def gera_df_trimestral(self, df, possui_data_inicio_exercicio=True):
        df_trimestral = df.copy(deep=True)

        if possui_data_inicio_exercicio:
            df_trimestral["MES_INICIAL"] = df_trimestral.index.get_level_values(1).str[
                5:7
            ]
            df_trimestral["MES_FINAL"] = df_trimestral.index.get_level_values(2).str[
                5:7
            ]
        else:
            df_trimestral["MES_INICIAL"] = df_trimestral.index.get_level_values(1).str[
                5:7
            ]
            df_trimestral["MES_FINAL"] = df_trimestral.index.get_level_values(1).str[
                5:7
            ]

        df_trimestral["ANO"] = df_trimestral.index.get_level_values(1).str[:4]
        df_trimestral["TRIMESTRE"] = df_trimestral.apply(
            self.retorna_trimestre, axis=1, args=(possui_data_inicio_exercicio,)
        )

        df_trimestral.index = df_trimestral["TRIMESTRE"]
        # df_trimestral[df_trimestral['TRIMESTRE'].str[-6:]=='-10-01']

        df_trimestral = df_trimestral.drop("TRIMESTRE", axis=1)
        df_trimestral = df_trimestral.drop("MES_INICIAL", axis=1)
        df_trimestral = df_trimestral.drop("MES_FINAL", axis=1)
        df_trimestral = df_trimestral.drop("ANO", axis=1)

        df_trimestral.sort_index(ascending=False, inplace=True)
        df_trimestral = df_trimestral[df_trimestral.index.notnull()]
        return df_trimestral

    def gera_grafico_anual(
        self, df_anual, titulo, descricao_eixo_y, unidade_eixo_y, unidade_y_apos=True
    ):
        fig = go.Figure()

        anos = list(df_anual.index.unique())

        for c in df_anual.columns:
            if unidade_y_apos:
                template_y = "%{value:.2f} " + unidade_eixo_y
                hover_template_y = (
                    "<b>"
                    + titulo
                    + "</b><br>Data: %{label}<br>"
                    + descricao_eixo_y
                    + ": %{y:.2f}"
                    + unidade_eixo_y
                )
            else:
                template_y = unidade_eixo_y + " %{value:.2f}"
                hover_template_y = (
                    "<b>"
                    + titulo
                    + "</b><br>Data: %{label}<br>"
                    + descricao_eixo_y
                    + ": "
                    + unidade_eixo_y
                    + " %{y:.2f} "
                )

            fig.add_trace(
                go.Bar(
                    x=df_anual.index,
                    y=df_anual[c],
                    name=c,
                    text=df_anual[c],
                    texttemplate=template_y,
                    hovertemplate=hover_template_y,
                    textposition="inside",
                    textangle=0,
                    textfont={"family": "Arial", "size": 15, "color": "Black"},
                )
            )

        if unidade_eixo_y:
            titulo_eixo_y = descricao_eixo_y + " (" + unidade_eixo_y + ")"
        else:
            titulo_eixo_y = descricao_eixo_y

        fig.update_layout(
            yaxis_title=titulo_eixo_y,
            xaxis_title="Anos",
            legend_title="Empresas selecionadas:",
            title={
                "text": "<b>" + titulo + " Anual para os anos de " + ", ".join(anos),
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            legend=dict(x=0, y=-0.5),
            barmode="group",
            bargap=0.2,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1,
        )  # gap between bars of the same location coordinate.

        # Pega a data em que o gráfico foi gerado
        today = datetime.today().strftime("%d/%m/%Y")

        fig.add_annotation(
            x=0.9,
            y=0,
            text=f"Fonte dos dados: https://dados.cvm.gov.br/ <br>Data da geração: {today}",
            showarrow=False,
            xref="paper",
            yref="paper",
            xshift=150,
            yshift=-130,
            font=dict(size=12, color="grey"),
            align="left",
        )

        return fig

    def gera_grafico_trimestral(
        self,
        df_trimestral,
        titulo,
        descricao_eixo_y,
        unidade_eixo_y,
        unidade_y_apos=True,
    ):
        fig = go.Figure()

        anos = list(df_trimestral.index.str[0:4].unique())
        anos.sort()

        if unidade_y_apos:
            template_y = "%{value:.2f} " + unidade_eixo_y
            hover_template_y = (
                "<b>"
                + titulo
                + "</b><br>Data: %{label}<br>"
                + descricao_eixo_y
                + ": %{y:.2f}"
                + unidade_eixo_y
            )
        else:
            template_y = unidade_eixo_y + " %{value:.2f}"
            hover_template_y = (
                "<b>"
                + titulo
                + "</b><br>Data: %{label}<br>"
                + descricao_eixo_y
                + ": "
                + unidade_eixo_y
                + " %{y:.2f} "
            )

        for c in df_trimestral.columns:
            fig.add_trace(
                go.Bar(
                    x=df_trimestral.index,
                    y=df_trimestral[c],
                    name=c,
                    hovertemplate=hover_template_y,
                    text=df_trimestral[c],
                    texttemplate=template_y,
                    textposition="inside",
                    textangle=0,
                    textfont={"family": "Arial", "size": 15, "color": "Black"},
                )
            )
        fig.update_xaxes(
            tickangle=-80,
        )

        if unidade_eixo_y:
            titulo_eixo_y = descricao_eixo_y + " (" + unidade_eixo_y + ")"
        else:
            titulo_eixo_y = descricao_eixo_y

        fig.update_layout(
            # autosize=False,
            # width=1200,
            # height=800,
            yaxis_title=titulo_eixo_y,
            xaxis_title="Trimestres/Anos",
            legend_title="Empresas selecionadas:",
            title={
                "text": "<b>"
                + titulo
                + " Trimestral para os anos de "
                + ", ".join(anos),
                "y": 0.9,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            legend=dict(x=0, y=-0.8),
            barmode="group",
            bargap=0.2,  # gap between bars of adjacent location coordinates.
            bargroupgap=0.1,
        )  # gap between bars of the same location coordinate.

        # Pega a data em que o gráfico foi gerado

        # fig.update_xaxes(
        #     showgrid=True,
        #     ticks="outside",
        #     tickson="boundaries",
        #     ticklen=20
        # )

        today = datetime.today().strftime("%d/%m/%Y")
        fig.add_annotation(
            x=0.9,
            y=0,
            text=f"Fonte dos dados: https://dados.cvm.gov.br/ <br>Data da geração: {today}",
            showarrow=False,
            xref="paper",
            yref="paper",
            xshift=150,
            yshift=-130,
            font=dict(size=12, color="grey"),
            align="left",
        )

        # fig.update_layout(hovermode="x unified")
        # fig.update_layout(
        #     hoverlabel=dict(
        #         bgcolor="white",
        #         font_size=16,
        #         font_family="Rockwell"
        #     )
        # )
        return fig

    def __init__(self):
        pass

    def set_codigos_cvm(self, codigos_cvm):
        self.codigos_cvm = codigos_cvm

    def gerar_grafico_anual(self):
        margem_liquida_empresas = pd.DataFrame()

        for empresa in self.empresas_selecionadas:
            print("Gerando grafico anual... empresa " + str(empresa))
            lucro_liquido = self.dre_completo.loc[empresa, :].loc[
                "Lucro/Prejuízo Consolidado do Período"
            ]
            receita_liquida = self.dre_completo.loc[empresa, :].loc[
                "Receita de Venda de Bens e/ou Serviços"
            ]
            margem_liquida = pd.Series(lucro_liquido / receita_liquida) * 100.0
            margem_liquida_empresas = pd.concat(
                [margem_liquida_empresas, margem_liquida], axis=1
            )

        margem_liquida_empresas.columns = self.empresas_selecionadas
        margem_liquida_empresas_anual = self.gera_df_anual(
            margem_liquida_empresas,
            [{"indice": 1, "mes": "-01-"}, {"indice": 2, "mes": "-12-"}],
        )
        return self.gera_grafico_anual(
            margem_liquida_empresas_anual, "Margem Liquida", "Percentual", "%"
        )

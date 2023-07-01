import datetime
import os
from datetime import date
from pprint import pprint
from typing import List

import fundamentus as fd
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from tabulate import tabulate
from utils.streamlit_utils import adicionar_avisos_dev


@st.cache_data(show_spinner="Buscando todos os dados fundamentalistas...", ttl=3600)
def get_resultado():
    return fd.get_resultado()


@st.cache_data(show_spinner="Buscando dados fundamentalistas de um papel...", ttl=3600)
def get_detalhes_papel(papel):
    return fd.get_detalhes_papel(papel)


@st.cache_data(show_spinner="Buscando lista de papeis...", ttl=3600)
def list_papel_all():
    return fd.list_papel_all()


class ItemClassificar:
    def __init__(self, ticker, valor, classificao=None):
        self.ticker = ticker
        self.valor = valor
        self.classificao = classificao

    def __repr__(self):
        return f"{self.ticker}: {self.valor}, classificao {self.classificao}"

    def __str__(self):
        return f"{self.ticker}: {self.valor}, classificao {self.classificao}"

    def __eq__(self, other):
        return self.ticker == other.ticker and self.valor == other.valor and self.classificao == other.classificao


def tranformar_df_em_lista(df: pd.DataFrame):
    df = df.astype(str)
    copia_df = df.copy()
    copia_df.reset_index(inplace=True)

    lista = []
    lista.append(copia_df.columns.tolist())

    for linha in copia_df.values.tolist():
        lista.append(linha)

    for numero_linha, linha in enumerate(lista):
        if numero_linha > 0:
            for numero_coluna, coluna in enumerate(linha):
                if numero_coluna > 0:
                    lista[numero_linha][numero_coluna] = ItemClassificar(
                        lista[0][numero_coluna], coluna)

    return lista


class Descricoes:
    DESCRICAO_PVP = """O P/VP, ou Preço sobre Valor Patrimonial, é um indicador que informa se o valor de uma ação está relativamente cara ou barata. O P/VP pode ser obtido através da divisão entre o preço de um ativo negociado em bolsa e o valor patrimonial da companhia."""
    DESCRICAO_PL = """O P/L, ou Preço/Lucro, é um índice usado para avaliar se o preço das ações de uma empresa está caro ou barato. Na fórmula do P/L, o preço analisado é sempre o valor por ação que está divulgado na bolsa em um certo momento. Já o lucro é o ganho líquido por cada uma das ações neste mesmo momento."""
    DESCRICAO_DY = """O Dividend Yield, que traduzido para o português refere-se a Rendimento de Dividendos, é o indicador que verifica a performance da organização mediante os proventos que foram pagos aos acionistas da empresa ao longo dos últimos 12 meses do ano."""
    DESCRICAO_ROE = """O ROE (Return on Equity), ou Retorno sobre Patrimônio Líquido, é um indicador de rentabilidade que serve para determinar o quão eficiente é uma empresa na geração de lucro a partir dos seus recursos. O ROE leva em conta o patrimônio líquido e os valores investidos no negócio, inclusive o de acionistas."""
    DESCRICAO_ROIC = """Analisar os números de uma empresa é uma prática recorrente entre os investidores da bolsa. Neste contexto, o ROIC é uma métrica utilizada com frequência por quem investe em ações."""
    DESCRICAO_PATRIMONIO_LIQUIDO = """O Patrimônio Líquido é um indicador contábil que indica a relação entre os ativos e passivos financeiros de uma empresa. Por conta disso, o Patrimônio Líquido representa o total de bens de uma companhia que realmente pertence aos seus acionistas. Para calcular o Patrimônio Líquido, basta fazer uma subtração entre os bens e direitos que uma organização possui em relação às suas obrigações financeiras. É possível afirmar que o PL é um dos conceitos mais importantes dentro de um balanço patrimonial. Nele, são registrados o capital social, lucros acumulados, contas de reserva e outros dados financeiros."""
    DESCRICAO_MARGEM_LIQUIDA = """A Margem Líquida é razão entre o Lucro Líquido e a Receita Líquida de uma companhia após a dedução de impostos e tributos. Podendo representar um resultado trimestral ou anual, a Margem Líquida representa o resultado líquido das vendas de um negócio. Portanto, está diretamente ligado com o nível de rentabilidade que uma companhia consegue com suas operações. Para os investidores, a Margem Líquida demonstra se uma empresa possui bons retornos a partir custos de produção do seu produto/serviço."""
    DESCRICAO_PRECO_SOBRE_CAPITAL_GIRO = """P/Capital de Giro representa o Preço da Ação dividido pelo Capital de Giro por ação de uma empresa. O P/Capital de Giro é um indicador muito importante na análise de empresas, já que permite que sejam encontradas boas e novas oportunidades de investimentos. O Capital de Giro de uma empresa representa o seu ativo circulante menos seu passivo circulante, ou seja, o resultado entre o dinheiro que ela possui e o que ela deve."""


detalhes = [
    {'indice': 'pl', 'nome': 'P/L', 'descricao': Descricoes.DESCRICAO_PL,
     'link': 'https://statusinvest.com.br/termos/p/p-l', 'ordenacao': 'ASC',
     'multiplicador': 1},  # Menor valor -> melhor

    {'indice': 'dy', 'nome': 'D.Y', 'descricao': Descricoes.DESCRICAO_DY,
     'link': 'https://statusinvest.com.br/termos/d/dividend-yield', 'ordenacao': 'DESC',
     'multiplicador': 100},  # Maior valor -> melhor

    {'indice': 'pvp', 'nome': 'P/VP', 'descricao': Descricoes.DESCRICAO_PVP,
     'link': 'https://statusinvest.com.br/termos/p/p-vp', 'ordenacao': 'ASC',
     'multiplicador': 1},  # Menor valor ->melhor

    {'indice': 'roe', 'nome': 'ROE', 'descricao': Descricoes.DESCRICAO_ROE,
     'link': 'https://statusinvest.com.br/termos/r/roe', 'ordenacao': 'DESC',
     'multiplicador': 100},  # Maior valor -> melhor

    {'indice': 'roic', 'nome': 'ROIC', 'descricao': Descricoes.DESCRICAO_ROIC,
     'link': 'https://statusinvest.com.br/termos/r/roic', 'ordenacao': 'DESC',
     'multiplicador': 100},  # Maior valor -> melhor

    {'indice': 'patrliq', 'nome': 'PATRIMÔNIO LÍQUIDO', 'descricao': Descricoes.DESCRICAO_PATRIMONIO_LIQUIDO,
     'link': 'https://statusinvest.com.br/termos/p/patrimonio-liquido', 'ordenacao': 'DESC',
     'multiplicador': 1},  # Maior valor -> melhor

    {'indice': 'mrgliq', 'nome': 'MARGEM LÍQUIDA', 'descricao': Descricoes.DESCRICAO_MARGEM_LIQUIDA,
     'link': 'https://statusinvest.com.br/termos/m/margem-liquida', 'ordenacao': 'DESC',
     'multiplicador': 100},  # Maior valor -> melhor

    {'indice': 'pcg', 'nome': 'P/CAPITAL DE GIRO', 'descricao': Descricoes.DESCRICAO_PRECO_SOBRE_CAPITAL_GIRO,
     'link': 'https://statusinvest.com.br/termos/p/p-capital-giro', 'ordenacao': 'ASC',
     'multiplicador': 1},  # Menor valor -> melhor

    # TODO: adicionar outros detalhes
    # psr, pa, , pebit, pacl, evebit, evebitda, mrgebit,
    # liqc, liq2m, divbpatr, c5y

]


def transformar_lista_pretty(lista):
    lista_pretty = lista
    lista_pretty[0][0] = ""

    # ajustando primeira coluna
    for numero_linha, linha in enumerate(lista_pretty):
        if numero_linha > 0:
            dados_indicador = list(
                filter(lambda d: d['indice'] == lista_pretty[numero_linha][0], detalhes))[0]
            mk_primeira_coluna = f"[{dados_indicador['nome']}]({dados_indicador['link']}, \"{dados_indicador['descricao']}\")"

            lista_pretty[numero_linha][0] = mk_primeira_coluna

        for numero_coluna, coluna in enumerate(linha):
            if numero_linha > 0 and numero_coluna > 0:
                item = coluna
                item.valor = formatar_valor(str(
                    float(item.valor)*dados_indicador['multiplicador']))

                if item.classificao == '1 lugar':
                    item.valor = f"🥇 **{item.valor}**"
                if item.classificao == '2 lugar':
                    item.valor = f"🥈 **{item.valor}**"
                if item.classificao == '3 lugar':
                    item.valor = f"🥉 **{item.valor}**"

                lista_pretty[numero_linha][numero_coluna] = f"{item.valor}"

    return lista_pretty


def adicionar_linha_medalhas(lista: List):
    medalhas = []

    for i in range(len(lista[0])):
        if i > 0:
            count_primeiro = 0
            count_segundo = 0
            count_terceiro = 0

            for j in range(len(lista)):
                if "🥇" in lista[j][i]:
                    count_primeiro += 1

                elif "🥈" in lista[j][i]:
                    count_segundo += 1

                elif "🥉" in lista[j][i]:
                    count_terceiro += 1

            medalhas.append(
                f"{count_primeiro} 🥇, {count_segundo} 🥈, {count_terceiro} 🥉")

    lista.append(["**Medalhas**"]+medalhas)
    return lista


def adicionar_linha_classificacao_final(lista: List):
    classificacao = []

    tupla_medalhas = []
    for n, i in enumerate(lista[-1][1:]):
        i = i.replace("🥇", "")
        i = i.replace("🥈", "")
        i = i.replace("🥉", "")
        ouro, prata, bronze = i.split(",")
        tupla_medalhas.append(
            (ouro.strip(), prata.strip(), bronze.strip(), lista[0][n+1]))

    ordenada = list(sorted(tupla_medalhas, reverse=True))
    ordenada = list(map(lambda x: x[3], ordenada))

    for ticker in lista[0][1:]:
        ordem = ordenada.index(ticker)+1

        if ordem == 1:
            classificacao.append(
                f"<p class=\"icone-maior\" title=\"{ordem}º lugar\">🥇</p>")
        elif ordem == 2:
            classificacao.append(
                f"<p class=\"icone-maior\" title=\"{ordem}º lugar\">🥈</p>")
        elif ordem == 3:
            classificacao.append(
                f"<p class=\"icone-maior\" title=\"{ordem}º lugar\">🥉</p>")
        else:
            classificacao.append(
                f"<p class=\"centralizado\">**{ordem}º lugar**</p>")

    lista.append(["**Classificação final**"]+classificacao)
    return lista


def ajustar_cabecalho(lista: List, dados):
    mais_cabecalho = ["**Cotação:**"]
    for numero_coluna, coluna in enumerate(lista[0]):
        if (numero_coluna > 0):
            mais_cabecalho.append("R$ " + formatar_valor(
                dados.loc['cotacao', coluna]))
        lista[0][numero_coluna] = f"[{coluna}](https://www.fundamentus.com.br/detalhes.php?papel={coluna})"
    lista.insert(1, mais_cabecalho)
    return lista


def classificar_numeros_lista(df: pd.DataFrame, detalhes):
    lista_completa = tranformar_df_em_lista(df)

    for numero_linha, linha in enumerate(lista_completa):
        if (numero_linha > 0):  # desconsiderar a linha com o título das colunas
            indice_linha = linha[0]
            ordem = list(filter(lambda o: o['indice'] ==
                                indice_linha, detalhes))[0]['ordenacao']

            for numero_coluna, coluna in enumerate(linha):
                if numero_coluna > 0:  # desconsiderar coluna 0
                    quantos = 0
                    # copia a linha sem o indice
                    linha_sem_o_item = linha[1:].copy()
                    # remove o proprio elemento da linha
                    linha_sem_o_item.remove(coluna)

                    for item2 in linha_sem_o_item:
                        if (ordem == "ASC" and float(item2.valor) < float(coluna.valor)) or \
                           (ordem == "DESC" and float(item2.valor) > float(coluna.valor)):
                            quantos += 1

                    coluna.classificao = f"{quantos+1} lugar"

    return lista_completa


def formatar_valor(valor: str):
    valor = float(valor)
    return "{:,.2f}".format(valor).replace('.', 'X').replace(',', '.').replace('X', ',')


def validar(papeis_selecionados, indicadores_selecionados, alertas):
    if (len(papeis_selecionados) == 0):
        with alertas:
            st.error(icon="🚨", body="Selecione pelo menos um ticker.")
        st.stop()
        
    print(type(indicadores_selecionados))
    if (len(indicadores_selecionados) == 0):
        with alertas:
            st.error(icon="🚨", body="Selecione pelo menos um indicador.")
        st.stop()


def gerar_tabela(dados, papeis_selecionados, indicadores_selecionados):
    dados_filtrados = dados[papeis_selecionados]
    detalhes_filtrados = list(
        filter(lambda x: x['nome'] in indicadores_selecionados, detalhes))
    dados_filtrados = dados_filtrados.loc[dados_filtrados.index.isin(
        det['indice'] for det in detalhes_filtrados)]
    retorno = transformar_lista_pretty(
        classificar_numeros_lista(dados_filtrados, detalhes))
    retorno = adicionar_linha_medalhas(retorno)
    retorno = adicionar_linha_classificacao_final(retorno)
    retorno = ajustar_cabecalho(retorno, dados)
    alinhamento = ("right",)*len(retorno[0])
    retorno_markdown = tabulate(
        retorno, headers="firstrow", tablefmt='pipe', showindex=False, colalign=alinhamento)
    st.write(retorno_markdown, unsafe_allow_html=True)


def gerar_observacoes():
    st.write("------")
    st.write(
        "Observação: Dados do site [Fundamentus](https://www.fundamentus.com.br/). Baseado no comparador existente no site [Status Invest](https://statusinvest.com.br/cliente/comparar-acoes/).")


def main():
    st.title(":tophat: Factor Investing")
    mensagens = st.container()

    st.markdown("""
    <style>
    .icone-maior {
        font-size: 25pt !important;
        text-align: center !important;
        margin: 0 !important;
    }

    .centralizado {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

    adicionar_avisos_dev()
    alertas = st.empty()
    dados = get_resultado()
    setores = fd.setor._setor
    dados = dados.transpose()
    lista_indicadores = list(map(lambda i: i['nome'], detalhes))

    form = st.form("form")

    papeis_selecionados = form.multiselect(
        'Selecione o(s) ticker(s):', dados.columns)
    indicadores_selecionados = form.multiselect(
        'Selecione o(s) indicadore(s):', lista_indicadores.copy(), lista_indicadores.copy())

    if form.form_submit_button("Comparar"):
        validar(papeis_selecionados, indicadores_selecionados, alertas)
        gerar_tabela(dados, papeis_selecionados, indicadores_selecionados)
        gerar_observacoes()

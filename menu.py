class Menu:
    labels = [
        "Inicial",
        "Carteira",
        "Inflação",
        "Tesouro Direto",
        "Dias Consecutivos",
        "Comparativo de Fundamentos",
        "Panorama de Mercado",
        "Rentabilidades mensais",
        "Dividendos",
        "Factor Investing",
        "Relatório FOCUS",
        # "Markowitz - Fronteira Eficiente",
        "Relatório QuantStats",
        "Fundos Brasileiros",
    ]

    def __init__(self):
        pass

    @staticmethod
    def carregar_pagina(selecionada):
        if selecionada == "Inicial":
            from paginas.page_inicial import main

        if selecionada == "Inflação":
            from paginas.page_inflacao import main

        if selecionada == "Tesouro Direto":
            from paginas.page_tesouro_direto import main

        if selecionada == "Dias Consecutivos":
            from paginas.page_dias_consecutivos import main

        if selecionada == "Comparativo de Fundamentos":
            from paginas.page_comparativo_fundamentos import main

        if selecionada == "Panorama de Mercado":
            from paginas.page_panorama_mercado import main

        if selecionada == "Rentabilidades mensais":
            from paginas.page_rentabilidades_mensais import main

        if selecionada == "Dividendos":
            from paginas.page_dividendos import main

        if selecionada == "Carteira":
            from paginas.page_comparador_carteiras import main

        if selecionada == "Factor Investing":
            from paginas.page_factor_investing import main

        if selecionada == "Relatório QuantStats":
            from paginas.page_relatorio_quantstats import main

        if selecionada == "Fundos Brasileiros":
            from paginas.page_fundos_brasileiros import main

        if selecionada == "Markowitz - Fronteira Eficiente":
            from paginas.page_markowitz import main

        if selecionada == "Relatório FOCUS":
            from paginas.page_relatorio_focus import main

        main()

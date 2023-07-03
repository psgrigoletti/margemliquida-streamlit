class Menu:
    labels = ["Inicial",
              "Carteira",
              "Inflação",
              "Tesouro Direto",
              "Dias Consecutivos",
              "Comparativo de Fundamentos",
              "Panorama de Mercado",
              "Rentabilidades mensais",
              "Dividendos",
              "Factor Investing"]

    def __init__(self):
        pass

    @staticmethod
    def carregar_pagina(selecionada):
        if selecionada == "Inicial":
            from paginas.page_inicial import main
            main()

        if selecionada == "Inflação":
            from paginas.page_inflacao import main
            main()

        if selecionada == "Tesouro Direto":
            from paginas.page_tesouro_direto import main
            main()

        if selecionada == "Dias Consecutivos":
            from paginas.page_dias_consecutivos import main
            main()

        if selecionada == "Comparativo de Fundamentos":
            from paginas.page_comparativo_fundamentos import main
            main()
            
        if selecionada == "Panorama de Mercado":
            from paginas.page_panorama_mercado import main
            main()
            
        if selecionada == "Rentabilidades mensais":
            from paginas.page_rentabilidades_mensais import main
            main()
            
        if selecionada == "Dividendos":
            from paginas.page_dividendos import main
            main()

        if selecionada == "Carteira":
            from paginas.page_comparador_carteiras import main
            main()
            
        if selecionada == "Factor Investing":
            from paginas.page_factor_investing import main
            main()
        

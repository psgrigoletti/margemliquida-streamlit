class Menu:
    labels = ["Inicial",
              "Inflação",
              "Tesouro Direto",
              "Dias Consecutivos",
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

        if selecionada == "Factor Investing":
            from paginas.page_comparativo_fundamentos import main
            main()

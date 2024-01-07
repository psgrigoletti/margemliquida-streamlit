import re

import pandas as pd
import pdfplumber

tiposObservacoes = {
    "A": "Posição futuro",
    "T": "Liquidação pelo Bruto",
    "#2": "Corretora ou pessoa vinculada atuou na contra parte.",
    "#8": "Liquidação Institucional",
    "D#": "",
    "C": "Clubes e fundos de Ações",
    "I": "POP",
    "#": "Negócio direto",
    "P": "Carteira Própria",
    "H": "Home Broker",
    "D": "Day Trade",
    "X": "Box",
    "F": "Cobertura",
    "Y": "Desmanche de Box",
    "B": "Debêntures",
    "L": "Precatório",
}

tiposTemporariosAcoes = {
    "ERB": "",
    "ERA": "",
    "ERS": "",
    "ES": "",
    "ED": "",
    "EX": "",
    "EC": "Ex - Cisão",
    "EG": "Ex - Grupamento",
    "ER": "Ex - Rendimentos",
    "EJ": "Ex - Juros",
    "N1": "Cia. Nível 1 de Governança Corporativa",
    "N2": "Cia. Nível 2 de Governança Corporativa",
    "NM": "Cia. Novo Mercado",
}

tiposAcoes = {
    "UNT": "Units",
    "ON": "Ações Ordinárias",
    "PN": "Ações Preferenciais",
    "PNA": "Ações Preferenciais classe A",
    "PNB": "Ações Preferenciais classe B",
    "PNC": "Ações Preferenciais classe C",
    "PND": "Ações Preferenciais classe D",
    "CI": "Cotas de fundos de investimento",
    "DRN A": "",
    "DRN": "BDR Não Patrocinado",
    "DR1": "BDR Nível 1",
    "DR2": "BDR Nível 2",
    "DR3": "BDR Nível 3",
    "DRE": "BDR de ETF",
}

tiposMercado = {
    "VISTA": "Mercado à vista",
    "FRACIONARIO": "Mercado Fracionário",
    "OPCAO DE VENDA": "Opção de venda",
}

tipos_mercado = "|".join(tiposMercado)
tipos_acoes = "|".join(tiposAcoes)
tipos_temporarios_acoes = "|".join(tiposTemporariosAcoes)
tipos_observacoes = "|".join(tiposObservacoes)

regex_espaco = "(?:\s)?"
regex_espaco_obrigatorio = "(?:\s)?"

regex_fii = (
    "(1-BOVESPA){1}"
    + regex_espaco
    + "(C|V){1}"
    + regex_espaco
    + "("
    + tipos_mercado
    + "){1}"
    + regex_espaco
    + "(FII\s.*)(?:\w{4}\d{2})((?:(\s)?)CI)"
    + regex_espaco
    + "(?:"
    + tipos_temporarios_acoes
    + ")?"
    + regex_espaco
    + "(?:"
    + tipos_observacoes
    + ")*"
    + regex_espaco
    + "(\d+){1}"
    + regex_espaco
    + "(\d+,\d+){1}"
    + regex_espaco
    + "(.+\d+,\d+){1}"
    + regex_espaco
    + "(D|C){1}"
)


def arquivos_pdf_2_df(arquivos):
    # path_notas = "./xp"
    # arquivos = []
    # for filename in Path(path_notas).rglob("*.pdf"):
    #     arquivos.append(filename)

    operacoes_para_o_excel = []

    for path_nota in arquivos:
        pdf = pdfplumber.open(path_nota)
        for pagina in pdf.pages:
            # Número da nota, data da nota
            nota = pagina.crop((400, 0, pagina.width, 100))
            textos = nota.extract_text().split("\n")
            numero_nota = textos[1].split(" ")[0] + "-" + textos[1].split(" ")[1]
            data_nota = textos[1].split(" ")[2]

            # print(f"Nota: {numero_nota}")
            # print(f"Data: {data_nota}")

            # Operações
            operacoes = pagina.crop((0, 250, pagina.width, pagina.height - 400))
            table_settings = {
                "vertical_strategy": "lines",
                "horizontal_strategy": "text",
                "snap_y_tolerance": 5,
                "intersection_x_tolerance": 5,
            }
            textos = operacoes.extract_text().split("\n")

            # Valor total
            total = pagina.crop(
                (300, pagina.height - 200, pagina.width, pagina.height - 195)
            )
            valor_total = total.extract_text().split("\n")
            valor_total = " ".join(valor_total).split(" ")[3]
            valor_total = float(valor_total.replace(".", "").replace(",", "."))
            print(f"Total: {valor_total}")

            valor_das_operacoes = 0
            for o in textos:
                nova_linha = re.split(regex_fii, o)
                nova_linha = list(filter(lambda x: x != None, nova_linha))
                nova_linha = list(filter(lambda x: len(x.strip()) > 0, nova_linha))
                nova_linha = list(map(lambda x: x.strip(), nova_linha))
                valor_das_operacoes += float(
                    nova_linha[7].replace(".", "").replace(",", ".")
                )

            for o in textos:
                nova_linha = re.split(regex_fii, o)
                nova_linha = list(filter(lambda x: x != None, nova_linha))
                nova_linha = list(filter(lambda x: len(x.strip()) > 0, nova_linha))
                nova_linha = list(map(lambda x: x.strip(), nova_linha))
                nova_linha.append(numero_nota)  # 9
                nova_linha.append(data_nota)  # 10
                nova_linha.append(valor_total)  # 11
                nova_linha.append(valor_das_operacoes)  # 12
                # print(f"Operacoes: {nova_linha}")
                # print(nova_linha[5])
                nova_linha[5] = int(nova_linha[5])
                nova_linha[6] = float(nova_linha[6].replace(".", "").replace(",", "."))
                nova_linha[7] = float(nova_linha[7].replace(".", "").replace(",", "."))
                nova_linha.append(nova_linha[7] / valor_das_operacoes)  # 13
                nova_linha.append(nova_linha[13] * valor_total)
                operacoes_para_o_excel.append(nova_linha)

            # print(f"Novas Operacoes: {novas_operacoes}")

    # Create the pandas DataFrame
    df = pd.DataFrame(
        operacoes_para_o_excel,
        columns=[
            "Negociação",
            "C/V",
            "Tipo mercado",
            "Especificação do título",
            "Obs. (*)",
            "Quantidade",
            "Preço/Ajuste",
            "Valor Operação/Ajuste",
            "D/C",
            "Nota",
            "Data",
            "Valor total nota",
            "Valor das operações",
            "Percentual",
            "Valor Op+Taxas",
        ],
    )

    df.drop(columns=["Negociação", "Tipo mercado", "Obs. (*)", "D/C"], inplace=True)
    return df


def df_2_excel(df, nome_arquivo):
    # import uuid
    # myuuid = str(uuid.uuid4())
    # nome_arquivo_final = nome_arquivo + "_" + myuuid + ".xlsx"
    import io

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        for ticker in df["Especificação do título"].unique():
            df[df["Especificação do título"] == ticker].to_excel(
                writer, sheet_name=str(ticker)
            )

        df_total = pd.DataFrame(df["Especificação do título"].unique())
        df_total.to_excel(writer, sheet_name="TOTAIS")

    return buffer

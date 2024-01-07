"""Módulo utilitário para data e hora"""

from datetime import date, datetime
from typing import Any, Tuple

from workalendar.america import Brazil


class DataHoraUtils:
    """Classe utilitária para data e hora"""

    FORMATO_DATA_AMERICANA_HIFEN = "%Y-%m-%d"
    FORMATO_DATA_BRASILEIRA_BARRA = "%d/%m/%Y"

    def __init__(self):
        """Vazio"""

    @staticmethod
    def retorna_data_atual_formato_ddmmyyyy() -> str:
        """Retorna a data atual no formado DD/MM/YYYY"""
        return date.today().strftime(DataHoraUtils.FORMATO_DATA_BRASILEIRA_BARRA)

    @staticmethod
    def retorna_data_formato_ddmmyyyy(data_informada: datetime) -> str:
        """Retorna a data informada no formado DD/MM/YYYY"""
        return data_informada.strftime(DataHoraUtils.FORMATO_DATA_BRASILEIRA_BARRA)

    @staticmethod
    def retornar_feriados_no_brasil() -> Tuple[Any]:
        """Retorna os feriados no Brasil para os próximos 15 anos"""
        data_atual = datetime.today()
        ano_atual = data_atual.year

        cal = Brazil()
        feriados_brasil = []
        for i in range(ano_atual, ano_atual + 15):
            feriados_brasil_raw = cal.holidays(i)
            for j in feriados_brasil_raw:
                feriados_brasil.append(j)

        feriados_brasil = list(zip(*feriados_brasil))[0]
        return feriados_brasil

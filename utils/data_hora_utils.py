from datetime import date, datetime
from workalendar.america import Brazil

class DataHoraUtils:
    def __init__(self):
        pass
    
    @staticmethod
    def retorna_data_atual_formato_ddmmyyyy():
        return date.today().strftime('%d/%m/%Y')

    @staticmethod
    def retorna_data_formato_ddmmyyyy(data_informada):
        return data_informada.strftime("%d/%m/%Y")
    
    def retornar_feriados_no_brasil():
        data_atual = datetime.today()
        ano_atual = data_atual.year
        dias_semana = {"SEGUNDA": 0, "TERCA": 1, "QUARTA": 2, "QUINTA": 3, "SEXTA": 4, "SABADO": 5, "DOMINGO": 6}

        cal = Brazil()
        feriados_brasil = []
        for i in range(ano_atual, ano_atual+15):
            feriados_brasil_raw = cal.holidays(i)
            for j in feriados_brasil_raw:
                feriados_brasil.append(j)

        feriados_brasil = (list(zip(*feriados_brasil))[0])
        return feriados_brasil
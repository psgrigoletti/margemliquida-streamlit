from datetime import date

class DataHoraUtils:
    def __init__(self):
        pass
    
    @staticmethod
    def retorna_data_atual_formato_ddmmyyyy():
        return date.today().strftime('%d/%m/%Y')

    @staticmethod
    def retorna_data_formato_ddmmyyyy(data_informada):
        return data_informada.strftime("%d/%m/%Y")
    
print(DataHoraUtils.retorna_data_atual_formato_ddmmyyyy())
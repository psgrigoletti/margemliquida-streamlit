"""Testes do módulo utils"""
import unittest
from datetime import datetime

from src.utils.data_hora_utils import DataHoraUtils


class TestClassificador(unittest.TestCase):
    """TestClassificador _summary_

    Args:
        unittest (_type_): _description_
    """

    def test_inicial(self):
        """Teste inicial"""
        assert "teste".upper() == "TESTE", "Teste sempre correto"

    def test_retorna_data_atual_formato_ddmmyyyy(self):
        """Teste para classe utilitária DataHoraUtils"""
        data = DataHoraUtils.retorna_data_atual_formato_ddmmyyyy()
        assert len(data) == 10
        assert data is not None

    def test_retorna_data_formato_ddmmyyyy(self):
        """Teste para classe utilitária DataHoraUtils"""
        data = DataHoraUtils.retorna_data_formato_ddmmyyyy(datetime.now())
        assert len(data) == 10
        assert data is not None

    def test_igualdade_de_datas(self):
        """Teste para classe utilitária DataHoraUtils"""
        data1 = DataHoraUtils.retorna_data_formato_ddmmyyyy(datetime.now())
        data2 = DataHoraUtils.retorna_data_atual_formato_ddmmyyyy()
        assert data1 == data2

    def test_retornar_feriados_no_brasil(self):
        """Teste para classe utilitária DataHoraUtils"""
        lista = DataHoraUtils.retornar_feriados_no_brasil()
        assert len(lista) > 0
        assert lista is not None

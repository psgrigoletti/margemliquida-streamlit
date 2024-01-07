"""Testes do módulo utils"""
from src.utils.data_hora_utils import DataHoraUtils


def test_inicial():
    """Teste inicial"""
    assert "teste".upper() == "TESTE", "Teste sempre correto"


def test_retorna_data_atual_formato_ddmmyyyy():
    """Teste para classe utilitária DataHoraUtils"""
    assert len(DataHoraUtils.retorna_data_atual_formato_ddmmyyyy()) == 10
    assert DataHoraUtils.retorna_data_atual_formato_ddmmyyyy() is not None


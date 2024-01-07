from typing import List
import unittest


class ItemClassificar:
    def __init__(self, ticker, valor, classificao=None):
        self.ticker = ticker
        self.valor = valor
        self.classificao = classificao

    def __str__(self):
        return f"{self.ticker}: {self.valor}, classificao {self.classificao}"

    def __eq__(self, other):
        return (
            self.ticker == other.ticker
            and self.valor == other.valor
            and self.classificao == other.classificao
        )


def retornar_lista_inicial():
    return [
        ItemClassificar("ACAO1", 10.5),
        ItemClassificar("ACAO2", 5.3),
        ItemClassificar("ACAO3", 1.1),
        ItemClassificar("ACAO4", 4.1),
        ItemClassificar("ACAO5", 11.1),
        ItemClassificar("ACAO6", 1.1),
    ]


def retornar_lista_asc():
    return [
        ItemClassificar("ACAO1", 10.5, "5 lugar"),
        ItemClassificar("ACAO2", 5.3, "4 lugar"),
        ItemClassificar("ACAO3", 1.1, "1 lugar"),
        ItemClassificar("ACAO4", 4.1, "3 lugar"),
        ItemClassificar("ACAO5", 11.1, "6 lugar"),
        ItemClassificar("ACAO6", 1.1, "1 lugar"),
    ]


def retornar_lista_desc():
    return [
        ItemClassificar("ACAO1", 10.5, "2 lugar"),
        ItemClassificar("ACAO2", 5.3, "3 lugar"),
        ItemClassificar("ACAO3", 1.1, "5 lugar"),
        ItemClassificar("ACAO4", 4.1, "4 lugar"),
        ItemClassificar("ACAO5", 11.1, "1 lugar"),
        ItemClassificar("ACAO6", 1.1, "5 lugar"),
    ]


def classificar_numeros(lista: List[ItemClassificar], ordem):
    for item in lista:
        quantos = 0
        lista_sem_o_item = lista.copy()
        lista_sem_o_item.remove(item)
        for item2 in lista_sem_o_item:
            if (ordem == "ASC" and item2.valor < item.valor) or (
                ordem == "DESC" and item2.valor > item.valor
            ):
                quantos += 1
        item.classificao = f"{quantos+1} lugar"
    return lista


class TestClassificador(unittest.TestCase):
    def test_ordem_asc(self):
        lista = retornar_lista_inicial()
        # menor->maior, menor eh o campeão
        resultado = classificar_numeros(lista, "ASC")
        self.assertEqual(resultado, retornar_lista_asc())

    def test_ordem_desc(self):
        lista = retornar_lista_inicial()
        resultado = classificar_numeros(lista, "DESC")  # maior eh o campeão
        self.assertEqual(resultado, retornar_lista_desc())


# if __name__ == '__main__':
#     unittest.main()


# print(xpi.analise("cyre3"))

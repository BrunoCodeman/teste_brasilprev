import rules
import aiounittest
from models import Jogador, Propriedade, PERSONALIDADES


class MonopolyTest(aiounittest.AsyncTestCase):

    async def test_must_pay_rent(self):
        valor_compra = 100
        valor_aluguel = 10
        _j1 = Jogador(personalidade=PERSONALIDADES[0])
        _j2 = Jogador(personalidade=PERSONALIDADES[0])
        _p = Propriedade(valor_compra, valor_aluguel, _j2)
        await rules.pagar_aluguel(_j1, _p)
        self.assertEqual(_j1.saldo, 290)
        self.assertEqual(_j2.saldo, 310)


    async def test_must_buy_property_if_impulsive_and_has_money(self):
        _j1 = Jogador(personalidade=PERSONALIDADES[0])
        _p = Propriedade(valor_compra=300, valor_aluguel=150)
        await rules.comprar_propriedade(_j1, _p)
        self.assertEqual(_j1.propriedades[0], _p)
        self.assertEqual(_p.dono, _j1)


    async def test_must_buy_property_if_picky_and_rent_value_greater_than_50_and_has_money(self):
        _j1 = Jogador(personalidade=PERSONALIDADES[1])
        _p = Propriedade(valor_compra=300, valor_aluguel=150)
        await rules.comprar_propriedade(_j1, _p)
        self.assertEqual(_j1.propriedades[0], _p)
        self.assertEqual(_p.dono, _j1)


    async def test_must_buy_property_if_cautious_and_balance_is_80_and_has_money(self):
        _j1 = Jogador(personalidade=PERSONALIDADES[2])
        _p = Propriedade(valor_compra=220, valor_aluguel=150)
        await rules.comprar_propriedade(_j1, _p)
        self.assertEqual(_j1.propriedades[0], _p)
        self.assertEqual(_p.dono, _j1)
        self.assertEqual(_j1.saldo, 80)
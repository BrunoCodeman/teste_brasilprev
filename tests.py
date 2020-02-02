import rules
import aiounittest
from models import Jogador, Propriedade, PERSONALIDADES


class MonopolyTest(aiounittest.AsyncTestCase):

    async def test_must_pay_rent(self):
        valor_compra = 100
        valor_aluguel = 10
        _j1 = Jogador(personalidade=PERSONALIDADES[0])
        _j2 = Jogador(personalidade=PERSONALIDADES[0])
        _p = Propriedade(valor_compra=valor_compra, valor_aluguel=valor_aluguel, dono=_j2)
        rules.pagar_aluguel(_j1, _p)
        self.assertEqual(_j2.saldo, 310)
        self.assertEqual(_j1.saldo, 290)


    async def test_must_buy_property_if_impulsive_and_has_money(self):
        _j1 = Jogador(personalidade=PERSONALIDADES[0])
        _p = Propriedade(valor_compra=300, valor_aluguel=150)
        rules.comprar_propriedade(_j1, _p)
        self.assertEqual(_j1.propriedades[0], _p)
        self.assertEqual(_p.dono, _j1)


    async def test_must_buy_property_if_picky_and_rent_value_greater_than_50_and_has_money(self):
        _j1 = Jogador(personalidade=PERSONALIDADES[1])
        _p = Propriedade(valor_compra=300, valor_aluguel=150)
        rules.comprar_propriedade(_j1, _p)
        self.assertEqual(_j1.propriedades[0], _p)
        self.assertEqual(_p.dono, _j1)


    async def test_must_buy_property_if_cautious_and_balance_is_80_and_has_money(self):
        _j1 = Jogador(personalidade=PERSONALIDADES[2])
        _p = Propriedade(valor_compra=220, valor_aluguel=150)
        rules.comprar_propriedade(_j1, _p)
        self.assertEqual(_j1.propriedades[0], _p)
        self.assertEqual(_p.dono, _j1)
        self.assertEqual(_j1.saldo, 80)


    async def test_must_walk_many_steps(self):
        _j = Jogador(personalidade=PERSONALIDADES[0])
        steps = 6
        rules.andar_casas(_j, steps)
        self.assertEqual(_j.posicao, steps)


    async def test_must_go_to_the_beginning_of_the_board_after_20th_step(self):
        _j = Jogador(personalidade=PERSONALIDADES[0])
        _j.posicao = 19
        steps = 3
        expected = (_j.posicao + steps) - 21
        rules.andar_casas(_j, steps)
        self.assertEqual(_j.posicao, expected)


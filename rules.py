import numpy as np
from typing import List
from random import randint, shuffle, choice
from models import Jogador, Propriedade, PERSONALIDADES


def ordenar_por_saldo(jogadores: List[Jogador]) -> List[Jogador]:
    """
    Ordena a lista de jogadores por valor de saldo

    Params:
    - jogadores: A lista de jogadores do jogo atual

    Returns:
    A mesma lista, ordenada por valor de saldo, do maior para o menor
    """
    return sorted(jogadores, key=lambda x: x.saldo, reverse=True)
    

def turno(jogador: Jogador, propriedades: List[Propriedade]):
    """
    Executa o turno de um jogador. Rola o dado, anda o
    número de casas necessárias, compra um imóvel ou
    para o aluguel de acordo com as regras estabelecidas.

    Params:
    - Jogador: O jogador deste turno
    - Propriedades: A lista de propriedades do jogo
    """
    if jogador.saldo > 0:
        numero_dado = rolar_dado()
        andar_casas(jogador, numero_dado)
        propriedade = propriedades[jogador.posicao]
        comprar_propriedade(jogador, propriedade)
        pagar_aluguel(jogador, propriedade)
    else:
        for p in jogador.propriedades:
            p.dono = None 
        jogador.propriedades = []


def atualizar_saldo_fim_tabuleiro(jogador: Jogador) -> Jogador:
    """
    Atualiza o saldo do jogador ao completar a volta no tabuleiro

    Params:
    - Jogador: O jogador que deverá ter seu saldo atualizado

    Returns:
    O jogador com o saldo atualizado
    """
    jogador.saldo+=100
    return jogador


def andar_casas(jogador: Jogador, casas: int) -> Jogador:
    """
    Atualiza a posição do jogador de acordo com o número no dado

    Params:
    - Jogador: O jogador do turno
    - Casas: A quantidade de casas a andar

    Returns:
    O jogador com a posição atualizada
    """
    total = jogador.posicao + casas
    if jogador.posicao == 0:
        jogador.posicao = total
    else:
        if total < 20:
            jogador.posicao = total
        else:        
            jogador.posicao = total-21
            atualizar_saldo_fim_tabuleiro(jogador)
    return jogador


def saldo_positivo(jogador: Jogador) -> Jogador:
    """
    Verifica se o jogador tem o saldo positivo

    Returns:
    - O jogador caso tenha saldo positivo, ou nulo.
    """
    return jogador if jogador.saldo > 0 else None


def vencedor(lista_jogadores: list) -> Jogador:
    """
    Verifica se há um vencedor do jogo

    Returns:
    - O vencedor do jogo caso exista, ou nulo
    """
    jogadores_no_pareo = list(filter(saldo_positivo, lista_jogadores))
    return jogadores_no_pareo[0] if len(jogadores_no_pareo) == 1 else None


def rolar_dado() -> int:
    """
    Rola o D6 para movimentação do jogador

    Returns:
    - Um número entre 1 e 6 para que o jogador ande casas
    """
    return randint(1, 6)


async def criar_jogadores() -> List[Jogador]:
    """
    Cria 4 jogadores para uma nova partida

    Returns:
    - Uma lista com  4 objetos da classe Jogador
    """
    jogadores = []
    for i in range(0, 4):
        jogadores.append(Jogador(personalidade=PERSONALIDADES[i]))
    
    shuffle(jogadores)
    return jogadores


async def criar_propriedades() -> List[Propriedade]:
    """
    Cria 20 propriedades para uma nova partida

    Returns:
    - Uma lista com  20 objetos da classe Propriedade
    """
    propriedades = []
    for i in range(0, 20):
        valor = randint(0, 300)
        aluguel = randint(0, valor - 1)
        prop = Propriedade(valor_aluguel=aluguel, valor_compra=valor)
        propriedades.append(prop)
    return propriedades


def pagar_aluguel(jogador: Jogador, propriedade: Propriedade)-> Jogador:
    """
    Cobra o aluguel de uma propriedade quando um jogador passa por ela
    Params:
    - jogador: O jogador a ser cobrado.
    - propriedade: Propriedade na qual o jogador parou.

    Returns:
    - O jogador que pagou o aluguel, com seu saldo atualizado.
    """
    if(propriedade.dono != jogador and propriedade.dono is not None):
        saldo_inquilino = jogador.saldo - propriedade.valor_aluguel
        saldo_proprietario = propriedade.dono.saldo + propriedade.valor_aluguel
        jogador.saldo = saldo_inquilino
        propriedade.dono.saldo = saldo_proprietario
    return jogador


def comprar_propriedade(jogador: Jogador, propriedade: Propriedade) -> (Jogador, Propriedade):
    """
    Efetua a venda da propriedade de acordo com o saldo e o perfil do jogador
    e caso a propriedade não tenha dono.

    Params:
    - jogador: O jogador que pretende comprar a propriedade
    - propriedade: A propriedade a ser adquirida pelo jogador

    Returns:
    Uma tupla (jogador, propriedade) com os resultados finais da operação.
    Caso não haja venda, o retorno é igual aos parâmetros de entrada.
    """
    tem_saldo_para_comprar = jogador.saldo >= propriedade.valor_compra
    propriedade_nao_tem_dono = propriedade.dono is None

    if tem_saldo_para_comprar and propriedade_nao_tem_dono:
        saldo_final_jogador = jogador.saldo - propriedade.valor_compra
        if jogador.personalidade == "impulsivo":
            jogador.saldo = saldo_final_jogador
            jogador.propriedades.append(propriedade)
            propriedade.dono = jogador

        if jogador.personalidade == "exigente":
            if propriedade.valor_aluguel > 50:
                jogador.saldo = saldo_final_jogador
                jogador.propriedades.append(propriedade)
                propriedade.dono = jogador

        if jogador.personalidade == "cauteloso":
            if saldo_final_jogador == 80:
                jogador.saldo = saldo_final_jogador
                jogador.propriedades.append(propriedade)
                propriedade.dono = jogador

        if jogador.personalidade == "aleatório":
            np.random.seed(0)
            _choice = np.random.choice(11)
            print(f"random choice - {choice}")
            if choice([0, 1]) == 1:
                jogador.saldo = saldo_final_jogador
                jogador.propriedades.append(propriedade)
                propriedade.dono = jogador

    return jogador, propriedade

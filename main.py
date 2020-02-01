import asyncio
import uvloop
import rules


async def start_game():
    rodada = 0
    propriedades = await rules.criar_propriedades()
    jogadores = await rules.criar_jogadores()
    while rules.vencedor(jogadores) is None:
        max_size = len(jogadores) -1
        rodada+=1
        for i in range(0, max_size):
            jogador = jogadores[i]
            await rules.turno(jogador, propriedades)
        if rodada >= 1_000:
            break #terminar jogo
        print([jogador.saldo for jogador in jogadores])
    else:
        print([jogador.saldo for jogador in jogadores])
        print(rules.vencedor(jogadores))


if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [asyncio.ensure_future(start_game())]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    


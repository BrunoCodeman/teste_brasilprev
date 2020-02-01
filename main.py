import asyncio
import uvloop
import rules


async def start_game():
    rodada = 0
    vencedor = None
    try:
        propriedades = await rules.criar_propriedades()
        jogadores = await rules.criar_jogadores()
        while rules.vencedor(jogadores) is None:
            max_size = len(jogadores) -1
            rodada+=1
            for i in range(0, max_size):
                jogador = jogadores[i]
                rules.turno(jogador, propriedades)
            if rodada >= 1_000:
                print("GAME OVER! \n")
                ordem_final = rules.ordenar_por_saldo(jogadores)
                vencedor = ordem_final[0]
                print("Placar final\n")
                for jogador in ordem_final:
                    print(f"{jogador}\n")
                break #terminar jogo
        else:
            vencedor = rules.vencedor(jogadores)
        print(f"Vencedor - {vencedor}")
        
    except Exception as e:
        print(f"Error - {e}, starting again \n\n")
        await asyncio.sleep(3)
        await start_game()
        


if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [asyncio.ensure_future(start_game())]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    


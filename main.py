import sys, os
import asyncio
import uvloop
import rules
from models import PERSONALIDADES

def calcular_porcentagem_vencedores(jogadores: dict) -> dict:
    perfis_vencedores = { k:0 for k in PERSONALIDADES}
    for k,v in jogadores.items():
        perfis_vencedores[k] = (v*100)/300
    return perfis_vencedores

async def main():
    total_simulacoes = 300
    data = {"timeouts": 0, "rodadas":0, "perfis_vencedores":  { k:0 for k in PERSONALIDADES} }
    max_range = total_simulacoes+1
    for i in range(0, max_range):
        # {"timeout": timeout, "rodadas": rodada, "vencedor": vencedor}
        result = await start_game()
        data["rodadas"]+= result["rodadas"]
        data["perfis_vencedores"][result["vencedor"]]+=1
        if result["timeout"]:
            data["timeouts"]+=1
    ordem_vencedores = {k: v for k, v in sorted(data["perfis_vencedores"].items(), key=lambda item: item[1])}
    maior_vencedor =  list(ordem_vencedores.keys())[-1]
    print(f"Timeouts: {data['timeouts']}\n")
    print(f"Média de turnos - {data['rodadas']/300}\n")
    print("Percentual de vitórias por perfil")
    print(f"{calcular_porcentagem_vencedores(data['perfis_vencedores'])}\n\n")
    print(f"Maior vencedor - {maior_vencedor} ({data['perfis_vencedores'][maior_vencedor]} vitórias)")
    

async def start_game():
    rodada = 0
    vencedor = None
    timeout = False
    result = {}
    try:
        propriedades = await rules.criar_propriedades()
        jogadores = await rules.criar_jogadores()
        while rules.vencedor(jogadores) is None:
            rodada+=1
            max_size = len(jogadores) -1
            turnos = range(0, max_size)
            for i in turnos:
                jogador = jogadores[i]
                rules.turno(jogador, propriedades)
            if rodada >= 1_000:
                timeout = True
                ordem_final = rules.ordenar_por_saldo(jogadores)
                vencedor = ordem_final[0]
                break #terminar jogo
        else:
            vencedor = rules.vencedor(jogadores)
        result = {"timeout": timeout, "rodadas": rodada, "vencedor": vencedor.personalidade}
    except Exception as e:
        print(f"Error - {e}")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        result = await start_game()
    finally:
        return result
        


if __name__ == '__main__':
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [asyncio.ensure_future(main())]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    


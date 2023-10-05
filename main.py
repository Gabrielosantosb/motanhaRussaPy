import threading
import time
import random

# Parâmetros
n = 10  # Número de passageiros
m = 3   # Número de carros (agora com 3 carros)
C = 5   # Capacidade de cada carro
Te = 2  # Tempo de embarque/desembarque em segundos (reduzido para simplificar a simulação)
Tm = 5  # Tempo de passeio em segundos (1 minuto)
Tp = 2  # Intervalo de chegada dos passageiros em segundos (reduzido para simplificar a simulação)

# Semáforos
embarque_sem = threading.Semaphore(0)      # Controla o embarque no carro
passeio_sem = threading.Semaphore(0)       # Controla o início do passeio
desembarque_sem = threading.Semaphore(0)   # Controla o desembarque do carro
mutex = threading.Semaphore(1)             # Mutex para garantir exclusão mútua ao imprimir

# Variáveis globais
passageiros_na_fila = 0
carro_atual = 1  # Carro atualmente em ação (inicia com o Carro 1)
carro_em_movimento = [False] * (m + 1)  # Lista para acompanhar o estado de cada carro
passageiros_curtiram = 0

def passageiro(id):
    global passageiros_na_fila

    # Entra na fila de espera
    passageiros_na_fila += 1
    print(f"[{time.time()}] - Passageiro {id} chegou. Passageiros na fila: {passageiros_na_fila}")

    # Espera para embarcar
    embarque_sem.acquire()
    print(f"[{time.time()}] - Passageiro {id} embarcou no Carro {carro_atual}.")
    
    # Espera pelo passeio
    passeio_sem.acquire()
    print(f"[{time.time()}] - Passageiro {id} está curtindo o passeio.")
    global passageiros_curtiram
    passageiros_curtiram += 1

def carro(id):
    global passageiros_na_fila, carro_atual, carro_em_movimento

    while True:
        # Espera até que o carro esteja cheio e seja sua vez
        while passageiros_nafila < C or carro_atual != id:
            pass

        # Inicia o embarque
        print(f"[{time.time()}] - Carro {id} começou o embarque.")
        for _ in range(C):
            embarque_sem.release()
            passageiros_na_fila -= 1

        # Inicia o passeio
        print(f"[{time.time()}] - Carro {id} começou o passeio.")
        carro_em_movimento[id] = True
        time.sleep(Tm)  # Simula o passeio
        carro_em_movimento[id] = False

        # Libera os passageiros para desembarcar
        for _ in range(C):
            desembarque_sem.release()

        # Muda para o próximo carro
        carro_atual = (carro_atual % m) + 1

        # Verifica se todos os passageiros curtiram o passeio
        if passageiros_curtiram == n:
            print("Todos os passageiros curtiram o passeio. Encerrando o programa.")
            return

if __name__ == "__main__":
    # Inicia a thread de cada carro
    carros_threads = []
    for i in range(1, m + 1):  # Começando em 1 para evitar Carro 0
        carro_thread = threading.Thread(target=carro, args=(i,))
        carros_threads.append(carro_thread)
        carro_thread.start()

    # Inicia as threads dos passageiros
    passageiros_threads = []
    for i in range(1, n + 1):  # Começando em 1 para evitar Passageiro 0
        passageiro_thread = threading.Thread(target=passageiro, args=(i,))
        passageiros_threads.append(passageiro_thread)
        time.sleep(random.uniform(0, Tp))  # Intervalo aleatório de chegada dos passageiros
        passageiro_thread.start()

    # Aguarda todas as threads de passageiros terminarem
    for thread in passageiros_threads:
        thread.join()

    # Termina as threads dos carros
    for thread in carros_threads:
        thread.join()

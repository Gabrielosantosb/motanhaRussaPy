import threading
import time
from collections import deque

# Parâmetros
n = 10  # Número de passageiros
m = 3   # Número de carros (agora com 3 carros)
C = 5   # Capacidade de cada carro
Te = 5  # Tempo de embarque/desembarque em segundos
Tm = 5  # Tempo de passeio em segundos (1 minuto)
Tp = 5  # Intervalo de chegada dos passageiros em segundos

# Semáforos
embarque_sem = threading.Semaphore(0)  # Controla o embarque no carro
passeio_sem = threading.Semaphore(0)   # Controla o início do passeio
desembarque_sem = threading.Semaphore(0)  # Controla o desembarque do carro
carro_atual_sem = threading.Semaphore(1)  # Controla qual carro está atualmente em ação
ordem_embarque_sem = threading.Semaphore(0)  # Controla a ordem de embarque dos carros

# Fila de espera dos passageiros
fila_de_espera = deque()

# Variáveis globais
carro_em_movimento = [False] * (m + 1)  # Lista para acompanhar o estado de cada carro
passageiros_curtiram = 0

def passageiro(passageiroId):
    global passageiros_curtiram

    # Entra na fila de espera
    fila_de_espera.append(passageiroId)
    print(f"[{time.time()}] - Passageiro {passageiroId} chegou. Passageiros na fila: {len(fila_de_espera)}")

    # Espera para embarcar
    embarque_sem.acquire()
    carro_atual_sem.acquire()
    carro_id = carro_em_movimento.index(False)  # Encontra o primeiro carro disponível
    print(f"[{time.time()}] - Passageiro {passageiroId} embarcou no Carro {carro_id}.")
    carro_atual_sem.release()
    embarque_sem.release()

    # Espera pelo passeio
    passeio_sem.acquire()
    print(f"[{time.time()}] - Passageiro {passageiroId} está curtindo o passeio.")
    passageiros_curtiram += 1

def carro(carroId):
    global passageiros_curtiram

    while True:
        # Aguarda a ordem de embarque
        ordem_embarque_sem.acquire()

        # Espera até que o carro esteja cheio ou não haja mais passageiros
        while len(fila_de_espera) > 0 and passageiros_curtiram < n:
            passageiro_id = fila_de_espera.popleft()
            print(f"[{time.time()}] - Carro {carroId} embarcou Passageiro {passageiro_id}")
            embarque_sem.release()
            time.sleep(Te)  # Simula o tempo de embarque

        # Inicia o passeio
        print(f"[{time.time()}] - Carro {carroId} começou o passeio.")
        carro_em_movimento[carroId] = True
        time.sleep(Tm)  # Simula o passeio
        carro_em_movimento[carroId] = False

        # Inicia o desembarque
        print(f"[{time.time()}] - Carro {carroId} retornou e começou o desembarque.")
        for _ in range(C):
            desembarque_sem.release()

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

    # Inicia as threads dos passageiros
    passageiros_threads = []
    for i in range(1, n + 1):  # Começando em 1 para evitar Passageiro 0
        passageiro_thread = threading.Thread(target=passageiro, args=(i,))
        passageiros_threads.append(passageiro_thread)

    # Inicia as threads dos carros
    for thread in carros_threads:
        thread.start()

    # Espera um tempo para permitir que os carros se inicializem
    time.sleep(2)

    # Inicia as threads

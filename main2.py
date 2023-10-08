import threading
import time

# Variáveis de controle
trava_check_in = threading.Lock()
trava_corrida = threading.Lock()

fila_embarque = threading.Semaphore(0)  # sinalizar que os passageiros podem embarcar
todos_embarcaram = threading.Semaphore(0)  # sinalizar que todos os passageiros embarcaram
fila_desembarque = threading.Semaphore(0)  # sinalizar que os passageiros podem desembarcar
todos_desembarcaram = threading.Semaphore(0)  # sinalizar que todos os passageiros desembarcaram
semaforo_carro = threading.Semaphore(1)  # controlar o acesso ao carro (1 carro por vez)

# Variáveis da montanha-russa
embarcados = 0  # Contador de passageiros embarcados no carro atual
desembarcados = 0  # Contador de passageiros desembarcados do carro atual
corrida_atual = 0  # Contador de corridas
total_corridas = 0  # Contador total de corridas

# Informações carros e passageiros
carros = []  
id_carro = 0 
id_passageiro = 0  
passageiros = 0  
capacidade_carro = 0 
passageiros_concluidos = 0 
passageiros_na_fila = 0 


def getTime():
    return time.strftime("%H:%M:%S")


def carregar():
    print('--------------------------------------------------------------------------')
    print(f"Total de passageiros na fila: {passageiros_na_fila}")
    print(f"Total de carros: {carros}")
    print(f"Capacidade do carro: {capacidade_carro}")
    time.sleep(2)
    print('--------------------------------------------------------------------------')


def iniciar_corrida():
    global id_carro
    print(f"[{getTime()}] Carro lotado, pronto para o passeio!")
    time.sleep(2)
    print(f"[{getTime()}] O carro #{id_carro} está na corrida!")
    time.sleep(5)


def descarregar():
    print(f"[{getTime()}] A corrida terminou, vamos desembarcar!")
    time.sleep(2)


def embarcar():
    global embarcados
    print(f"[{getTime()}] {embarcados} passageiros embarcaram no carro...")
    time.sleep(1)


def desembarcar():
    global desembarcados, passageiros, passageiros_concluidos, passageiros_na_fila
    print(f"[{getTime()}] Passageiro #{desembarcados} desembarcou do carro...")
    passageiros_concluidos += 1
    passageiros_na_fila -= 1
    
    time.sleep(1)


# -----------------------------------------------
# Funções de Thread

def thread_carro():
    global corrida_atual, id_carro, carros, capacidade_carro, passageiros_na_fila

    while passageiros_concluidos != passageiros:
        carregar()
        id_carro = carros[corrida_atual % len(carros)]
        corrida_atual += 1

        print(f"[{getTime()}] Corrida #{corrida_atual}")
        print(f"[{getTime()}] Carro #{id_carro} está indo para a corrida, vamos embarcar os passageiros!")

        if passageiros_na_fila < capacidade_carro:
            todos_embarcaram.release()

        for i in range(min(capacidade_carro, passageiros_na_fila)):
            fila_embarque.release()
        todos_embarcaram.acquire()

        iniciar_corrida()
        descarregar()

        for i in range(min(capacidade_carro, passageiros_na_fila)):
            fila_desembarque.release()

        todos_desembarcaram.acquire()
        print(f"[{getTime()}] Carro #{id_carro} está vazio!\n")


def thread_passageiro():
    global id_passageiro, capacidade_carro, passageiros_concluidos, embarcados

    while True:
        fila_embarque.acquire()
        with trava_check_in:
            global embarcados
            embarcados += 1
            id_passageiro += 1
            embarcar()

            if embarcados == capacidade_carro or passageiros_concluidos == passageiros:
                todos_embarcaram.release()
                embarcados = 0
        fila_desembarque.acquire()

        with trava_corrida:
            global desembarcados
            desembarcados += 1
            desembarcar()

            if desembarcados == capacidade_carro or passageiros_concluidos == passageiros:
                todos_desembarcaram.release()
                desembarcados = 0


# -----------------------------------------------

def validar_input():
    global passageiros, capacidade_carro, carros, passageiros_na_fila

    passageiros = int(input("Quantos passageiros?\n"))
    while passageiros <= 0:
        print("Por favor, insira um número de passageiros válido (maior que zero).")
        passageiros = int(input("Quantos passageiros?\n"))

    capacidade_carro = int(input("Qual será a capacidade do carro?\n"))
    while capacidade_carro <= 0:
        print("Por favor, insira uma capacidade de carro válida (maior que zero).")
        capacidade_carro = int(input("Qual será a capacidade do carro?\n"))

    carros = int(input("Quantos carros existem na montanha-russa?\n"))
    while carros <= 0:
        print("Por favor, insira um número de carros válido (maior que zero).")
        carros = int(input("Quantos carros existem na montanha-russa?\n"))

    carros = list(range(1, carros + 1))
    passageiros_na_fila = passageiros


if __name__ == "__main__":
    validar_input()
    print('--------------------------------------------------------------------------')
    print(f"Número de passageiros: {passageiros}")
    print(f"Número de passageiros na fila: {passageiros_na_fila}")
    print(f"Número de carros: {carros}")
    print(f"Capacidade dos carros: {capacidade_carro}")

    thread_carro = threading.Thread(target=thread_carro)
    threads_passageiros = [threading.Thread(
        target=thread_passageiro) for i in range(passageiros)]

    thread_carro.start()
    for thread in threads_passageiros:
        thread.start()

    thread_carro.join()

    print("Todos os passageiros se divertiram! A montanha-russa está fechando...")

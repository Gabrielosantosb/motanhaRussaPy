import threading
import random
import time

# Variáveis de controle
check_in_lock = threading.Lock() 
riding_lock = threading.Lock()   

board_queue = threading.Semaphore(0)      # sinalizar que os passageiros podem embarcar
all_boarded = threading.Semaphore(0)      # sinalizar que todos os passageiros embarcaram
unboard_queue = threading.Semaphore(0)    # sinalizar que os passageiros podem desembarcar
all_unboarded = threading.Semaphore(0)    # sinalizar que todos os passageiros desembarcaram
car_semaphore = threading.Semaphore(1)    # controlar o acesso ao carro (1 carro por vez)

# Variáveis  da montanha-russa
boarded = 0               # Contador de passageiros embarcados no carro atual
unboarded = 0             # Contador de passageiros desembarcados do carro atual
current_ride = 0         # Contador de corridas
total_rides = 0           # Contador total de corridas

# Informações carros e passageiros
cars = []                  # Lista de carros
car_id = 0                 # ID do carro
passenger_id = 0           # ID do passageiro
passengers = 0             # Número total de passageiros
capacity = 0               # Capacidade máxima de cada carro
passengers_completed = 0   # Contador de passageiros que concluíram o passeio
passengersNaFila = 0



def get_time():
    return time.strftime("%H:%M:%S")

def load():
    print('--------------------------------------------------------------------------')        
    print(f"Total de passageiros na fila: {passengersNaFila}")
    print(f"Total de carros: {cars}")
    print(f"Capacidade do carro: {capacity}")
    time.sleep(2)
    print('--------------------------------------------------------------------------')


def run():
    global car_id
    print(f"[{get_time()}]Carrinho lotado, pronto para o passeio!")
    time.sleep(2)
    print(f"[{get_time()}]O carro #{car_id} está no passeio!")
    time.sleep(5)


def unload():
    print(f"[{get_time()}]Acabou o passeio, vamos desembarcar!")
    time.sleep(2)


def board():
    global boarded
    print(f"[{get_time()}]{boarded} embarcaram no carro...")
    time.sleep(random.randint(0, 1))


def unboard():
    global unboarded, passengers, passengers_completed, passengersNaFila
    print(f"[{get_time()}]Passageiro #{unboarded} desembarcou do carro...")
    passengers_completed += 1
    passengersNaFila -= 1
    time.sleep(random.randint(0, 1))

# -----------------------------------------------
# Thread Functions


def car_thread():
    global current_ride, car_id, cars, capacity, passengersNaFila

    while passengers_completed != passengers:
        load()
        car_id = cars[current_ride % len(cars)] 
        current_ride += 1


        print(f"[{get_time()}]Corrida #{current_ride}")
        print(f"[{get_time()}]Carro #{car_id} vai passear, vamos embarcar os passageiros!")
        
        if passengersNaFila < capacity:
            all_boarded.release()
            # board_queue.release()

        for i in range(min(capacity, passengersNaFila)):  
            board_queue.release()
        all_boarded.acquire()

        run()
        unload()

        for i in range(min(capacity, passengersNaFila)):  
            unboard_queue.release()

        all_unboarded.acquire()
        print(f"[{get_time()}]Carro #{car_id} está vazio!\n")
        
def passenger_thread():
    global passenger_id, capacity, pa

    while True:
        board_queue.acquire()

        with check_in_lock:
            global boarded
            boarded += 1
            passenger_id += 1
            board()
            

            if boarded == capacity or passengers_completed == passengers:
                all_boarded.release()
                boarded = 0
        unboard_queue.acquire()

        with riding_lock:
            global unboarded
            unboarded += 1
            unboard()

            if unboarded == capacity or passengers_completed == passengers:
                    all_unboarded.release()
                    unboarded = 0

# -----------------------------------------------
def validateInputs():
    global passengers, capacity, cars, passengersNaFila
    
    passengers = int(input("Quantos passageiros?\n"))
    while passengers <= 0:
        print("Por favor, insira um número de passageiros válido (maior que zero).")
        passengers = int(input("Quantos passageiros?\n"))

    capacity = int(input("Qual vai ser a capacidade do carro?\n"))
    while capacity <= 0:
        print("Por favor, insira uma capacidade de carro válida (maior que zero).")
        capacity = int(input("Qual vai ser a capacidade do carro?\n"))

    cars = int(input("Quantos carros tem na montanha russa?\n"))
    while cars <= 0:
        print("Por favor, insira um número de carros válido (maior que zero).")
        cars = int(input("Quantos carros tem na montanha russa?\n"))
    
    cars = list(range(1, cars + 1))
    passengersNaFila = passengers

if __name__ == "__main__":
    validateInputs()
    print('--------------------------------------------------------------------------')
    print(f"Número de passageiros:{passengers}")
    print(f"Número de passageiros na fila:{passengersNaFila}")
    print(f"Número de carros: {cars}")
    print(f"Capacidade do carros: {capacity}")

    car_thread = threading.Thread(target=car_thread)
    passenger_threads = [threading.Thread(
        target=passenger_thread) for i in range(passengers)]

    car_thread.start()
    for thread in passenger_threads:
        thread.start()

    car_thread.join()
    
    print("Todos os passageiros se divertiram! Montanha russa fechando...")

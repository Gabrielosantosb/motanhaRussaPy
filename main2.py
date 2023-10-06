import threading
import random
import time



# Variables
check_in_lock = threading.Lock()
riding_lock = threading.Lock()

board_queue = threading.Semaphore(0)
all_boarded = threading.Semaphore(0)
unboard_queue = threading.Semaphore(0)
all_unboarded = threading.Semaphore(0)
car_semaphore = threading.Semaphore(1)

boarded = 0
unboarded = 0
current_ride = 0
total_rides = 0

cars = []
car_id = 0
passenger_id = 0
passengers = 0
capacity = 0
passengers_completed = 0



def load():
    print('--------------------------------------------------------------------------')
    # print(f"Carro # vai passear, vamos embarcar os passageiros!")
    print(
        f"Corrida #{current_ride+1} vai começar, vamos embarcar os passageiros!")
    print(f"Total de passageiros na fila: {passengersNaFila}")
    print(f"Capacidade do carro: {capacity}")
    time.sleep(2)
    print('--------------------------------------------------------------------------')


def run():
    print("Carrinho lotado, pronto para o passeio!")
    time.sleep(2)
    print("O carro está no passeio!")
    time.sleep(5)


def unload():
    print("Acabou o passeio, vamos desembarcar!")
    time.sleep(2)


def board():
    global boarded
    print(f"{boarded} embarcaram no carro...")
    time.sleep(random.randint(0, 1))


def unboard():
    global unboarded, passengers, capacity, passengers_completed, passengersNaFila
    print(f"Passageiro #{unboarded} desembarcou do carro...")
    passengers_completed += 1
    passengersNaFila -= 1
    time.sleep(random.randint(0, 1))

# Thread Functions


def car_thread():
    global current_ride, car_id

    while passengers_completed != passengers:
        load()
        car_id += 1  # Atribuir um novo ID de carro
        print(f"Corrida #{current_ride}")
        print(f"Carro #{car_id} vai passear, vamos embarcar os passageiros!")
        
        for _ in range(capacity):
            board_queue.release()

        all_boarded.acquire()

        run()
        unload()

        for _ in range(capacity):
            unboard_queue.release()

        all_unboarded.acquire()
        print(f"Carro #{car_id} está vazio!\n")
        current_ride += 1


def passenger_thread():
    global passenger_id

    while True:
        board_queue.acquire()

        with check_in_lock:
            global boarded
            boarded += 1
            passenger_id += 1  
            board()

            if boarded == capacity:
                all_boarded.release()
                boarded = 0

        unboard_queue.acquire()

        with riding_lock:
            global unboarded
            unboarded += 1
            unboard()

            if unboarded == capacity:
                all_unboarded.release()
                unboarded = 0


if __name__ == "__main__":
    random.seed(time.time())
    # passengers = 2 + random.randint(0, MAX_PASSENGERS)
    # capacity = 1 + random.randint(0, passengers - 1)
    passengers = int(input("Quantos passageiros?\n"))
    capacity = int(input("Qual vai ser a capacidade do carro?\n"))
    cars = int(input("Quantos carros tem na montanha russa?\n"))
    passengersNaFila = passengers
    print('--------------------------------------------------------------------------')
    print(f"Número de passageiros:{passengers}")
    print(f"Número de passageiros na fila:{passengersNaFila}")
    print(f"Número de carros: {cars}")
    print(f"Capacidade do carros: {capacity}")


    car_thread = threading.Thread(target=car_thread)
    passenger_threads = [threading.Thread(
        target=passenger_thread) for _ in range(passengers)]

    car_thread.start()
    for thread in passenger_threads:
        thread.start()

    car_thread.join()
    
    print("Todos os passageiros se divertiram! Montanha russa fechando...")

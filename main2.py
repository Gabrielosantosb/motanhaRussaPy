import threading
import random
import time

MAX_PASSENGERS = 25
MAX_RIDES = 10

# Variables
check_in_lock = threading.Lock()
riding_lock = threading.Lock()

board_queue = threading.Semaphore(0)
all_boarded = threading.Semaphore(0)
unboard_queue = threading.Semaphore(0)
all_unboarded = threading.Semaphore(0)

boarded = 0
unboarded = 0
current_ride = 0
total_rides = 0
passengers = 0
capacity = 0

# Helper functions
def load():
    print(f"Corrida #{current_ride+1} vai começar, vamos embarcar os passageiros!")
    print(f"Capacidade do carro: {capacity}")
    time.sleep(2)

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
    global unboarded
    print(f"{unboarded} desembarcaram do carro...")
    time.sleep(random.randint(0, 1))

# Thread Functions
def car_thread():
    global current_ride
    while current_ride < total_rides:
        load()

        for _ in range(capacity):
            board_queue.release()

        all_boarded.acquire()

        run()
        unload()

        for _ in range(capacity):
            unboard_queue.release()

        all_unboarded.acquire()
        print("O carro está vazio!\n")
        current_ride += 1

def passenger_thread():
    while True:
        board_queue.acquire()

        with check_in_lock:
            global boarded
            boarded += 1
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
    passengers = 2 + random.randint(0, MAX_PASSENGERS)
    capacity = 1 + random.randint(0, passengers - 1)
    total_rides = 1 + random.randint(0, MAX_RIDES)

    car_thread = threading.Thread(target=car_thread)
    passenger_threads = [threading.Thread(target=passenger_thread) for _ in range(passengers)]

    # print(f"Today the roller coaster will ride {total_rides} times!")
    # print(f"There are {passengers} passengers waiting in the roller coaster queue!\n")

    car_thread.start()
    for thread in passenger_threads:
        thread.start()

    car_thread.join()

    print("O maquinista cansou de trabalhar, montanha russa fechando...")

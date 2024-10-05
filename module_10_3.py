import threading
import random
import time

class Bank:
    def __init__(self):
        self.balance = 0  # Начальный баланс
        self.lock = threading.Lock()  # Создание локалки для блокировки потоков

    def deposit(self):
        for _ in range(100):  # 100 транзакций пополнения
            amount = random.randint(50, 500)  # Случайная сумма пополнения
            with self.lock:  # Блокировка для безопасного доступа к балансу
                self.balance += amount
                print(f"Пополнение: {amount}. Баланс: {self.balance}")
                if self.balance >= 500 and self.lock.locked():  # Если баланс >= 500
                    self.lock.release()  # Разблокировать поток (но это не обязательно)
            time.sleep(0.001)  # Имитация времени выполнения транзакции

    def take(self):
        for _ in range(100):  # 100 транзакций снятия
            amount = random.randint(50, 500)  # Случайная сумма снятия
            print(f"Запрос на {amount}")
            with self.lock:  # Блокировка для безопасного доступа к балансу
                if amount <= self.balance:  # Проверка на наличие средств
                    self.balance -= amount
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                else:
                    print("Запрос отклонён, недостаточно средств")
                    # Блокировка потока, если средств недостаточно:
                    # Здесь следует использовать while loop для ожидания разблокировки
                    while not self.lock.locked():
                        self.lock.acquire()

            time.sleep(0.001)  # Имитация времени выполнения транзакции

# Создание объекта класса Bank
bk = Bank()

# Создание двух потоков для методов deposit и take
th1 = threading.Thread(target=bk.deposit)
th2 = threading.Thread(target=bk.take)

# Запуск потоков
th1.start()
th2.start()

# Ожидание завершения потоков
th1.join()
th2.join()

# Вывод итогового баланса
print(f'Итоговый баланс: {bk.balance}')

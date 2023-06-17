import threading
import random
import time

g_money = 0
lock = threading.Lock()


class Product(threading.Thread):
    def run(self):
        global g_money
        for _ in range(10):
            lock.acquire()
            money = random.randint(1000, 10000)
            g_money += money
            print(threading.current_thread().getName(), '挣了{}钱，当前余额为：{}'.format(money, g_money))
            time.sleep(1)
            lock.release()


class Custmer(threading.Thread):
    def run(self) -> None:
        global g_money
        for _ in range(10):
            lock.acquire()
            money = random.randint(1000, 10000)
            if money <= g_money:
                g_money -= money
                print(threading.current_thread().getName(), '花了{}钱，当前余额为：{}'.format(money, g_money))
            else:
                print(threading.current_thread().getName(), '花了{}钱，当前余额不足，为：{}'.format(money, g_money))
            time.sleep(1)
            lock.release()


def start():
    for i in range(5):
        th = Product(name='生产者{}'.format(i))
        th.start()

    for j in range(5):
        cust = Custmer(name='消费者{}'.format(j))
        cust.start()


if __name__ == '__main__':
    start()

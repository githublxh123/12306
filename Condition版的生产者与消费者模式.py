import threading
import random

g_money = 0
lock = threading.Condition()
g_time = 0


class Product(threading.Thread):
    def run(self):
        global g_money
        global g_time
        for _ in range(10):
            lock.acquire()
            money = random.randint(1000, 10000)
            g_money += money
            g_time += 1
            print(threading.current_thread().getName(), '挣了{}钱，当前余额为：{}'.format(money, g_money))
            # time.sleep(1)
            lock.notify_all()
            lock.release()


class Custmer(threading.Thread):
    def run(self) -> None:
        global g_money
        for _ in range(10):
            lock.acquire()
            money = random.randint(1000, 10000)
            while g_money < money:  # 当余额不足的时候
                if g_time >= 50:  # 当生产者已经生产完毕，需要释放锁
                    lock.release()
                    return
                print(threading.current_thread().getName(), '想花{}钱，但是当前余额不足，为：{}'.format(money, g_money))
                lock.wait()  # 余额不足的情况下需要等待消费者的唤醒

            g_money -= money
            print(threading.current_thread().getName(), '花了{}钱，当前余额为：{}'.format(money, g_money))
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

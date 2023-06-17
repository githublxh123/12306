import time
from queue import Queue  # FIFO(先进先出)
import random
import threading


# q = Queue(5)  # 创建一个队列，最多可以存放5个数据


#
# # 向队列中存放数据
# for i in range(4):
#     q.put(i)
#
# print('队列中实际的数据有多少个：', q.qsize())
#
# for _ in range(5):
#     try:
#         print(q.get(block=False))
#     except:
#         print('数据已经取完，队列目前为空')
# if q.full():
#     print('队列已满')
# else:
#     print('队列未满，当前队列的个数为{}'.format(q.qsize()))

def add_value(q):
    while True:
        q.put(random.randint(100, 1000))
        time.sleep(1)


def get_value(q):
    while True:
        print('取出的元素：{}'.format(q.get()))


def start():
    q = Queue(10)
    t1 = threading.Thread(target=add_value, args=(q,))
    t2 = threading.Thread(target=get_value, args=(q,))
    t1.start()
    t2.start()


if __name__ == '__main__':
    start()

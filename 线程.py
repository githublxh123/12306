import time
import threading
# from concurrent.futures import thread


# def fun1():
#     for i in range(5):
#         print('-----fun1中i的值为：', i)
#         time.sleep(1)
#
#
# def fun2():
#     for i in range(5):
#         print('-----fun2中i的值为：', i)
#         time.sleep(1)
#
#
# def single():
#     fun1()
#     fun2()


# def mult():
#     t1 = threading.Thread(target=fun1)
#     t2 = threading.Thread(target=fun2)
#     #启动程序
#     t1.start()
#     t2.start()
#
#
# if __name__ == '__main__':
#     # single()
#     mult()

# class CodingThread(threading.Thread):
#     def run(self):
#         for i in range(5):
#             print('---fun1中i的值为：', i)
#             time.sleep(1)
#
#
# class CodingThread2(threading.Thread):
#     def run(self):
#         for i in range(5):
#             print('-----fun2中i的值为：', i)
#             time.sleep(1)
#
#
# def mult():
#     t1 = CodingThread()
#     t2 = CodingThread2()
#     t1.start()
#     t2.start()
#
# if __name__ == '__main__':
#     mult()

class CodingThread(threading.Thread):
    def run(self):
        thread = threading.current_thread()
        print(thread)
        print('线程的名称：', thread.getName())
        for i in range(5):
            print('---fun1中i的值为：', i)
            time.sleep(1)



class CodingThread2(threading.Thread):
    def run(self):
        thread = threading.current_thread()
        print(thread)
        print('线程的名称：',thread.getName())
        #修改线程的名称
        for i in range(5):
            print('-----fun2中i的值为：', i)
            time.sleep(1)


def mult():
    t1 = CodingThread()
    t2 = CodingThread2()
    t1.start()
    t2.start()
    print(threading.enumerate())

if __name__ == '__main__':
    mult()

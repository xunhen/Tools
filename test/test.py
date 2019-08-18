import queue
import threading
import random
import time

class Producer(threading.Thread):
    """
    Producer thread 制作线程
    """
    def __init__(self, t_name, queue):  # 传入线程名、实例化队列
        threading.Thread.__init__(self, name=t_name)  # t_name即是threadName
        self.data = queue

    def run(self):
        for i in range(5):  # 生成0-4五条队列
            print("%s: %s is producing %d to the queue!" % (time.ctime(), self.getName(), i))  # 当前时间t生成编号d并加入队列
            self.data.put(i)  # 写入队列编号
            time.sleep(random.randrange(10) / 5)  # 随机休息一会
        print("%s: %s producing finished!" % (time.ctime(), self.getName))  # 编号d队列完成制作


class Consumer(threading.Thread):
    """
    Consumer thread 消费线程，感觉来源于COOKBOOK
    """
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data = queue

    def run(self):
        for i in range(5):
            val = self.data.get()
            print("%s: %s is consuming. %d in the queue is consumed!" % (time.ctime(), self.getName(), val))  # 编号d队列已经被消费
            time.sleep(random.randrange(10))
        print("%s: %s consuming finished!" % (time.ctime(), self.getName()))  # 编号d队列完成消费

if __name__ == '__main__':
    """
     Main thread 主线程
     """
    queue = queue.Queue()  # 队列实例化
    queue.empty()
    queue.get()
    producer = Producer('Pro.', queue)  # 调用对象，并传如参数线程名、实例化队列
    consumer1 = Consumer('Con1.', queue)  # 同上，在制造的同时进行消费
    consumer2 = Consumer('Con2.', queue)  # 同上，在制造的同时进行消费
    consumer3 = Consumer('Con3.', queue)  # 同上，在制造的同时进行消费
    producer.start()  # 开始制造
    consumer1.start()  # 开始消费
    consumer2.start()  # 开始消费
    consumer3.start()  # 开始消费
    """
    join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
　　join()方法的位置是在for循环外的，也就是说必须等待for循环里的两个进程都结束后，才去执行主进程。
    """
    producer.join()
    consumer1.join()
    consumer2.join()
    consumer3.join()
    print('All threads terminate!')
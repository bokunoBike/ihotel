import queue
import threading
import serial
from influxdb import InfluxDBClient


class Producer(threading.Thread):
    """docstring for Producer"""

    def __init__(self, q, name):
        super(Producer, self).__init__()
        self.q = q
        self.name = name
        print('Producer %s start' % self.name)

    def run(self):

        # 硬件端口号com3，波特率9600
        ser = serial.Serial('com3', 9600)

        # 读取数据99999个
        for j in range(0, 99999):
            resource = ser.readline()

            try:
                # 把读取的一个数据传入队列
                self.q.put(resource, block=True, timeout=3)

            except queue.Full:
                # 队满报错
                print('queue is full, %s will exit' % self.name)

            print('%s: resource %s in queue' % (self.name, resource))

        # 硬件端口关闭
        ser.close()


class Consumer(threading.Thread):
    """docstring for Consumer"""

    def __init__(self, q, name):
        super(Consumer, self).__init__()
        self.q = q
        self.name = name
        print('consumer %s start' % name)

    def run(self):
        # 写入数据99999个
        for j in range(0, 99999):
            try:
                # 获取队列中的数据
                res = self.q.get(block=True, timeout=3)

                # 数据保存到influxdb当中
                data_out(res)

                self.q.task_done()

            except queue.Empty:
                # 队空报错
                print('queue is empty, %s will exit' % self.name)
                break

            else:
                print('%s:resource %s out queue' % (self.name, str(res)))


def data_out(d):
    # 初始化
    client = InfluxDBClient()

    # 创建数据库test_db
    client.create_database('test_db')

    # 连接并使用数据库test_db
    client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')

    # 写入数据格式如下
    data = [
        {
            "measurement": "Z101",  # 表名
            "tags": {
                "sensor": "num"  # 标签（属性）
            },
            "fields": {
                "value": d  # 值
            }
        }
    ]

    # 写入数据
    client.write_points(data)


# 设置队列最长长度
testQueue = queue.Queue(4096)

# 一个生产者一个消费者
for i in range(0, 1):
    p = Producer(testQueue, 'p%i' % i)
    p.start()
for i in range(0, 1):
    c = Consumer(testQueue, 'c%i' % i)
    c.start()

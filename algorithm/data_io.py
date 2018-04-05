#!/usr/bin/python
# --coding:utf-8--
import queue
import threading
import serial
from influxdb import InfluxDBClient
import time
import re


class Producer(threading.Thread):
    """docstring for Producer"""

    def __init__(self, q, name):
        super(Producer, self).__init__()
        self.q = q
        self.name = name
        print('Producer %s start' % self.name)

    def run(self):

        # 硬件端口号com3，波特率9600
        while 1:
            try:
                ser = serial.Serial('/dev/ttyACM0', 9600)
                break
            except Exception as e:
                print(e, "\n没有检测到串口，将于5s后自动重试")
                time.sleep(5)
                continue

        # 将数据写入内存
        while 1:
            resource = ser.readline()

            try:
                # 把读取的一个数据传入队列
                self.q.put(resource, block=True, timeout=3)

            except queue.Full:
                # 队满报错
                print('queue is full, %s will exit' % self.name)

            print('%s: resource %s in queue' % (self.name, resource))

        # 硬件端口关闭
        # ser.close()


class Consumer(threading.Thread):
    """docstring for Consumer"""

    def __init__(self, q, name):
        super(Consumer, self).__init__()
        self.q = q
        self.name = name
        print('consumer %s start' % name)

    def run(self):

        n = 0
        # 初始化数据库
        while 1:
            try:
                # 初始化
                client = InfluxDBClient()
                # 删除冗余数据
                client.drop_database('ihotel')
                # 创建数据库ihotel
                client.create_database('ihotel')
                # 连接并使用数据库ihotel
                client = InfluxDBClient('localhost', 8086, 'root', '', 'ihotel')
                break
            except Exception as e:
                print("Error:", e, "\n请检查influxdb或者mysql数据库，操作将于5s后自动重试")
                time.sleep(5)
                continue

        # 从内存取数据
        while 1:
            n += 1
            try:
                # 获取队列中的数据
                res = self.q.get(block=True, timeout=3)

                # 数据保存到influxdb当中
                data_out(res, n, client)

                self.q.task_done()

            except queue.Empty:
                # 队空报错
                print('queue is empty, %s will exit' % self.name)
                break

            else:
                print('%i   %s:resource %s out queue' % (n, self.name, str(res)))


# 数据存入influxdb
def data_out(res, n, client):
    pattern = re.compile(r".*(\d):(\d*)")
    try:
        res_t = re.match(pattern, str(res))
        if res_t is None:
            return
    except TypeError:
        return
    # print(res_t.group(1), res_t.group(2))

    # 防止res_t.group(2)即传感器信号为空
    res_t2 = res_t.group(2)
    if len(res_t.group(2)) == 0:
        res_t2 = 0

    # 写入数据格式如下
    data = [
        {
            "measurement": "Z101",  # 表名
            "tags": {
                "sensor": "num%s" % res_t.group(1),  # 标签（属性）
            },
            "fields": {
                "n": n,  # 索引
                "value": int(res_t2),  # 值
            }
        }
    ]

    # 写入数据
    client.write_points(data)


# 设置队列最长长度
testQueue = queue.Queue(1024)

# 一个生产者一个消费者
for i in range(0, 1):
    p = Producer(testQueue, 'p%i' % i)
    p.start()
for i in range(0, 1):
    c = Consumer(testQueue, 'c%i' % i)
    c.start()

#!/usr/bin/python
# --coding:utf-8--
from influxdb import InfluxDBClient
import time
import random

num = 0
sensor = 0
m = 40
room_id = 'Z101'
sensor_count = 2

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

# 模拟1500组数据写入influxdb
for n in range(1, 8500):
    time.sleep(0.001)

    # 模拟传感器号码
    num = num % sensor_count + 1

    # 模拟超声波信号
    if num == 1 or num == 2:
        sensor = 190 + random.randint(-5, 5)
        if m < n <= m + 70:
            sensor -= 100
        # 每13组模拟一次超声无效信号
        if n % 13 == 0:
            sensor = sensor + 90 + random.randint(-10, 10)
    # 模拟红外信号
    else:
        sensor = 0
        if m < n <= m + 30:
            sensor = 1

    # 每121组数据，超声波检测到40次变化，红外60次变化
    if n % 205 == 0:
        m += 205
        print('数据导入量: %s' % n)

    t = round(time.time() * 1000000000)
    # 写入数据格式如下
    data = [
        {
            "measurement": room_id,  # 表名
            "tags": {
                "sensor": "num%s" % num,  # 标签（属性）

            },
            "fields": {
                "n": n,
                "value": sensor  # 值
            }
        }
    ]
    # 写入数据
    client.write_points(data)

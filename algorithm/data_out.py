#!/usr/bin/python
# --coding:utf-8--
from influxdb import InfluxDBClient
import time
import random

num = 2
sensor = 0
m = 20
room_id = 'Z101'

# 初始化数据库
while 1:
    try:
        # 初始化
        client = InfluxDBClient()
        # 删除冗余数据
        client.drop_database('test_db')
        # 创建数据库test_db
        client.create_database('test_db')
        # 连接并使用数据库test_db
        client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')
        break
    except Exception as e:
        print("Error:", e, "\n请检查influxdb或者mysql数据库，操作将于5s后自动重试")
        time.sleep(5)
        continue
            
# 模拟3000组数据写入influxdb
for n in range(1, 3000):
    time.sleep(0.001)
    # 模拟两个传感器
    if num == 1:
        num = 2
    else:
        num = 1

    # 模拟超声波信号波动
    sensor = 190 + random.randint(-5, 5)

    # 模拟超声波信号变化
    if m < n <= m + 40:
        sensor -= 100

    # 每13组模拟一次无效信号
    if n % 13 == 0:
        sensor = sensor + 90 + random.randint(-10, 10)

    # 每121组数据，超声波检测到40次变化
    if n % 121 == 0:
        m += 121
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

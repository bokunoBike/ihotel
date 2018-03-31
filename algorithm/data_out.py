#!/usr/bin/python
# --coding:utf-8--
from influxdb import InfluxDBClient
import time
import random

# 初始化
client = InfluxDBClient()
# 删除冗余数据
client.drop_database('test_db')
# 创建数据库test_db
client.create_database('test_db')
# 创建数据保留策略为1h
client.query('CREATE RETENTION POLICY "1_hours" ON "test_db" DURATION 1h REPLICATION 1 DEFAULT')
# 连接并使用数据库test_db
client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')

i = 2
k = 0
li = 20
room_id = 'Z101'
# 模拟1000组数据写入influxdb
for j in range(1, 500):
    time.sleep(0.001)
    # 模拟两个传感器
    if i == 1:
        i = 2
    else:
        i = 1

    # 模拟超声波信号波动
    k = 190 + random.randint(-5, 5)
    # 模拟超声波信号变化
    if li < j < li + 40:
        k -= 100
    # # 每40组模拟一次无效信号
    # if j % 20 == 0:
    #     k = k + 90 + random.randint(-10, 10)
    # 每121组数据，超声波检测到40次变化
    if j % 121 == 0:
        li += 121
        print('数据导入量: %s' % j)

    t = round(time.time() * 1000000000)
    # 写入数据格式如下
    data = [
        {
            "measurement": room_id,  # 表名
            "tags": {
                "sensor": "num%s" % i,  # 标签（属性）

            },
            "fields": {
                "n": j,
                "value": k  # 值
            }
        }
    ]
    # 写入数据
    client.write_points(data)

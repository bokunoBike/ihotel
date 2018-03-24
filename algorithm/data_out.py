from influxdb import InfluxDBClient
import time
import random

# 初始化
client = InfluxDBClient()

# 显示所有数据库名称
print(client.get_list_database())

# 创建数据库test_db
client.create_database('test_db')

# 连接并使用数据库test_db
client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')

i = 2
k = 0
li = 20
room_num = 'Z101'
# 模拟1000组数据写入influxdb
for j in range(1, 1000):
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
    # 每121组数据，超声波检测到40次变化
    if j % 121 == 0:
        li += 121
        print('数据导入量: %s' % j)

    t = round(time.time() * 1000000000)
    # 写入数据格式如下
    data = [
        {
            "measurement": room_num,  # 表名
            "tags": {
                "sensor": "num%s" % i,  # 标签（属性）
                "n": j,

            },
            "time": t,
            "fields": {
                "value": k  # 值
            }
        }
    ]
    # 写入数据
    client.write_points(data)

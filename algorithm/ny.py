# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient
import datetime

room_id = "Z101"
print(room_id)
client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')
current_time = datetime.datetime.now()
over_time = current_time - datetime.timedelta(seconds=5)
# result = client.query("select * from %s WHERE time >= %s AND time <= %s  group by TIME(1s);" % (room_id, current_time, over_time))
print("select * from %s WHERE time <= %d AND time >= %d;" % (
    room_id, current_time.timestamp() * 1000000000, over_time.timestamp() * 1000000000))
result = client.query(
                "select mean(value) from %s WHERE sensor='num2' AND time <= %d AND time >= %d GROUP BY TIME(100ms);" % (
                    room_id, current_time.timestamp() * 1000000000, over_time.timestamp() * 1000000000))
# result = client.query("select * from %s;" % (room_id))

for raw in result[room_id]:
    print(raw['time'])
    # print(raw)

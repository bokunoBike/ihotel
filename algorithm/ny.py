# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient

room_id = "Z101"
print(room_id)
client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')
result = client.query("select * from %s where %s.time - now.time < 28801000000;" % (room_id, room_id))
# result = client.query("select * from %s;" % (room_id))
for raw in result[room_id]:
    print((raw['time'], raw['sensor'], raw['value']))
    # print(raw)

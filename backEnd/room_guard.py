# -*- coding: utf-8 -*-

import pymysql
import time
import datetime

# 连接mysql
db = pymysql.connect("localhost", "root", "", "ihotel")
cursor = db.cursor()

while True:
    current_time = datetime.datetime.now()
    sql = "UPDATE Room SET pattern='0' WHERE expired_time < '%s %s:%s:%s';" % (
        current_time.date(), current_time.hour, current_time.minute, current_time.second)
    i = cursor.execute(sql)
    db.commit()
    sql = "UPDATE Room SET user_id=NULL WHERE room_id in (SELECT room_id FROM Record WHERE expired_time < '%s %s:%s:%s')" % (
        current_time.date(), current_time.hour, current_time.minute, current_time.second)
    i = cursor.execute(sql)
    db.commit()
    time.sleep(10)
cursor.close()
db.close()

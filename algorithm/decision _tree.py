import time
from influxdb import InfluxDBClient
import pymysql


def _my_tree(room_num=None):
    people_num = 0  # 人数
    sensor1 = 0  # 超声波1号
    sensor2 = 0  # 超声波2号
    sensor3 = 0  # 红外线1号
    sensor4 = 0  # 红外线2号
    sensor1_temp = 0  # 暂存sensor1改变后的信号
    sensor2_temp = 0  # 暂存sensor2改变后的信号
    sensor1_stat = 0  # 判断sensor1信号是否改变
    sensor2_stat = 0  # 判断sensor2信号是否改变
    max_distance = 200  # 传感器有效测量距离

    # 初始化
    client = InfluxDBClient()
    # 显示所有数据库名称
    print(client.get_list_database())
    # 创建数据库test_db
    client.create_database('test_db')
    # 连接influxdb
    client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')
    # 连接mysql
    db = pymysql.connect("localhost", "root", "", "ihotel")
    cursor = db.cursor()

    n = 1
    while 1:
        # 实时时间
        t = time.time()

        # 实时读取influxdb中的sensor1数据
        result = client.query("select*from " + room_num + " where n = '" + str(n) + "' ;")
        if len(result) == 0:
            continue
        # print(ki, result.raw['series'][0]['values'][0])
        n += 1
        # 分割数据
        sensor = result.raw['series'][0]['values'][0][2]  # 传感器号码
        distance = result.raw['series'][0]['values'][0][3]  # 距离

        # 传感器信号判断
        if max_distance - distance > 40:
            stat = 1
        else:
            stat = 0

        # 传感器判断
        if sensor == 'num1':
            sensor1 = stat
        elif sensor == 'num2':
            sensor2 = stat

        # sensor1_temp暂存sensor1改变后的信号，sensor1信号改变时sensor1_stat记为1
        if sensor1_temp != sensor1:
            sensor1_temp = sensor1
            sensor1_stat = 1

        # sensor2_temp暂存sensor2改变后的信号，sensor2信号改变时sensor2_stat记为1
        if sensor2_temp != sensor2:
            sensor2_temp = sensor2
            sensor2_stat = 1

        people_stat = 0

        # 如果sensor1发生改变，且改变后的信号为1，sensor2实时信号为0，人数加1
        if sensor1_stat == 1 and sensor1_temp == 1 and sensor2 == 0:
            people_num += 1
            people_stat = 1
            sensor1_stat = 0

        # 如果房间人数不为0，sensor2发生改变，且改变后的信号为1，sensor1实时信号为0，人数减1
        elif people_num != 0 and sensor2_stat == 1 and sensor2_temp == 1 and sensor1 == 0:
            people_num -= 1
            people_stat = 1
            sensor2_stat = 0

        # 如果房间人数判断为0，红外线有信号，人数加1
        if people_num == 0:
            if sensor3 == 1 or sensor4 == 1:
                people_num += 1
                people_stat = 1

        # 人数发生变化时，将time和people_num写入数据库
        if people_stat == 1:
            print('time:%s people num:%i' % (t, people_num))
            # sql = "INSERT INTO peo_stat(time_stamp, peo_num) VALUE ('%s','%i')" % (t, people_num)
            sql = "UPDATE room set people_counts='%i' WHERE room_id='%s'" % (people_num, room_num)
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()


if __name__ == "__main__":
    _my_tree('Z101')

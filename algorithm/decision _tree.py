#!/usr/bin/python
# --coding:utf-8--
import time
from influxdb import InfluxDBClient
import pymysql


def _my_tree(room_id='Z101', max_distance=190, fluctuate=20):
    """
    :param room_id: 房间号
    :param max_distance: 超声波传感器有效测量距离
    :param fluctuate: 传感器数据可能的波动范围
    :return: None
    """

    people_num = 0  # 人数
    sensor1_level = 0  # 超声波1号电平
    sensor2_level = 0  # 超声波2号电平
    sensor3_level = 0  # 红外线1号电平
    sensor4_level = 0  # 红外线2号电平

    # 对两个数据库进行初始化操作
    while 1:
        try:
            # 初始化influxdb
            client = InfluxDBClient()
            # 显示所有数据库名称
            print(client.get_list_database())
            # 创建数据库test_db
            client.create_database('test_db')
            # 连接influxdb
            client = InfluxDBClient('localhost', 8086, 'root', '', 'test_db')

            # 连接mysql
            db = pymysql.connect("localhost", "root", "123456", "ihotel")
            cursor = db.cursor()
            break
        except Exception as e:
            print("Error:", e, "\n请检查influxdb或者mysql数据库，操作将于5s后自动重试")
            time.sleep(5)
            continue

    # 舍弃前几组不稳定数据(12的倍数)
    n = 24

    # 缓存前6组数据
    while 1:
        try:
            result1 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n))
            result2 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 1))
            result3 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 2))
            result4 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 3))
            result5 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 4))
            result6 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 5))
            temp = [result1.raw['series'][0]['values'][0], result2.raw['series'][0]['values'][0],
                    result3.raw['series'][0]['values'][0], result4.raw['series'][0]['values'][0],
                    result5.raw['series'][0]['values'][0], result6.raw['series'][0]['values'][0]]
            break
        except Exception as e:
            print("Error:", e, "\n请确保传感器信息已经存入influxdb中，操作将于5s后自动重试")
            time.sleep(5)
            continue

    # 将n指向第下一个还未缓存的数据
    n += 6

    # 超声波最近3个状态（从左到右状态由旧到新）
    sensor_stat = ['00', '00', '00']

    # 算法判断开始
    while 1:
        # 实时时间
        t = time.time()

        # 读取下一组数据
        result = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n))
        if len(result) == 0:
            continue

        # 清除旧数据，缓存新数据
        temp.pop(0)
        temp.append(result.raw['series'][0]['values'][0])

        # 提取数据
        sensor_num = temp[2][2]  # 传感器号码
        distance_or_signal1 = temp[0][3]  # 第1个超声距离或者红外信号
        distance_or_signal2 = temp[2][3]  # 第2个超声距离或者红外信号
        distance_or_signal3 = temp[4][3]  # 第3个超声距离或者红外信号

        # 过滤无效信号
        # 一个传感器的连续的3个信号，如果第1个和第3个信号相差不大
        if distance_or_signal1 - fluctuate < distance_or_signal3 < distance_or_signal1 + fluctuate:
            sig_ave = (distance_or_signal1 + distance_or_signal3) / 2
            # 而中间信号波动很大时，中间信号取1、3信号平均值
            if distance_or_signal2 > sig_ave + fluctuate or distance_or_signal2 < sig_ave - fluctuate:
                distance_or_signal2 = sig_ave
                temp[2][3] = sig_ave

        # 超声传感器信号判断
        if max_distance - int(distance_or_signal2) > 40:
            stat = 1
        else:
            stat = 0
        if sensor_num == 'num1':
            sensor1_level = stat
        elif sensor_num == 'num2':
            sensor2_level = stat

        # 红外传感器信号判断
        elif sensor_num == 'num3':
            sensor3_level = distance_or_signal2
        elif sensor_num == 'num4':
            sensor4_level = distance_or_signal2

        # 超声波状态判断
        # 00：增加最新状态，删除旧状态
        if sensor1_level == 0 and sensor2_level == 0:
            sensor_stat.pop(0)  # 删
            sensor_stat.append('00')  # 增
        # 10：如果第2个状态和第3个状态都是10，说明1号先于2号触发一段时间，此时则不改变状态（锁存有用状态）
        #     否则将增加最新状态，删除旧状态
        elif sensor_stat != ['00', '10', '10'] and sensor1_level == 1 and sensor2_level == 0:
            sensor_stat.pop(0)  # 增
            sensor_stat.append('10')  # 删
        # 01：类似10
        elif sensor_stat != ['00', '01', '01'] and sensor1_level == 0 and sensor2_level == 1:
            sensor_stat.pop(0)  # 增
            sensor_stat.append('01')  # 删
        # 11
        elif sensor1_level == 1 and sensor2_level == 1:
            # 当出现锁存有用状态时，更新最新状态
            if sensor_stat == ['00', '10', '10'] or sensor_stat == ['00', '01', '01']:
                sensor_stat[2] = '11'  # 更新
            # 否则增加最新状态，删除旧状态
            else:
                sensor_stat.pop(0)
                sensor_stat.append('11')

        # 人数变化状态
        people_stat = 0

        # 00->10->11，加1人
        if sensor_stat == ['00', '10', '11']:
            people_num += 1
            people_stat = 1
        # people_num!=0，00->01->11，减1人
        if people_num != 0 and sensor_stat == ['00', '01', '11']:
            people_num -= 1
            people_stat = 1

        # 如果房间人数判断为0，红外线有信号，人数加1
        if people_num == 0:
            if sensor3_level == 1 or sensor4_level == 1:
                people_num += 1
                people_stat = 1

        # 人数发生变化时
        if people_stat == 1:
            print(n, t, people_num, distance_or_signal2)

            n += 24  # 人数变化后舍弃后24组数据降低CPU使用率
            # 舍弃数据后需要重新缓存6组数据
            while 1:
                try:
                    result1 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n))
                    result2 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 1))
                    result3 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 2))
                    result4 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 3))
                    result5 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 4))
                    result6 = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + 5))
                    temp = [result1.raw['series'][0]['values'][0], result2.raw['series'][0]['values'][0],
                            result3.raw['series'][0]['values'][0], result4.raw['series'][0]['values'][0],
                            result5.raw['series'][0]['values'][0], result6.raw['series'][0]['values'][0]]
                    break
                except Exception as e:
                    print("Error:", e, "\n请确保传感器信息已经存入influxdb中，操作将于5s后自动重试")
                    time.sleep(5)
                    continue

            # 人数变化后存储到数据库
            sql = "UPDATE room SET people_counts='%i' WHERE room_id='%s'" % (people_num, room_id)
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()

        # 下一组数据
        n += 1


if __name__ == "__main__":
    _my_tree('Z101')

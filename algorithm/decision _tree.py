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
    surpass_query = 0
    jump_interval = 50  # 跳50组数据
    sensor_count = 2  # 传感器数量

    '''对两个数据库进行初始化操作'''
    while 1:
        try:
            # 连接influxdb
            client = InfluxDBClient('localhost', 8086, 'root', '', 'ihotel')

            # 连接mysql
            db = pymysql.connect("localhost", "root", "123456", "ihotel")
            cursor = db.cursor()
            break
        except Exception as e:
            print("Error:", e, "\n请检查influxdb或者mysql数据库，操作将于5s后自动重试")
            time.sleep(5)
            continue

    # 舍弃前几组不稳定数据(sensor_count * 3的倍数)
    n = 24

    ''' 缓存前sensor_count * 3组数据'''
    i = 1
    temp = []
    while i <= sensor_count * 3:
        try:
            result = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + i))
            temp.append(result.raw['series'][0]['values'][0])
            i += 1
        except Exception as e:
            print("Error:", e, "\n请确保传感器信息已经存入influxdb中，操作将于1s后自动重试")
            time.sleep(1)
            continue
    # 将n指向第下一个还未缓存的数据
    n += sensor_count * 3

    # 超声波最近3个状态（从左到右状态由旧到新）
    sensor_stat = ['00', '00', '00']

    ''' 算法判断开始'''
    while 1:
        # 实时时间
        t = time.time()
        try:
            # 读取下一组数据
            result = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n))
            if len(result) == 0:
                time.sleep(0.5)
                continue
        except Exception as e:
            print("Error:", e, "\n数据库出错，程序将于1s后重新启动")
            time.sleep(1)
            _my_tree(room_id, max_distance, fluctuate)
            return

        # 清除旧数据，缓存新数据
        temp.pop(0)
        temp.append(result.raw['series'][0]['values'][0])

        # 提取数据
        sensor_num = temp[sensor_count][2]  # 传感器号码
        distance_or_signal1 = temp[0 * sensor_count][3]  # 第1个超声距离或者红外信号
        distance_or_signal2 = temp[1 * sensor_count][3]  # 第2个超声距离或者红外信号
        distance_or_signal3 = temp[2 * sensor_count][3]  # 第3个超声距离或者红外信号

        ''' 过滤无效信号'''
        # 一个传感器的连续的3个信号，如果第1个和第3个信号相差不大
        if distance_or_signal1 - fluctuate < distance_or_signal3 < distance_or_signal1 + fluctuate:
            sig_ave = (distance_or_signal1 + distance_or_signal3) / 2
            # 而中间信号波动很大时，中间信号取1、3信号平均值
            if distance_or_signal2 > sig_ave + fluctuate or distance_or_signal2 < sig_ave - fluctuate:
                distance_or_signal2 = sig_ave
                temp[1 * sensor_count][3] = sig_ave

        '''传感器信号判断'''
        # 超声传感器信号判断
        if max_distance - int(distance_or_signal2) > 40:
            stat = 1
        else:
            stat = 0
        if sensor_num == 'num1':
            sensor1_level = stat
        elif sensor_num == 'num2':
            sensor2_level = stat

        ''' 超声波状态判断'''
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

        '''人数判断'''
        # 00->10->11，加1人
        if sensor_stat == ['00', '10', '11']:
            people_num += 1
            people_stat = 1
            people_change = 1
        # people_num!=0，00->01->11，减1人
        if people_num != 0 and sensor_stat == ['00', '01', '11']:
            people_num -= 1
            people_stat = 1
            people_change = -1

        ''' 人数发生变化时'''
        if people_stat == 1:
            print(n - 2 * sensor_count, t, people_num, distance_or_signal2, sensor_stat)

            n += 24  # 人数变化后舍弃后24组数据降低CPU使用率
            time.sleep(0.2)  # CPU休眠一段时间防止之后的数据还没传进来
            # 舍弃数据后需要重新缓存sensor_count * 3组数据
            i = 1
            j = 1
            temp = []
            while i <= sensor_count * 3:
                try:
                    result = client.query("SELECT*FROM %s WHERE n = %i;" % (room_id, n + i))
                    temp.append(result.raw['series'][0]['values'][0])
                    i += 1
                except Exception as e:
                    print("Error:", e, "\n数据库出错，操作将于0.5s后自动重试")
                    if j > 6:
                        print("请手动重启程序")
                        return
                    time.sleep(0.5)
                    j += 1
                    continue
            n += sensor_count * 3
            # 人数变化后存储到数据库
            # sql = "UPDATE Room SET people_counts='%i' WHERE room_id='%s'" % (people_num, room_id)
            if people_change == 1:
                sql = "UPDATE Room SET people_counts=people_counts+1 WHERE room_id='%s'" % (room_id,)
            elif people_change == -1:
                sql = "UPDATE Room SET people_counts=people_counts-1 WHERE room_id='%s' AND people_counts!=0" % (
                    room_id,)
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()

            # 下一组数据
            if n > surpass_query:
                # query_sql = "SELECT first(n) FROM %s WHERE n>%i AND (value < %i OR value > %i);" % (
                #     room_id, n, max_distance - fluctuate, max_distance + fluctuate)
                query_sql = "SELECT first(n) FROM %s WHERE n>%i AND value < %i;" % (
                    room_id, n, max_distance - fluctuate)
                result = client.query(query_sql)
                # print("SELECT first(n) FROM %s WHERE n>%i AND (value < %i OR value > %i);" % (
                #     room_id, n, max_distance - fluctuate, max_distance + fluctuate))
                # print(result.raw['series'][0]['values'][0][1])
                # print(result.raw)
                while len(result) == 0:
                    print('sleep')
                    time.sleep(0.5)
                    result = client.query(query_sql)
                next_n = result.raw['series'][0]['values'][0][1]
                if next_n - n <= jump_interval:
                    surpass_query += jump_interval
                    n += 1
                    # print('find no jump')
                else:
                    n = next_n - 10
                    surpass_query = n
                    print('jump')
            else:
                n += 1


if __name__ == "__main__":
    _my_tree('Z101')

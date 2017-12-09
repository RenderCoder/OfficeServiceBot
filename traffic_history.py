#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import re

# 绘图方法
def add_data_to_image(mac, data_array):
    file_name = re.sub(r'\:', '_', mac)
    
    # plt.figure(figsize=(20,10))
    # plt.plot([1,2,3,4,5,6])
    plt.plot(np.array(data_array), label=mac)
    # plt.legend()
    plt.legend(bbox_to_anchor=(1.04,1), borderaxespad=0)
    plt.subplots_adjust(right=0.8)
    plt.ylabel('network KB/s')  #为y轴加注释
    plt.xlabel('time point')
    plt.title('Network Traffic')
    # plt.show()
    

def save_image():
    fig = plt.gcf()
    fig.set_size_inches(12, 5)
    plt.draw()
    fig.savefig('./images/all.png')#, dpi=100)

conn = sqlite3.connect('test.db')
print('Opened database successfully')
c = conn.cursor()

# 获取最后一次数据时间
cursor = c.execute("SELECT UP, DOWN, MAC, Timestamp  FROM TRAFFIC_HISTORY ORDER BY ID DESC LIMIT 1")
for row in cursor:
   print("UP = ", row[0])
   print("DOWN = ", row[1])
   print("MAC = ", row[2])
   time = row[3]
   print('------')
print(time)
'''
# 获取最近一次统计的 mac 地址数量
cursor = c.execute("SELECT MAC FROM TRAFFIC_HISTORY WHERE DATETIME(TRAFFIC_HISTORY.Timestamp) = '{time}'".format(time=time))
for row in cursor:
    device_count = row[0]
    print('Lastest traffic data device count = ', device_count)
'''
# 查询最近一次统计的 mac 地址列表, 取最近 15 分钟（LIMIT = 15*4）
recent_devices_traffic_data = {}
cursor = c.execute("SELECT MAC FROM TRAFFIC_HISTORY WHERE DATETIME(TRAFFIC_HISTORY.Timestamp) = '{time}'".format(time=time))
for row in cursor:
    current_mac = row[0]
    print('current mac = ', current_mac)
    recent_devices_traffic_data[current_mac] = {'UP':[], 'DOWN':[]}
    
for key in recent_devices_traffic_data.keys():
    cursor = c.execute("SELECT UP, DOWN FROM TRAFFIC_HISTORY WHERE MAC = '{mac}' ORDER BY ID DESC LIMIT 60".format(mac=key))
    for row in cursor:
        up = row[0]
        down = row[1]
        recent_devices_traffic_data[key]['UP'].append(up)
        recent_devices_traffic_data[key]['DOWN'].append(down)
    add_data_to_image(key, recent_devices_traffic_data[key]['DOWN'])

print(recent_devices_traffic_data)

# 绘制并保存图形
print('draw image...')
save_image()
print('save image done.')

print("Done.")
conn.close()
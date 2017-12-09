#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import json
import sqlite3

test_data = b'\xef\xbb\xbfvar array_traffic = new Array();\nvar router_traffic = new Array();\narray_traffic = [["AC:89:95:77:9A:E9", "996055825", "2194849299"], ["61:FE:C5:9F:80:4D", "24944756", "69859739"], ["34:CB:00:EA:01:A5", "6497908", "5743238"], ["6C:40:88:92:E6:56", "26223811", "476987978"], ["DC:CC:5C:D3:AE:1A", "41962324", "31270255"], ["8E:E6:51:DC:65:2A", "1976260", "18426081"], ["A0:5E:60:12:50:8E", "13448374", "102802756"], ["38:BB:7A:9F:8C:81", "63140", "74613"], ["28:6C:87:B1:6B:3F", "389682", "340876"], ["A4:5E:60:FA:02:90", "1412998", "27494712"]];\nrouter_traffic = ["1112975078", "2927849547"];\n\n'
test_data = bytes.decode(test_data, 'utf-8')
result = re.sub(r'var array_traffic = new Array\(\)\;\nvar router_traffic = new Array\(\)\;\narray_traffic = ', '', test_data)
result = re.sub(r'\n|\;|\ufeff', '', result)
result = result.split('router_traffic = ')
if len(result) < 2:
    print('路由实时带宽使用数据解析错误.')
    exit(0)

sub_device_traffic_data = json.loads(result[0])
sub_device_traffic_data = map(
    lambda x: {
        'mac': x[0],
        'up': round(int(x[1])/1024/1024),
        'down': round(int(x[2])/1024/1024)
    },
    sub_device_traffic_data
)
sub_device_traffic_data = list(sub_device_traffic_data)
all_traffic_data = json.loads(result[1])

print(sub_device_traffic_data)

def procress_data_string(data_bytes):
    test_data = data_bytes
    test_data = bytes.decode(test_data, 'utf-8')
    result = re.sub(r'var array_traffic = new Array\(\)\;\nvar router_traffic = new Array\(\)\;\narray_traffic = ', '', test_data)
    result = re.sub(r'\n|\;|\ufeff', '', result)
    result = result.split('router_traffic = ')
    if len(result) < 2:
        print('路由实时带宽使用数据解析错误.')
        exit(0)

    sub_device_traffic_data = json.loads(result[0])
    sub_device_traffic_data = map(
        lambda x: {
            'mac': x[0],
            'up': round(int(x[1])/1024/1024),
            'down': round(int(x[2])/1024/1024)
        },
        sub_device_traffic_data
    )
    sub_device_traffic_data = list(sub_device_traffic_data)
    all_traffic_data = json.loads(result[1])
    return sub_device_traffic_data

def insert_data(sub_device_traffic_data):
    conn = sqlite3.connect('test.db')
    print('Opened database successfully')

    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists TRAFFIC_HISTORY
        (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
        UP              INT     NOT NULL,
        DOWN            INT     NOT NULL,
        MAC        CHAR(11),
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );''')
    print('Table created successfully')
    c.execute('''
        CREATE INDEX if not exists MAC_ADDRESS
        ON TRAFFIC_HISTORY (MAC);
    ''')

    # insert

    for traffic_item in sub_device_traffic_data:
        print(traffic_item)
        c.execute("INSERT INTO TRAFFIC_HISTORY (UP,DOWN,MAC) \
        VALUES ({up}, {down}, '{mac}')".format(up=traffic_item['up'], down=traffic_item['down'], mac=traffic_item['mac']))

    print('commit')
    conn.commit()

    conn.close()
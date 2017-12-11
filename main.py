#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import os
from flask import Flask, render_template
import sqlite3
import re
from monitor_traffic import setup_token, start_monitor
import atexit
import threading

'''
token = os.environ.get('dingtalk_token', 'a')
url = 'https://oapi.dingtalk.com/robot/send?access_token={token}'.format(token=token)
print(url)

headers = {'content-type': 'application/json'}
data = {"msgtype": "text", 
    "text": {                                        
        "content": "^H^H^H^H我就是我, 是不一样的烟火"
     }
  }
r = requests.post(url, headers=headers, data=json.dumps(data))
print(r.text)
'''

def get_mac_list():
    conn = sqlite3.connect('test.db')
    print('Opened database successfully')
    c = conn.cursor()
    cursor = c.execute("SELECT UP, DOWN, MAC, Timestamp  FROM TRAFFIC_HISTORY ORDER BY ID DESC LIMIT 1")
    for row in cursor:
        print("UP = ", row[0])
        print("DOWN = ", row[1])
        print("MAC = ", row[2])
        time = row[3]
        print('------')
    print(time)

    mac_list = []
    cursor = c.execute("SELECT MAC FROM TRAFFIC_HISTORY WHERE DATETIME(TRAFFIC_HISTORY.Timestamp) = '{time}'".format(time=time))
    for row in cursor:
        current_mac = row[0]
        print('current mac = ', current_mac)
        mac_list.append(current_mac)

    conn.close()

    return mac_list

app = Flask(__name__)

@app.route('/')
def home():
    mac_list = get_mac_list()
    device_traffic_image_name = [*map(lambda x: re.sub(r'\:', '_', x), mac_list)]
    return render_template('home.html', mac_list=mac_list, device_traffic_image_name=device_traffic_image_name)

# 创建更新网络使用数据线程
class MonitorTrafficThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    
    def run(self):
        setup_token()
        start_monitor()

monitor_traffic_thread = MonitorTrafficThread(1, 'monitor_traffic_thread')
monitor_traffic_thread.start()

# 程序退出前动作
def exit_handler():
    print('Application will exit.')

atexit.register(exit_handler)

if __name__ == '__main__':
    app.run(debug=True)
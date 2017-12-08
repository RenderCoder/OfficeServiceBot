#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import os

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
'''
Descripttion: 
version: 
Author: Catop
Date: 2021-04-11 23:38:52
LastEditTime: 2021-04-11 23:45:19
'''
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import requests
import json
import time

import globalAPI.goapi as goapi

def zaoan():
    url = 'http://api.tianapi.com/txapi/lzmy/index'
    params = {'key':'ce9683fb3b39fb211a0834c09165c599'}

    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    if(res_dict['code'] == 200):
        content = res_dict['newslist'][0]
        text = '早安一言☀️\n'+content['saying']+'\n'+content['transl']+' ——'+content['source']

        #goapi.sendMsg('601179193',text)
        goapi.sendGroupMsg('949773437',text)
        goapi.sendGroupMsg('515192555',text)

if __name__ == '__main__':
    zaoan()
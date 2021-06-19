'''
Description: /amuseActice/舔狗
Author: Catop
Date: 2021-06-19 13:56:49
LastEditTime: 2021-06-19 14:35:03
'''
from globalAPI import goapi
import requests
import json


def handler(message, qid, type, message_id):
    """获取舔狗"""
    url = 'http://api.tianapi.com/txapi/tiangou/index'
    params = {'key':'ce9683fb3b39fb211a0834c09165c599'}
    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    text = ""
    if(res_dict['code'] == 200):
        text = res_dict['newslist'][0]['content']
    
    #return text
    if(type == 'private'):
        goapi.sendMsg(qid, text)
    else:
        goapi.sendGroupMsg(qid, text)
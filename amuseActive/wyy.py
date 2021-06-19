'''
Description: 网易云
Author: Catop
Date: 2021-06-19 14:35:46
LastEditTime: 2021-06-19 14:37:22
'''

from globalAPI import goapi
import requests
import json


def handler(message, qid, type, message_id):
    """获取网易云热评"""
    url = 'https://v1.hitokoto.cn'
    params = {'c':'j'}
    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    text = ""

    if(res_dict['from']):
        text = res_dict['hitokoto']+'——'+res_dict['from']
    else:
        text = res_dict['hitokoto']

    if(type == 'private'):
        goapi.sendMsg(qid, text)
    else:
        goapi.sendGroupMsg(qid, text)
    
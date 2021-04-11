'''
Descripttion: 
version: 
Author: Catop
Date: 2021-04-11 23:08:09
LastEditTime: 2021-04-11 23:45:03
'''

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import requests
import json
import time

import globalAPI.goapi as goapi


def wanan():
    text = f'今天辛苦了❤️\n{history_today()}\n{get_wyy()}\n\n时间不早了，赶快休息吧~'
    cq_code = f'[CQ:image,file={english_img()}]'
    #goapi.sendMsg('601179193',cq_code)
    #goapi.sendMsg('601179193',text)
    goapi.sendGroupMsg('949773437',cq_code)
    goapi.sendGroupMsg('949773437',text)

    goapi.sendGroupMsg('515192555',cq_code)
    goapi.sendGroupMsg('515192555',text)
    


def history_today():
    url = 'http://api.tianapi.com/txapi/lishi/index'
    params = {'key':'ce9683fb3b39fb211a0834c09165c599'}
    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    if(res_dict['code'] == 200):
        content = res_dict['newslist'][0]
        return content['lsdate']+' '+content['title']

def english_img():
    url = 'http://api.tianapi.com/txapi/everyday/index'
    params = {'key':'ce9683fb3b39fb211a0834c09165c599'}
    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    if(res_dict['code'] == 200):
        return res_dict['newslist'][0]['imgurl']

def get_wyy():
    url = 'https://v1.hitokoto.cn'
    params = {'c':'j'}
    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    if(res_dict['from']):
        return res_dict['hitokoto']+'——'+res_dict['from']
    else:
        return res_dict['hitokoto']


    

if __name__  == '__main__':
    #print(zaoan())
    #print(history_today())
    #print(english_img())
    #print(get_wyy())
    #print(wanan())
    wanan()
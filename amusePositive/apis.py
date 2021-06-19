'''
Descripttion: 一言API，全部返回纯文本，调用时请自行处理错误
version: 
Author: Catop
Date: 2021-04-11 23:38:52
LastEditTime: 2021-06-19 14:36:15
'''

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import requests
import json
import time




def get_wenyanwen():
    """获取文言文"""
    url = 'http://api.tianapi.com/txapi/lzmy/index'
    params = {'key':'ce9683fb3b39fb211a0834c09165c599'}

    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    if(res_dict['code'] == 200):
        content = res_dict['newslist'][0]
        text = content['saying']+'\n'+content['transl']+' ——'+content['source']


    return text


def getBingImg():
    """获取必应每日一图"""
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'

    res = requests.get(url)
    res_dict = json.loads(res.text)
    img_url = 'https://cn.bing.com' + res_dict['images'][0]['url']
    img_cpright = res_dict['images'][0]['copyright']
    
    text = f'[CQ:image,file={img_url}]\n——{img_cpright}'
    
    return text


def get_history_today():
    """获取历史上的今天"""
    url = 'http://api.tianapi.com/txapi/lishi/index'
    params = {'key':'ce9683fb3b39fb211a0834c09165c599'}
    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    text = ""
    if(res_dict['code'] == 200):
        content = res_dict['newslist'][-1]
        text = content['lsdate']+' '+content['title']
    
    return text

def english_img():
    """获取金山词霸英语每日一图"""
    url = 'http://api.tianapi.com/txapi/everyday/index'
    params = {'key':'ce9683fb3b39fb211a0834c09165c599'}
    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    text = ""
    if(res_dict['code'] == 200):
        image_url =  res_dict['newslist'][0]['imgurl']
        text = f"[CQ:image,file={image_url}]"
        

    
    return text




def caihongpi(user_id,type='group'):
    """获取彩虹屁"""
    url = 'http://api.tianapi.com/txapi/caihongpi/index'
    params = {'key':'ce9683fb3b39fb211a0834c09165c599'}
    res = requests.get(url,params=params)
    res_dict = json.loads(res.text)

    text = ""
    if(res_dict['code'] == 200):
        text = res_dict['newslist'][0]['content']
    
    return text
        


#DEBUG
if __name__ == '__main__':
    print(get_history_today())
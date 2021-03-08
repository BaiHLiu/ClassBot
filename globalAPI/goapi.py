'''
Descripttion: 
version: 
Author: Catop
Date: 2021-02-10 09:38:39
LastEditTime: 2021-03-08 13:01:53
'''
#coding:utf-8
import os
import sys
import json
import requests
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from globalAPI.CB_logger import plog as CB_logger

cwd = os.path.dirname(os.path.realpath(__file__))

#读取配置
conf_info = cwd+"/../conf/botConf.json"
with open(conf_info,"r") as f:
    conf_dict = json.load(f)
    
gocq_addr = conf_dict['gocq']['Address']
gocq_port = conf_dict['gocq']['Port']



def sendMsg(user_id,message):

    url = f'http://{gocq_addr}:{gocq_port}/send_private_msg'
    data = {'user_id':user_id,'message':message}
    res = requests.get(url,params=data)
    CB_logger('goapi',f"回复私聊消息@{user_id}：{message[:30]}")
    return res.text

def sendGroupMsg(group_id,message):
    url = f'http://{gocq_addr}:{gocq_port}/send_group_msg'
    data = {'group_id':group_id,'message':message}
    res = requests.get(url,params=data)
    CB_logger('goapi',f"回复群消息@{group_id}：{message[:30]}")
    return res.text


def add_request(request_flag):
    url = f'http://{gocq_addr}:{gocq_port}/set_friend_add_request'
    data = {'flag':str(request_flag)}
    res = requests.get(url,params=data)
    CB_logger('goapi','加好友成功')
    return res.text


if __name__=='__main__':
    sendMsg('601179193','test')
    #sendGroupMsg('1038368144','信安20-2')
    
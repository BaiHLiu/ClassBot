'''
Descripttion: 
version: 
Author: Catop
Date: 2021-02-10 09:38:39
LastEditTime: 2021-03-06 16:12:35
'''
#coding:utf-8
import requests

def sendMsg(user_id,message):

    url = 'http://127.0.0.1:5800/send_private_msg'
    data = {'user_id':user_id,'message':message}
    res = requests.get(url,params=data)
    print(f"[goapi]回复私聊消息@{user_id}：{message[:20]}")
    return res.text

def sendGroupMsg(group_id,message):
    url = 'http://127.0.0.1:5800/send_group_msg'
    data = {'group_id':group_id,'message':message}
    res = requests.get(url,params=data)
    print(f"[goapi]回复群消息@{group_id}：{message[:20]}")
    return res.text


def add_request(request_flag):
    url = 'http://127.0.0.1:5800/set_friend_add_request'
    data = {'flag':str(request_flag)}
    res = requests.get(url,params=data)
    print("[goapi]加好友成功")
    return res.text


if __name__=='__main__':
    #sendMsg('601179193','test')
    #sendGroupMsg('1038368144','信安20-2')
    pass
'''
Descripttion: 
version: 
Author: Catop
Date: 2021-02-10 07:47:09
LastEditTime: 2021-06-19 16:34:27
'''
#coding:utf-8


import os
import time
import random
import json
from flask import Flask,request,jsonify

from globalAPI import goapi as goapi
from globalAPI import dbconn as dbconn
from globalAPI.CB_logger import plog as CB_logger

from router import CB_router as CB_router



app = Flask(__name__)
@app.route('/', methods=['POST'])
def getEvent():
    data = request.json
    post_type = data.get('post_type')
    if(post_type == 'message'):
        message_type = data.get('message_type')
        message = data.get('message')
        message_id = data.get('message_id')
        user_id = str(data.get('user_id'))
        sender = data.get('sender')
        #sender为dict
        if(message_type=='private'):
            #处理私聊消息
            CB_logger('Flask',f'接收私聊消息@{user_id}:{message[:20]}')
            CB_router(user_id,message,'private',sender=sender,message_id=message_id)
        elif(message_type=='group'):
            #处理群聊消息
            group_id = data.get('group_id')
            
            CB_logger('Flask',f'接收群消息@{group_id}@{user_id}:{message[:20]}')
            CB_router(user_id,message,'group',group_id,sender=sender,message_id=message_id)

            
    elif(post_type == 'request'):
        request_type = data.get('request_type')
        if(request_type=='friend'):
            user_id = str(data.get('user_id'))
            comment = str(data.get('comment'))
            flag = str(data.get('flag'))
            CB_logger('Flask',f'\n[flask]接收加好友请求@{user_id}:{comment[:20]}')
            time.sleep(random.randint(5,10))
            goapi.add_request(flag)
            time.sleep(random.randint(5,10))
            goapi.sendMsg(user_id,"欢迎！\n请先注册，例如'注册@张三@信安20-2'\n 班级请严格按格式输入，否则可能统计不上哦")
    else:
        #暂不处理其他类型上报，为防止go-cq报错而设置
        pass
    

    return data


if __name__ == '__main__':
    conf_info = "conf/botConf.json"
    with open(conf_info,"r") as f:
        conf_dict = json.load(f)
    flask_host = conf_dict['Flask']['Host']
    flask_port = conf_dict['Flask']['Port']
    flask_debug = conf_dict['Flask']['Debug']
    if flask_debug=="False":
        flask_debug = False
    else:
        flask_debug = True

        
    app.run(host=flask_host,port=flask_port,debug=flask_debug)

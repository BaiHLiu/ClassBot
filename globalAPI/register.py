'''
Descripttion: 注册新用户
version: 
Author: Catop
Date: 2021-03-07 13:47:18
LastEditTime: 2021-03-28 15:19:21
'''

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import goapi
import inputFilter
import dbconn as globalDB


def register_prompt(user_id,message):
    """用户注册逻辑"""
    if('注册' in message):
        err_promot = '输入好像有点问题呢\n注册格式："注册@姓名@班级"'
        try:
            user_name = message.split('@')[1]
            user_class = message.split('@')[2]
            #简单过滤用户输入
            if not(inputFilter.is_Chinese(user_name) and inputFilter.check_length(user_name)):
                goapi.sendMsg(user_id,err_promot)
                return
            if not(inputFilter.is_valid(user_class) and inputFilter.check_length(user_class)):
                goapi.sendMsg(user_id,err_promot)
                return
                
        except:
            goapi.sendMsg(user_id,err_promot)
        else:
            if(globalDB.check_register(user_id)):
                goapi.sendMsg(user_id,'您已注册过啦~')
                re_register_user(user_id,user_name,user_class)
            else:
                    register_user(user_id,user_name,user_class)
    return 


def register_user(user_id,user_name,user_class):
    if(globalDB.register_user(user_id,user_name,user_class) == 1):
        goapi.sendMsg(user_id,'注册成功，现在可以开始上传图片了~')
    else:
        goapi.sendMsg(user_id,'注册失败'+f"user_id={user_id},user_name={user_name},user_class={user_class}")
        
def re_register_user(user_id,user_name,user_class):
    if(globalDB.re_register_user(user_id,user_name,user_class) == 1):
        goapi.sendMsg(user_id,'已更新字段')
    else:
        goapi.sendMsg(user_id,'更新字段失败:'+f"user_id={user_id},user_name={user_name},user_class={user_class}")
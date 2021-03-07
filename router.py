'''
Descripttion: 路由消息，根据前缀/指令分发给不同插件
version: 
Author: Catop
Date: 2021-03-06 12:21:07
LastEditTime: 2021-03-07 14:46:10
'''
#coding:utf-8

from globalAPI import goapi as goapi
from globalAPI import dbconn as dbconn
from globalAPI import register as register
from changZheng import plugin_main as changZheng
from adminManager import adminConf as adminConf

#设置支持的指令
user_cmd = ['截图上传']

def CB_router(user_id,message,message_type,group_id=0,raw=False,sub_type='',message_id=0,sender=[]):
    """路由message事件"""
    #检查是否为注册用户
    if not(dbconn.check_register(user_id)) and not('注册' in message):
        goapi.sendMsg(user_id,'您还没注册呢，请回复指令注册\n例如"注册@张三@信安20-2"\n(班级请严格按格式输入，否则可能统计不上哦)')
        return
    
    #响应任何用户的响应注册指令
    if('注册' in message):
        register.register_prompt(user_id,message)
        return

    #管理员热更新指令
    if('/sudo' in message):
        sudo_act(user_id,message)
        return


    #将用户指令写入数据库
    if(message in user_cmd):
        dbconn.add_cmd(user_id,message)
        goapi.sendMsg(user_id,message+" 开始~")
        return

    #分发指令(distribute to plugins)
    dis_plugins(user_id,message)


    return


def dis_plugins(user_id,message):
    """读取上条命令，分发给不同插件"""
    if(dbconn.check_cmd(user_id) == '截图上传'):
        changZheng.readMsg(user_id,message)
        dbconn.add_cmd(user_id,"")
    elif(1==2):
        pass
    else:
        msg = "您要做什么呢？请先输入指令，目前支持的指令有:\n"
        for i in range(0,len(user_cmd)):
            msg += f"{i+1}:{user_cmd[i]}\n"
        
        goapi.sendMsg(user_id,msg)
    
    #清空指令
    dbconn.add_cmd(user_id,"")

    return

def sudo_act(user_id,message):
    if('/sudo' in message and (user_id=='601179193' or user_id=="29242764")):
        #try:
        if('增加管理员' in message):
            admin_id = message.split('@')[1]
            group_id = message.split('@')[2]
            goapi.sendMsg(user_id,str(adminConf.add_admin(admin_id,group_id)))
        elif('删除管理员' in message):
            admin_id = message.split('@')[1]
            goapi.sendMsg(user_id,str(adminConf.del_admin(admin_id)))
        elif('展示管理员' in message):
            goapi.sendMsg(user_id,str(adminConf.show_admin()))
        else:
            goapi.sendMsg(user_id,'增加管理员\n删除管理员\n展示管理员')    
    return 
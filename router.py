'''
Descripttion: 路由消息，根据前缀/指令分发给不同插件
version: 
Author: Catop
Date: 2021-03-06 12:21:07
LastEditTime: 2021-06-19 16:47:30
'''
#coding:utf-8
from globalAPI import CB_logger as logger
from globalAPI import goapi 
from globalAPI import dbconn as dbconn
from globalAPI import register as register
from changZheng import plugin_main as changZheng
from adminManager import adminConf as adminConf
from classAlert import CA_main as classAlert
import amuseActive

###########################################
#无前缀主动命令响应
PERMIT_AUTO_QID = [159972680,441264425,1091802120]

###########################################


def CB_router(user_id,message,message_type,group_id=0,raw=False,sub_type='',message_id=0,sender=[]):
    """路由message事件"""
    #检查是否为注册用户(已弃用)
    # if not(dbconn.check_register(user_id)) and not('注册' in message):
    #     goapi.sendMsg(user_id,'您还没注册呢，请回复指令注册\n例如"注册@张三@信安20-2"\n(班级请严格按格式输入，否则可能统计不上哦)')
    #     return
    
    #响应任何用户的响应注册指令
    if('注册' in message):
        register.register_prompt(user_id,message)
        return

    #管理员热更新指令
    if('/sudo' in message):
        sudo_act(user_id,message)
        return

    #alert功能管理员指令
    if('/alert' in message):
        classAlert.readMsg(user_id,message)
        return
    
    #主动娱乐插件，以#开头
    if(message[0] == '#'):
        if(message_type == 'private'):
            amuseActive.controller.amuseRouter(message,user_id,'private',message_id)
        elif(message_type == 'group'):
            amuseActive.controller.amuseRouter(message,group_id,'group',message_id)

        return

    
    #无命令主动响应事件，需配置PERMIT_AUTO_QID
    if(user_id in PERMIT_AUTO_QID )or (group_id in PERMIT_AUTO_QID):
        #响应图片
        logger.plog('router','触发无命令图片响应')
        if(message[0:4] == '[CQ:'):
            if(message_type == 'private'):
                amuseActive.imgrec.handler(message, user_id, message_type, message_id)
            elif(message_type == 'group'):
                amuseActive.imgrec.handler(message, group_id, message_type, message_id)

        return

    # #将用户指令写入数据库
    # if(message_type == 'private'):
    #     if(message.isdigit()):
    #         if(int(message)>=0 and int(message)<=len(user_cmd)-1):
    #             message = user_cmd[int(message)]
                
    #             dbconn.add_cmd(user_id,message)
    #             goapi.sendMsg(user_id,message+" 开始~")
    #         else:
    #             goapi.sendMsg(user_id,"指令有误，请检查")
    
    #         return
    
        #分发指令(distribute to plugins)
        dis_plugins(user_id,message)


    return


def dis_plugins(user_id,message):
    """长征路截图上传机器人，已弃用"""

    #changZheng.readMsg(user_id,message)
    
    pass
    

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
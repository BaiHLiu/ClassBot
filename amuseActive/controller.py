'''
Description: 主动娱乐控制器，动态引入插件并调用其hander()函数
Author: Catop
Date: 2021-06-19 13:53:26
LastEditTime: 2021-06-19 16:11:39
'''

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import globalAPI.goapi as goapi
import globalAPI.CB_logger as logger

########################################
#设置不允许群组
DISABLE_GROUP = ['']
#设置不允许好友
DISABLE_FRIEND = ['']

#设置启用的插件名称
#出于安全考虑，请每次新增插件后手动在此更新。
ENABLED_PLUGINS = ['tiangou','wyy','imgrec']
########################################


def amuseRouter(message, qid, type, message_id):
    """娱乐插件路由"""
    if(qid in DISABLE_GROUP) or (qid in DISABLE_FRIEND):
        if(type == 'private'):
            goapi.sendMsg(qid,"抱歉，您暂无此权限")
        else:
            goapi.sendGroupMsg(qid,"抱歉，您所在的群组暂无此权限")
    
    else:
        try:
            message = message[1:]
            if not('[CQ' in message):
                #无CQ码，空格分割函数名和参数列表
                func_name = message.split(' ')[0]
            else:
                #有CQ码，按CQ码分割函数名和参数列表
                func_name = message.split('[')[0]
            #检查插件名称合法性，防止eval注入
            if(func_name not in ENABLED_PLUGINS):
                logger.plog("AmuseCtrl",f"找不到娱乐模块'{func_name}'","warning")
                if(type == 'private'):
                    goapi.sendMsg(qid,f"还没有'{func_name}'功能呢~")
                else:
                    goapi.sendGroupMsg(qid,f"还没有'{func_name}'功能呢~")


            cmd = f"__import__('{func_name}').handler('{message}','{qid}','{type}','{message_id}')"
            eval(cmd)

        except:
            logger.plog("AmuseCtrl",f"用户调用娱乐模块'{func_name}'失败\n命令：{cmd}","error")
        else:
            logger.plog("AmuseCtrl",f"成功调用娱乐模块'{func_name}'")

    


#DEBUG
if __name__ == "__main__":
    amuseRouter('#tiangou')
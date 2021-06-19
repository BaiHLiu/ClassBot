'''
Description: 每日一言定时器
Author: Catop
Date: 2021-06-19 13:13:51
LastEditTime: 2021-06-19 13:53:40
'''

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import globalAPI.goapi as goapi
import globalAPI.CB_logger as logger
import apis


#群组列表1
group_list1 = ['515192555','949773437']

def timer_task():
    """定时执行任务"""
    #命令行执行参数
    if(len(sys.argv)>1):
        opt = sys.argv[1]
    else:
        logger.plog("timer","命令行参数获取出错")
        return
        

    if(opt == 'zaoan'):
        #早安
        for groupId in group_list1:
            goapi.sendGroupMsg(groupId,"☀️早安\n"+apis.get_history_today()+"\n"+apis.english_img())
    elif(opt == 'wanan'):
        for groupId in group_list1:
            goapi.sendGroupMsg(groupId,"时间不早啦，赶快休息吧。\n"+apis.getBingImg())

#timer run
if __name__ == "__main__":
    timer_task()

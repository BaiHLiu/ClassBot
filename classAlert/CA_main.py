'''
Descripttion: ClassAlert功能主程序
version: 
Author: Catop
Date: 2021-03-27 20:28:25
LastEditTime: 2021-03-28 15:13:31
'''

import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import json
import time
import random
import shutil

import globalAPI.goapi as goapi
import adminManager.adminConf as adminConf

import CA_dbconn as dbconn
import CA_compress as compress


WEB_PATH = '/www/wwwroot/cloud1.catop.top/ClassAlert/'
cwd = os.path.dirname(os.path.realpath(__file__))

def readMsg(user_id,message):
    admin_list = adminConf.show_admin()
    if(str(user_id) in admin_list.keys()):
        try:
            user_class = dbconn.get_user_by_id(user_id)['user_class']
            if(user_class == None):
                goapi.sendMsg(user_id,'您还未绑定任何组织。')
                return

            if('新建' in message):
                title = message.split('@')[1]
                description = message.split('@')[2]
                pid = dbconn.add_project(title,description,user_class)
                goapi.sendMsg(user_id,f"----新建项目----\n项目id:{pid}\n项目标题:{title}\n项目描述:{description}")
                url = f"https://cloud1.catop.top:8002/ClassAlert/?pid={pid}"
                goapi.sendMsg(user_id,f"完成后请确认：\n项目:{title}\n链接:{url}")


            elif('提醒' in message):
                pid = message.split('@')[1]
                project_class = dbconn.get_project(pid)['user_class']
                if not(project_class == user_class):
                    goapi.sendMsg(user_id,f"该项目归属于{project_class}，您注册在{user_class}，暂无管理权限。")
                    return

                url = f"https://cloud1.catop.top:8002/ClassAlert/?pid={pid}"
                alert_list = dbconn.get_unset_user(pid)
                title = dbconn.get_project(pid)['title']
                err_list = []
                for uid in alert_list.keys():
                    try:
                        user_name = dbconn.get_user_by_id(uid)['user_name']
                        ####连续发送多条带链接私聊消息可能会被风控
                        goapi.sendMsg(uid,f"亲爱的{user_name},不好意思打扰一下，请及时完成{title}\n点击确认:{url}")
                        #goapi.sendMsg(uid,f"{user_name}您好,请及时完成{title}\n，完成后点击链接确认。（连续发送多条带链接私聊消息可能会被风控，请自行查阅管理员创建的链接）")
                    except:
                        err_list.append(str(uid))

                    dbconn.unset_count(uid)
                    time.sleep(random.randint(2,3))

                goapi.sendMsg(user_id,f"已发送私聊消息{len(alert_list.keys())}条，失败{len(err_list)}条\n失败名单:{err_list}")
            elif('统计' in message):
                pid = message.split('@')[1]
                project_class = dbconn.get_project(pid)['user_class']
                if not(project_class == user_class):
                    goapi.sendMsg(user_id,f"该项目归属于{project_class}，您注册在{user_class}，暂无管理权限。")
                    return

                alert_list = dbconn.get_unset_user(pid)
                msg = "----未完成名单----\n"
                msg += f"项目id:{pid}\n"
                for uid in alert_list.keys():
                    msg += f"{uid}({alert_list[uid]})\n"
                msg += f"共计{len(alert_list.keys())}条"
                goapi.sendMsg(user_id,msg)

                msg = "----已完成名单----\n"
                completed_list = {}
                user_list = dbconn.get_userinfo(user_class)
                submit_list = dbconn.get_submit_info(pid)
                for i in range(0,len(user_list)):
                    user_name = user_list[i]['user_name']
                    file_flag = 0
                    complete_flag = 0
                    file_name = ""
                    for k in range(0,len(submit_list)):
                        if(submit_list[k]['username'] == user_name):
                            complete_flag = 1
                            #检查是否有文件
                            if not(submit_list[k]['file_name'] == ''):
                                file_flag = 1
                                file_name = submit_list[k]['file_name']

                    if(complete_flag == 1):
                        msg += f"{user_name}"
                    else:
                        continue

                    if(file_flag == 1):
                        msg += f"-{file_name[10:]}\n"
                    else:
                        msg += "\n"
                    
                goapi.sendMsg(user_id,msg)


            elif('成员' in message):
                user_list = dbconn.get_userinfo(user_class)

                msg = f"{user_class}\n"
                for i in range(0,len(user_list)):
                    msg += f"{user_list[i]['user_name']}  次数:{user_list[i]['user_count']}\n"
                msg += f"共计{len(user_list)}人"
                
                goapi.sendMsg(user_id,msg)
            elif('打包' in message):
                pid = message.split('@')[1]
                project_class = dbconn.get_project(pid)['user_class']
                
                if not(project_class == user_class):
                    goapi.sendMsg(user_id,f"该项目归属于{project_class}，您注册在{user_class}，暂无管理权限。")
                    return

                comp_ret = archive_proj_files(pid)
                goapi.sendMsg(user_id,f"----打包完毕----\n项目id:{pid}\n有效文件:{comp_ret['file_num']}\n下载地址:https://cloud1.catop.top:8002/ClassAlert/compressed/{comp_ret['file_name']}")
            else:
                goapi.sendMsg(user_id,'/alert\n新建@项目标题@项目描述\n提醒@项目id\n成员\n统计@项目id\n打包@项目id')
        except Exception as err:
            goapi.sendMsg(user_id,f'错误{err}\n文件:{err.__traceback__.tb_frame.f_globals["__file__"]}\n行数{err.__traceback__.tb_lineno}')

        else:
            pass

    else:
        goapi.sendMsg(user_id,'您暂无管理员权限，请联系加入')

    return


def move_file(old_name,user_name,pid):
    pref_name = old_name.split('.')[0]
    ext_name = old_name.split('.')[1]

    new_name = f"{user_name}_项目{pid}.{ext_name}"
    shutil.copy(WEB_PATH+'/upload/'+old_name,cwd+'/tmp/'+new_name)
    #print(f"复制:{old_name} -> {new_name}成功")

    return new_name

def archive_proj_files(pid):
    """将指定pid的项目文件打包"""
    submit_info = dbconn.get_submit_info(pid)
    new_file_list = [] #新文件名列表
    for i in range(0,len(submit_info)):

        if(submit_info[i]['file_name'] == '' or  submit_info[i]['username']==''):
            #指定sid无姓名或文件
            continue


        user_name = submit_info[i]['username']
        not_allowed_chars = ['.',' ','/','`'] #过滤姓名问题
        for char_index in range(0,len(not_allowed_chars)):
            user_name = user_name.replace(not_allowed_chars[char_index],'')

        new_name = move_file(submit_info[i]['file_name'],user_name,pid)
        
        if not new_name in new_file_list:
            new_file_list.append(new_name)
    
    #print(new_file_list)
    comp_ret = compress.zip_file(new_file_list)

    return comp_ret
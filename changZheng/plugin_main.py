'''
Descripttion: 
version: 
Author: Catop
Date: 2021-02-28 08:57:49
LastEditTime: 2021-03-27 20:32:57
'''
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import json
import time
import urllib.parse
import requests

import adminManager.adminConf as adminConf
import globalAPI.dbconn as globalDB
import globalAPI.goapi as goapi
import globalAPI.inputFilter as inputFilter

import compress
import CZ_dbconn as dbconn
import ocrplus

cwd = os.path.dirname(os.path.realpath(__file__))


def readMsg(user_id,message):
    #处理消息核心
    user_id = str(user_id)
    #管理员列表
    admin_list = adminConf.show_admin()
    
    if('image' in message):
        if(globalDB.check_register(user_id)):
            #用户已注册
            get_img(user_id,message)
        else:
            #用户未注册
            goapi.sendMsg(user_id,'您还没注册呢，请输入例如"注册@张三@计科20-2"\n 班级请严格按格式输入，否则可能统计不上哦')
        return 
    
    if('/admin' in message):
        user_class = globalDB.get_user(user_id)['user_class']
        upload_date = time.strftime("%Y-%m-%d", time.localtime()) 
        print(user_id)
        if(user_id in admin_list.keys()):
            group_id = admin_list[user_id]
            if('群提醒' in message):
                send_alert(group_id,globalDB.get_user(user_id)['user_class'],'group')
            elif('提醒'in message):
                send_alert(user_id,globalDB.get_user(user_id)['user_class'],'private')
                upload_date = time.strftime("%Y-%m-%d", time.localtime()) 
                time.sleep(1)
                #ocr_err_upload(user_id,user_class,upload_date)
                ocr_err_upload(user_id,user_class,upload_date)
                time.sleep(2)
                send_images_info(user_id,user_class)
            elif('打包'in message):
                cmp_ret = compress.zip_file(upload_date,globalDB.get_user(user_id)['user_class'])
                goapi.sendMsg(user_id,f"---打包完毕---\n共处理:{cmp_ret['file_num']}张照片")
                goapi.sendMsg(user_id,'下载地址:http://static.catop.top:8001/'+urllib.parse.quote(cmp_ret['file_name']))
            elif('成员'in message):
                list_class_menbers(user_id,user_class)
            else:
                goapi.sendMsg(user_id,"目前支持以下管理指令呢：\n群提醒\n提醒\n打包\n成员\n")
        else:
            
            goapi.sendMsg(user_id,"无管理权限")

    

        
            
def get_img(user_id,message):
    #从message中解析到图片下载地址，并保存数据库，下载文件
    try:
        img_url = message.split('url=')[1][0:-1]
        user_name = globalDB.get_user(user_id)['user_name']
        user_class = globalDB.get_user(user_id)['user_class']
        upload_date = time.strftime("%Y-%m-%d", time.localtime()) 
        upload_time = time.strftime("%H:%M:%S", time.localtime()) 

        #修改文件名格式(注意只保存文件名和数据库中显示的file_name改变，目录等名称不变)
        file_date = time.strftime("%Y%m%d", time.localtime()) 
        
        #安全过滤
        if not(img_url[0:24] == 'http://c2cpicdw.qpic.cn/'):
            goapi.sendMsg(user_id,'图片url解析错误')
            return
        
        #判断文件目录是否存在
        if not(os.path.exists(f"{cwd}/images/{upload_date}")):
            os.mkdir(f"{cwd}/images/{upload_date}")
        if not(os.path.exists(f"{cwd}/images/{upload_date}/{user_class}")):
            os.mkdir(f"{cwd}/images/{upload_date}/{user_class}")

        file_name = f"/{upload_date}/{user_class}/{user_class}班-{user_name}-{file_date}.jpg"
        if(dbconn.check_today_upload(user_id,upload_date)):
            goapi.sendMsg(user_id,'您今天已经上传过照片啦，已覆盖之前的图片~')
        
        download_img(img_url,file_name)
        #print(img_url)
    except Exception as err:
        goapi.sendMsg(user_id,'图片下载出错了！')
        print(err)
    else:
        print("成功处理图片:"+file_name)
        goapi.sendMsg(user_id,"成功处理图片，正在识别...\n"+f"{user_class}班-{user_name}-{file_date}.jpg")

        """图片识别部分"""
        try:
            print(file_name)
            ocr_ret = ocrplus.ocr_img(f"{cwd}/images"+file_name)
            ocr_err_code = ocr_ret['err_code']
            if(ocr_err_code == 0):
                goapi.sendMsg(user_id,f"参赛次数:{ocr_ret['个人参赛次数']}\n个人积分:{ocr_ret['个人积分']}")
                ocr_times = ocr_ret['个人参赛次数']
                ocr_scores = ocr_ret['个人积分']
            else:
                print("图片无法识别:"+ocr_ret)
                #图片识别接口返回无法识别
                goapi.sendMsg(user_id,f"OCR无法识别，图片将人工复核~")
                dbconn.insert_img(user_id,file_name,upload_date,upload_time,'1','0','0')
                return 
        except:
            #图片识别接口出错
            print("OCR接口出错:")
            goapi.sendMsg(user_id,f"qwq图片识别接口出错了！图片将人工复核~")
            dbconn.insert_img(user_id,file_name,upload_date,upload_time,'1','0','0')
        else:
            dbconn.insert_img(user_id,file_name,upload_date,upload_time,ocr_err_code,ocr_times,ocr_scores)

    return 


def download_img(img_url,file_name):
    res = requests.get(img_url, stream=True)
    if res.status_code == 200:
        open(f'{cwd}/images'+file_name, 'wb').write(res.content)
        #print("image"+file_name+"saved successfully.")




def send_alert(group_id,user_class,type='private'):
    group_menbers = globalDB.get_class_members(user_class)
    current_date = time.strftime("%Y-%m-%d", time.localtime()) 
    alert_users = {}
    #user_id:last_date
    for user_id in group_menbers:
        #print(user_id)
        try:
            last_date = dbconn.check_status(user_id)
        except TypeError:
            #还没发过照片
            alert_users[user_id] = '无记录'
        else:
            if(str(last_date)!=str(current_date)):
                alert_users[user_id] = str(last_date)[5:]
                
    
    #print(alert_users)
    msg = f"今天还有{len(alert_users)}位小可爱未完成哦\n"


    if(type=='private'):
        for user_id in alert_users.keys():
            last_date = alert_users[user_id]
            msg += f"{globalDB.get_user(user_id)['user_name']}({alert_users[user_id]})"
            msg += f"{globalDB.get_user(user_id)['user_count']}\n"
        msg+=f"{user_class} {current_date}\n完成情况:{len(group_menbers)-len(alert_users)}/{len(group_menbers)}"
        goapi.sendMsg(group_id,msg)
    elif(type=='group'):
        for user_id in alert_users.keys():
            globalDB.add_user_count(str(user_id))
            last_date = alert_users[user_id]
            msg += f"[CQ:at,qq={user_id}]({alert_users[user_id]})-"
            msg += f"{globalDB.get_user(user_id)['user_count']}\n"
        msg += f"{user_class} {current_date}\n完成情况:{len(group_menbers)-len(alert_users)}/{len(group_menbers)}"
        goapi.sendGroupMsg(group_id,msg)
    
def list_class_menbers(user_id,user_class):
    msg = f"{user_class}成员情况：\n"
    ret = globalDB.get_class_members(user_class)
    for i in range(0,len(ret)):
        msg += f"{ret[i]} {globalDB.get_user(str(ret[i]))['user_name']} "
        msg += f"{globalDB.get_user(str(ret[i]))['user_count']}\n"
    msg += f"共计{str(len(ret))}人"

    goapi.sendMsg(user_id,msg)
    

def ocr_err_upload(user_id,user_class,upload_date):
    """为管理员上报ocr错误的图片"""
    msg = "OCR无法识别以下图片:\n"
    err_list = []
    class_menbers = globalDB.get_class_members(user_class)
    for i in range(0,len(class_menbers)):
        img_date = dbconn.check_status(class_menbers[i])
        if(str(img_date) == str(upload_date)):
            img_info = dbconn.get_latest_img_info(class_menbers[i],upload_date)[0]
            #print(img_info)
            if(img_info['ocr_err_code'] == 1):
                print(img_info)
                err_list.append(img_info['file_name'])

    for i in range(0,len(err_list)):
        cqCode = f"[CQ:image,file=file:{cwd}/images{err_list[i]}]"
        msg += f"{cqCode}\n"
    msg += f"数量:{len(err_list)}/{len(class_menbers)}"

    goapi.sendMsg(user_id,msg)
    return msg

def send_images_info(user_id,user_class):
    """上报班级图片情况（次数和成绩）"""
    class_menbers = globalDB.get_class_members(user_class)
    today_upload_count = 0
    upload_date = time.strftime("%Y-%m-%d", time.localtime()) 
    msg = f"{user_class} {upload_date}情况:\n"
    for i in range(0,len(class_menbers)):
        if(str(dbconn.check_status(class_menbers[i])) == str(upload_date)):
            today_upload_count += 1
            img_info = dbconn.get_latest_img_info(class_menbers[i],upload_date)[0]
            if(img_info['ocr_err_code'] == 0):
                msg += f"·{globalDB.get_user(class_menbers[i])['user_name']} 次数{img_info['ocr_times']} 分数{img_info['ocr_scores']}\n"
            else:
                msg += f"·{globalDB.get_user(class_menbers[i])['user_name']} 未识别到\n"
    
    msg += f"共计{today_upload_count}张照片"

    goapi.sendMsg(user_id,msg)
    return msg

if __name__ == "__main__":
    readMsg('601179193','注册@刘佰航@信安20-2')
'''
Descripttion: 全局数据库调用
version: 
Author: Catop
Date: 2021-03-06 12:23:03
LastEditTime: 2021-03-07 13:46:00
'''
#coding:utf-8
import os
import sys
import pymysql
import json

cwd = os.path.dirname(os.path.realpath(__file__))
conf_info = cwd+"/../conf/botConf.json"


with open(conf_info,"r") as f:
    conf_dict = json.load(f)
db_info = conf_dict['DataBase']
conn = pymysql.connect(host=db_info['Address'],user = db_info['UserName'],passwd = db_info['PassWord'],db = db_info['DBname'])

def check_cmd(user_id):
    """获取最近一条命令"""
    try:
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = f"SELECT last_cmd FROM userinfo WHERE user_id={user_id} LIMIT 1"
        conn.ping(reconnect=True)
        cursor.execute(sql)
        last_cmd = cursor.fetchone()['last_cmd']
        conn.commit()
    except TypeError:
        return ""
    else:
        return last_cmd

def add_cmd(user_id,cmd):
    """写入用户指令"""
    #请自行处理表中无此用户的情况
    succ_flag = 0
    try:
        cmd = cmd[:49]
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = f"UPDATE userinfo SET last_cmd=%s WHERE user_id=%s"
        params = [cmd,user_id]
        conn.ping(reconnect=True)
        cursor.execute(sql,params)
        conn.commit()
    except:
        pass
    else:
        succ_flag = 1

    
    return succ_flag


def check_register(user_id):
    """检查用户是否注册"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT uid FROM userinfo WHERE user_id={user_id} LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    user_info = cursor.fetchall()
    conn.commit()

    if(len(user_info)>=1):
        return 1
    else:
        return 0


def get_user(user_id):
    """获取用户姓名和班级"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT user_name,user_class FROM userinfo WHERE user_id={user_id} LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    user_info = cursor.fetchone()
    conn.commit()

    return user_info




def register_user(user_id,user_name,user_class):
    """注册新用户"""

    try:
        params = [user_id,user_name,user_class]
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = f"INSERT INTO userinfo(user_id,user_name,user_class) VALUES(%s,%s,%s)"
        conn.ping(reconnect=True)
        cursor.execute(sql,params)
        conn.commit()
    except:
        flag=0
    else:
        flag=1

    return flag


def re_register_user(user_id,user_name,user_class):
    """重新注册，更新用户信息"""
    try:
        params = [user_name,user_class,user_id]
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = f"UPDATE userinfo SET user_name=%s,user_class=%s WHERE user_id=%s"
        conn.ping(reconnect=True)
        cursor.execute(sql,params)
        conn.commit()
    except:
        flag=0
    else:
        flag=1
    return flag


def get_class_members(user_class):
    """获取班级成员QQ号list"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    params = [user_class]
    sql = f"SELECT user_id FROM userinfo WHERE user_class=%s"
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    sql_ret = cursor.fetchall()
    conn.commit()
    class_menbers = []

    for i in range(0,len(sql_ret)):
        class_menbers.append(sql_ret[i]['user_id'])
    return class_menbers


if __name__ == "__main__":
    print(add_cmd('601179193','test1111111'))
    print(check_cmd('601179193'))
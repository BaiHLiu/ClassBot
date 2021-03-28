'''
Descripttion:ClassAlert连接私有数据库 
version: 
Author: Catop
Date: 2021-03-27 20:25:23
LastEditTime: 2021-03-28 15:17:48
'''
import os
import sys
import json
import pymysql
import time


cwd = os.path.dirname(os.path.realpath(__file__))
conf_info = cwd+"/../conf/botConf.json"

with open(conf_info,"r") as f:
    conf_dict = json.load(f)
db_info = conf_dict['DataBase']

conn = pymysql.connect(host=db_info['Address'],user = db_info['UserName'],passwd = db_info['PassWord'],db = db_info['DBname'])



def add_project(ptitle,pdesc,user_class):
    """新建项目"""
    pdate = time.strftime("%Y-%m-%d", time.localtime())
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    params = [ptitle,pdesc,user_class,pdate]
    sql = f"INSERT INTO CA_project(title,description,user_class,date) VALUES(%s,%s,%s,%s)"
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    conn.commit()

    #返回影响的主键id
    return cursor.lastrowid
    

def get_unset_user(pid):
    """获取未完成用户的用户名和qq号"""
    user_list = get_userinfo(get_project(pid)['user_class'])
    unset_list = {}
    for i in range(0,len(user_list)):
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        params = [pid,user_list[i]['user_name']]
        sql = f"SELECT * FROM CA_submit WHERE (pid=%s AND username=%s) LIMIT 1"
        conn.ping(reconnect=True)
        cursor.execute(sql,params)
        user = cursor.fetchone()
        if not (user):
            unset_list[user_list[i]['user_id']] = user_list[i]['user_name']
    conn.commit()

    return unset_list

def unset_count(user_id):
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"UPDATE userinfo SET user_count=user_count+1 WHERE user_id={user_id}"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    conn.commit()

def get_project(pid):
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT * FROM CA_project WHERE id={pid} LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    project_info = cursor.fetchone()
    conn.commit()

    return project_info

def get_userinfo(user_class):
    """获取班级所有成员信息"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT * FROM userinfo WHERE user_class=%s ORDER BY user_count DESC"
    params = [user_class]
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    userinfo = cursor.fetchall()
    conn.commit()

    return userinfo
    
def get_user_by_id(user_id):
    """获取单个用户信息"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT * FROM userinfo WHERE user_id={user_id}"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    userinfo = cursor.fetchone()
    conn.commit()

    return userinfo
    
def get_submit_info(pid):
    """获取pid对应所有提交信息"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    params = [pid]
    sql = f"SELECT * FROM CA_submit WHERE pid=%s"
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    submit_info = cursor.fetchall()

    conn.commit()
    
    return submit_info

if __name__ == '__main__':
    #print(add_project('python','ok'))
    #print(get_unset_user(2)) 
    #unset_count('601179193')
    #print(get_project(9))
    #print(get_userinfo())
    #print(get_user_by_id('601179193'))
    #print(get_project(99) == None)
    #print(get_userinfo('信安20-2')
    print(len(get_unset_user('45')))
    #unset_count('1746991919')
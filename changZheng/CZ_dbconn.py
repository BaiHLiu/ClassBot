'''
Descripttion: 
version: 
Author: Catop
Date: 2021-02-10 09:10:27
LastEditTime: 2021-03-07 14:33:02
'''
#coding:utf-8
import os
import pymysql
import json
import sys

cwd = os.path.dirname(os.path.realpath(__file__))
conf_info = cwd+"/../conf/botConf.json"


with open(conf_info,"r") as f:
    conf_dict = json.load(f)
db_info = conf_dict['DataBase']

conn = pymysql.connect(host=db_info['Address'],user = db_info['UserName'],passwd = db_info['PassWord'],db = db_info['DBname'])


def insert_img(user_id,file_name,upload_date,upload_time,ocr_err_code,ocr_times,ocr_scores):
    """插入新图片记录"""
    params = [file_name,user_id,upload_date,upload_time,ocr_err_code,ocr_times,ocr_scores]
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"INSERT INTO CZ_imginfo(file_name,user_id,upload_date,upload_time,ocr_err_code,ocr_times,ocr_scores) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    conn.commit()

    return 




def check_today_upload(user_id,upload_date):
    """检查用户当日是否已经上传过"""
    user_id = str(user_id)
    upload_date = str(upload_date)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT imgid FROM CZ_imginfo WHERE(user_id={user_id} AND upload_date='{upload_date}')"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    if(len(cursor.fetchall())>=1):
        conn.commit()
        return 1
        
    else:
        conn.commit()
        return 0
        


def check_status(user_id):
    """返回指定用户最新一条记录的时间"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT upload_date FROM CZ_imginfo WHERE user_id={user_id} ORDER BY upload_date DESC LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    try:
        last_date = cursor.fetchone()['upload_date']
        conn.commit()
    except TypeError:
        last_date = '1970-01-01'
        
    return last_date


def get_latest_img_info(user_id,upload_date):
    """获取指定用户指定时间最新照片信息"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    params = [user_id,upload_date]
    sql = f"SELECT * FROM CZ_imginfo WHERE (user_id=%s AND upload_date=%s) ORDER BY imgid DESC LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    sql_ret = cursor.fetchall()
    conn.commit()

    return sql_ret







if __name__=='__main__':
    #print(get_user(601179193))
    #insert_img('601179193','test.jpg','2021-02-10','09:47:49')
    #print(check_today_upload('601179193','2021-02-10'))
    #print(register_user('29242764','李四','信安20-1'))
    #print(check_status(601179193))
    #print(get_class_members('信安20-2'))
    #print(get_latest_img_info('601179193','2021-02-13'))
    print(conn)
    
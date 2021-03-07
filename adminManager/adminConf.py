'''
Descripttion: 
version: 
Author: Catop
Date: 2021-02-28 09:06:43
LastEditTime: 2021-03-07 14:13:41
'''
import json
import os


admin_info = os.path.dirname(os.path.realpath(__file__))+"/admin_list.txt"

def add_admin(user_id,class_id):
    admin_list = show_admin()
    admin_list[str(user_id)] = str(class_id)
    with open(admin_info,"w") as f:
        json.dump(admin_list,f)
    return admin_list

def del_admin(user_id):
    admin_list = show_admin()
    del admin_list[str(user_id)]
    with open(admin_info,"w") as f:
        json.dump(admin_list,f)
    return admin_list
    


def show_admin():
    with open(admin_info,"r") as f:
        admin_list = json.load(f)
    return admin_list
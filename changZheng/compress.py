'''
Descripttion: 
version: 
Author: Catop
Date: 2021-02-10 20:05:50
LastEditTime: 2021-03-07 14:37:44
'''

import os
import time
import shutil
import zipfile
from os.path import join, getsize

cwd = os.path.dirname(os.path.realpath(__file__))

def zip_file(upload_date,user_class):
    zip_time = str(time.strftime("%H_%M_%S", time.localtime()))
    try:
        src_dir = f"{cwd}/images/{upload_date}/{user_class}"
        zip_name = f"{cwd}/compressed/{upload_date}_{user_class}_{zip_time}.zip"
        z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(src_dir):
            fpath = dirpath.replace(src_dir,'')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                #print(len(filenames))
                z.write(os.path.join(dirpath, filename),fpath+filename)
                print ('==压缩成功==')
        z.close()
    except:
        return 0
    else:
        ret = {}
        ret['file_num'] = str(len(filenames))
        ret['file_name'] = f"{upload_date}_{user_class}_{zip_time}.zip"
        return ret

if __name__ == '__main__':
    print(zip_file('2021-02-10','信安20-2'))
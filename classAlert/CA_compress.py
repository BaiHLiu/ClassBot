'''
Descripttion: 
version: 
Author: Catop
Date: 2021-03-27 20:54:53
LastEditTime: 2021-03-27 20:55:35
'''

import os
import random
import time
import shutil
import zipfile
from os.path import join, getsize

WEB_PATH = '/www/wwwroot/cloud1.catop.top/ClassAlert/'
cwd = os.path.dirname(os.path.realpath(__file__))

def zip_file(file_list):
    zip_time = generate_random_str(10)

    print(f"file_list={file_list}")
    src_dir = cwd+"/tmp/"
    zip_name = f"/www/wwwroot/cloud1.catop.top/ClassAlert/compressed/{zip_time}.zip"
    z = zipfile.ZipFile(zip_name,'w',zipfile.ZIP_DEFLATED)

    for filename in file_list:
        z.write(src_dir+filename,filename)
        os.remove(src_dir+filename)
    z.close()
    print ('==压缩成功==')

    ret = {}
    ret['file_num'] = str(len(file_list))
    ret['file_name'] = f"{zip_time}.zip"
    return ret


def generate_random_str(randomlength=16):
  """
  生成一个指定长度的随机字符串
  """
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]
  return random_str


if __name__ == '__main__':
    print(zip_file(['iShot2021-03-25 22.59.37.png','iShot2021-03-24 17.58.13.png']))
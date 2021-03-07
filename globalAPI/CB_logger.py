'''
Descripttion: 
version: 
Author: Catop
Date: 2021-03-07 12:49:27
LastEditTime: 2021-03-07 13:27:36
'''
import time


def plog(src,message,type='info'):
    """
    [INFO]普通信息
    [WARNING]警告
    [ERROR]错误
    """
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    logmsg = ""
    if(type=='info'):
        prefix = '\033[0;32;40m[INFO]\033[0m'
        src = f'\033[0;32;40m[{src}]\033[0m'
    elif(type=='warning'):
        prefix = '\033[0;33;40m[WARNING]\033[0m'
        src = f'\033[0;33;40m[{src}]\033[0m'
    elif(type=='error'):
        prefix = '\033[1;31;40m[ERROR]\033[0m'
        src = f'\033[1;31;40m[{src}]\033[0m'
    else:
        prefix = f'[{type}]'
    logmsg = f'[{ctime}] {prefix} {src} {message}'
    print(logmsg)
    
    
    return logmsg


if __name__ == '__main__':
    plog('Flask','错误','error')
    plog('changZheng','成功接收','info')
    plog('globalAPI','接口故障','warning')
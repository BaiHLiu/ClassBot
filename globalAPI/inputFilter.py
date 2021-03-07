'''
Descripttion: 过滤用户输入
version: 
Author: Catop
Date: 2021-02-15 18:49:45
LastEditTime: 2021-02-15 19:03:42
'''

def check_length(str):
    if(len(str)>=20):
        return False
    else:
        return True


def is_Chinese(word):
    """判断是否为中文"""
    for ch in word:
        if not '\u4e00' <= ch <= '\u9fff':
            return False
    return True



def is_valid(str):
    """基本黑名单过滤，判断是否符合规定"""
    block_list = [
        ' ',
        '.',
        '/',
        '@',
        ';',
        '&'
    ]
    for ch in str:
        if ch in block_list:
            return False
    
    return True
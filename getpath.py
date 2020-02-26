# !/usr/bin/python
# -*- coding: utf-8 -*-
# File:getpath.py
# File Created:2020-02-26 03:15:34
# Author:Derek.S(derekseli@outlook.com)
# -----
# Last Modified:2020-02-26 03:15:34
# -----

import os
import db
import time

def getpath(path):
    '''
    description: 获取文件名并写入数据库
    param {str} 路径
    return: none
    '''

    dirs = os.listdir(path)
    
    for x in dirs:
        name = x.split("]")[0].split("[")[1]
        movieInfo = {
            "fileName": name,
            "movieName": "",
            "chineseName": "",
            "duration": "",
            "tags": "",
            "releaseYear": "",
            "releaseTime": "",
            "createTime": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(os.path.getctime(path + x))),
            "poster": "",
            "directors": "",
            "scripts": "",
            "regions": "",
            "publish": "",
            "actors": "",
            "doneSign": "",
            "watchTime": ""
        }
        db.dbinsert(movieInfo)
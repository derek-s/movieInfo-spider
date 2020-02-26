# !/usr/bin/python
# -*- coding: utf-8 -*-
# File:db.py
# File Created:2020-02-24 10:00:05
# Author:Derek.S(derekseli@outlook.com)
# -----
# Last Modified:2020-02-24 10:00:05
# -----

import pymongo

def dblink():
    '''
    description: 数据库连接
    param: none
    return: 
    '''

    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['Info']
    db.authenticate("dbuser", "***123pwd321***")

    collection = db["Info"]

    return collection


def dbinsert(data):
    '''
    description: 数据库插入
    param: 键值对数据
    return: inserted_id
    '''

    collection = dblink()

    dbx = collection.insert_one(data)

    return dbx.inserted_id


def dbupdate(query, data):
    '''
    description: 数据库更新
    param: 查询条件 键值对数据
    return: upserted_id
    '''

    collection = dblink()

    dbx = collection.update_one(query, data)

    return dbx.modified_count

def dbquery(query):
    '''
    description: 数据库查询
    param: 查询条件
    return: collection
    '''

    collection = dblink()

    return collection.find(query, no_cursor_timeout=True)

def dbcount(query):
    '''
    description: 数据库查询计数
    param: 查询条件
    return: 查询到的总数
    '''
    collection = dblink()
    return collection.count_documents(query)
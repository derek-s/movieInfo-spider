# !/usr/bin/python
# -*- coding: utf-8 -*-
# File:main.py
# File Created:2020-02-26 10:32:24
# Author:Derek.S(derekseli@outlook.com)
# -----
# Last Modified:2020-02-26 10:32:24
# -----

import spider
import getpath
import db
import time

if __name__ == "__main__":
    
    # spider.spider("黑水 Dark Waters 2019")
    # getpath("")
    query = db.dbquery({"movieName": ""}).batch_size(10)

    for x in query:

        fileName = x["fileName"]
        movieInfo = spider.spider(fileName)
        update = {
            "$set": movieInfo
        }
        db.dbupdate({"fileName": fileName}, update)

        time.sleep(15)

    query.close()
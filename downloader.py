# !/usr/bin/python
# -*- coding: utf-8 -*-
# File:downloader.py
# File Created:2020-02-26 11:47:53
# Author:Derek.S(derekseli@outlook.com)
# -----
# Last Modified:2020-02-26 11:47:53
# -----

import requests
import time

def download(url):
    '''
    description: 下载函数
    param {str} url
    return: status
    '''

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    # 增加重试次数
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False
    r = s.get(url, headers=headers, stream=True)
    if(r.status_code == 200):
        fileName = url.split("/")[-1]
        with open("cover/" + fileName, "wb") as pic:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pic.write(chunk)
        print("cover download complete")
        # time.sleep(1)
    return
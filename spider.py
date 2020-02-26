# !/usr/bin/python
# -*- coding: utf-8 -*-
# File:spider.py
# File Created:2020-02-26 10:32:54
# Author:Derek.S(derekseli@outlook.com)
# -----
# Last Modified:2020-02-26 10:32:54
# -----

from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from urllib.parse import quote

import downloader
import db

def spider(name):
    '''
    description: 爬虫函数
    param {str} name
    return: none
    '''

    # 浏览器
    chromeOptions = Options()
    # chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome("driver/chromedriver.exe")

    # 打开搜索页面
    driver.get("http://search.mtime.com/search/?q=" + quote(name))

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "bottom")))
    # 获取搜索结果
    searchHTML = driver.find_element_by_xpath(r'//*[@id="moreRegion"]').get_attribute('innerHTML')
    
    flags = []

    soup = BeautifulSoup(searchHTML, "html.parser")
    for eachLink in soup.select("h3 > a.__r_c_"):
        flag = []
        for eachName in name.split(" "):
            if(eachName in eachLink.get_text()):
                flag.append(True)
            else:
                flag.append(False)
        flag.append(eachLink["href"])
        flags.append(flag)
    if(len(flags) != 1):
        trueCount = []
        for eachFlag in flags:
            # lenFlag = len(eachFlag)
            # if(eachFlag.count(True) + 1 == lenFlag):
            #     nWindow = "window.open('" + eachFlag[-1] + "')"
            #     driver.execute_script(nWindow)
            # else:
            #     trueCount.append([eachFlag.count(True), eachFlag[-1]])
            trueCount.append([eachFlag.count(True), eachFlag[-1]])
        url = max(trueCount)[1]
        nWindow = "window.open('" + url + "')"
        driver.execute_script(nWindow)
        
    else:
        nWindow = "window.open('" + flags[0][-1] + "')"
        driver.execute_script(nWindow)


    handles = driver.window_handles
    driver.switch_to.window(handles[1])

    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, "bottom")))
    htmlText = driver.page_source
    
    # bs4处理
    soup = BeautifulSoup(htmlText, "html.parser")

    # poster
    posterUrl = soup.select_one("div.db_cover > a > img")["src"]
    posterFilename = posterUrl.split("/")[-1]
    downloader.download(posterUrl)

    # 标题
    finder = soup.select_one("div#db_head")
    # 中文译名
    chineseName = finder.select_one("h1").get_text()
    # 英文名称
    movieName = finder.select_one("p.db_enname").get_text()
    # 上映年份
    releaseYear = finder.select_one("p.db_year").get_text().split("(")[1].split(")")[0]

    # print(chineseName, movieName, releaseYear)

    # 时长
    finder = soup.select_one("div.otherbox")
    try:
        duration = finder.select_one("span").get_text()
        # print(duration)
    except Exception as e:
        print("时长获取失败 " + str(e))
        duration = "N/A"

    # 分类标签
    try:
        tags = ""
        otherBoxElements =  finder.select("a")
        lenOtherBoxElements = len(otherBoxElements)
        for i in range(lenOtherBoxElements-1):
            if(lenOtherBoxElements != 1):
                tags += otherBoxElements[i].get_text()
                if(i != lenOtherBoxElements-2):
                    tags += "/"
            else:
                tags = otherBoxElements[i].get_text()
        # print(tags)
    except Exception as e:
        print("分类标签获取失败 " + str(e))
        tags = "N/A"

    # 上映时间
    try:
        
        otherBoxElements =  finder.select("a")
        releaseTime = otherBoxElements[-1].get_text()
    except Exception as e:
        print("上映时间获取失败 " + str(e))
        releaseTime = "N/A"


    # 导演
    try:
        directors = ""
        finder = soup.find_all(text=["导演："])
        directorList = finder[0].find_parents(limit=1)[0].find_next_siblings()
        lenDirector = len(directorList)
        if(lenDirector == 1):
            directors = directorList[0].get_text()
        for i in range(lenDirector-1):
            if(lenDirector != 1):
                directors += directorList[i].get_text()
                if(i != lenDirector-2):
                    directors += "/"
            else:
                directors = directorList[i].get_text()
        # print(directors)
    except Exception as e:
        print("导演获取失败 " + str(e))
        directors = "N/A"
    
    # 编剧
    try:
        scripts = ""
        finder = soup.find_all(text = ["编剧："])
        scriptList = finder[0].find_parents(limit=1)[0].find_next_siblings()
        lenScript = len(scriptList)
        if(lenScript == 1):
            scripts = scriptList[0].get_text()
        for i in range(lenScript-1):
            if(lenScript != 1):
                scripts += scriptList[i].get_text()
                if(i != lenScript-2):
                    scripts += "/"
            else:
                scripts = scriptList[i].get_text()
        # print(scripts)
    except Exception as e:
        print("编剧获取失败 " + str(e))
        scripts = "N/A"

    # 国家地区
    try:
        regions = ""
        finder = soup.find_all(text = ["国家地区："])
        regionsList = finder[0].find_parents(limit=1)[0].find_next_siblings()
        
        regions = regionsList[0].get_text()
        
        # print(regions)
    except Exception as e:
        print("国家地区获取失败 " + str(e))
        regions = "N/A"

    # 发行公司
    try:
        publish = ""
        finder = soup.find_all(text = ["发行公司："])
        publishList = finder[0].find_parents(limit=1)[0].find_next_siblings()
        lenPublish = len(publishList)
        if(lenPublish == 1):
            publish = publishList[0].get_text()
        for i in range(lenPublish-1):
            if(lenPublish != 1):
                publish += publishList[i].get_text()
                if(i != lenPublish-2):
                    publish += "/"
            else:
                publish = publishList[i].get_text()
        # print(publish)
    except Exception as e:
        print("发行公司获取失败 " + str(e))
        publish = "N/A"


    # 演员
    try:
        actors = []
        finder = soup.select("dl.main_actor")
        for x in finder:
            actor = ""
            actorsList = x.select("dd > p")
            for y in actorsList:
                actor += y.get_text()
            actors.append(str(actor).replace("\n", "").replace("饰\xa0", " 饰 "))
        # print(actors)
    except Exception as e:
        print("演员获取失败 " + str(e))
        actors = []


    movieInfo = {
        "fileName": name,
        "movieName": movieName,
        "chineseName": chineseName,
        "duration": duration,
        "tags": tags,
        "releaseYear": releaseYear,
        "releaseTime": releaseTime,
        "poster": posterFilename,
        "directors": directors,
        "scripts": scripts,
        "regions": regions,
        "publish": publish,
        "actors": actors
    }
    print(movieInfo)

    driver.quit()

    return movieInfo
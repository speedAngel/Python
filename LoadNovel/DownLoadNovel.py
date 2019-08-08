# -*- coding: utf-8 -*-
import  os
import bs4
from bs4 import BeautifulSoup
import sys
import json
import requests
import importlib
importlib.reload(sys)

global url
global headers
global savePath

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
url='http://www.xbiquge.la/0/10/'
savePath = "E:\mm"

#创建文件夹
def CreateDir(dirPath):
    if os.path.exists(dirPath) is False:
        os.makedirs(dirPath)
    os.chdir(dirPath)

def download_content(filePath,page):
    print('开始下载' + page)
    file = open(filePath,'a+', encoding='utf8')
    c_url = url+ page
    res = requests.get(c_url, headers=headers)
    soup = BeautifulSoup(res.text.encode(res.encoding).decode(res.apparent_encoding), 'html.parser')
    contents = soup.find_all('div', id="content")
    novel = contents[0].text.replace(' ', '\n').replace('\xa0' * 8, '\n')
    # print(novel)
    try:
        file.writelines(novel)
    except Exception as e:
        pass
    file.close()

def main():
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text.encode(res.encoding).decode(res.apparent_encoding), 'html.parser')
    name =soup.find_all('div', id ="info")[0].find('h1').text
    rootPath = savePath +'\\' + name
    CreateDir(rootPath)
    list_a = soup.find_all('div', class_="box_con")[-1].find_all('a')
    i = 0
    for a in list_a:
        i = i + 1
        href = a.attrs['href']
        array = href.split('/')
        file_name = array[len(array) - 1] #章节目录名称
        content = a.text
        # print(href)
        print(content)
        title = content.split(' ')[-1].replace('?','')
        num = str(i)
        titleName= num.zfill(4) + title
        filePath = rootPath+'\\'+titleName+'.txt'
        if os.path.exists(filePath) is True:
            continue
        try:
            download_content(filePath,file_name)
        except Exception as e:
            pass


if __name__ == '__main__':
    main()
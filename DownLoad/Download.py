import  os
import bs4
from bs4 import BeautifulSoup
import sys
import json
import requests
import importlib
importlib.reload(sys)

global headers
global url
global savepath
global datafile

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
url = 'https://www.mzitu.com/hot/'
savepath = "E:\mm"

datafile ="E:\mm\data.json"

dict = {}

#创建文件夹
def CreateDir(dirPath):
    if os.path.exists(dirPath) is False:
        os.makedirs(dirPath)
    os.chdir(dirPath)

def download_page(page,type):
    # print(page)
    res_page = requests.get(page, headers=headers)
    # 使用BeautifulSoup将请求到的html资源文本转化为soup
    page_soup = BeautifulSoup(res_page.text, 'html.parser')
    #print(page_soup)
    page_a = page_soup.find('div',class_='postlist').find_all('a',target='_blank')
    for a in page_a:
        # print(a)
        try:
            content = a.find('img').attrs['alt']
            content = content.replace(':','_').replace(',','_')
            print(content)

            path = savepath+"\\"+type+"\\"+ content
            if os.path.exists(path) is True:
                continue
            CreateDir(path)
            href = a.attrs['href']
            print(href)
            download_img(href, path)
        except Exception as e:
            pass



def download_img(href, path, headers=headers):
    img_page = requests.get(href, headers = headers)
    # 使用BeautifulSoup将请求到的html资源文本转化为soup
    img_soup = BeautifulSoup(img_page.text, 'html.parser')
    # print(page_soup)
    count = img_soup.find('div',class_='pagenavi').find_all('a')[-2].find('span').text
    print("图片总数：" + count)

    for i in range(int(count)):
        if i == 0:
            tmpUrl = href
        else:
            tmpUrl = href + '/' + str(i+1)
        tmp_page = requests.get(tmpUrl, headers=headers)
        tmp_soup = BeautifulSoup(tmp_page.text, 'html.parser')
        imgs = tmp_soup.find('div', class_='main-image').find_all('img')
        for img in imgs:
            # print(img)
            try:
                src = img.attrs['src']
                print(src)
                array = src.split('/')
                file_name = array[len(array) - 1]
                # print(file_name)
                # 防盗链加入Referer
                head = {'Referer': href,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
                imgfile = requests.get(src, headers=head)
                # print('开始保存图片')
                file_name = path+'\\' + file_name
                f = open(file_name, 'ab')
                if os._exists(file_name):
                    continue
                f.write(imgfile.content)
                #print(file_name, '图片保存成功！')
                f.close()
            except Exception as e:
                pass


def main():
    CreateDir(savepath)
    res = requests.get(url, headers=headers)
    #使用BeautifulSoup将请求到的html资源文本转化为soup
    soup = BeautifulSoup(res.text,'html.parser')
    #print(soup)
    maxPage = soup.find('div',class_ ='nav-links').find_all('a')[3].text
    print(maxPage)

    for i in range(int(maxPage),0,-1):
        #print(i)
        if i == 1:
            page = url
        else:
            page = url + 'page/' + str(i)
        print(page)
        typel= page.split('/')[3]
        #print(arrays[3])
        #dict[typel] = i
        download_page(page,typel)

if __name__ == '__main__':
    main()




import os
from requests.adapters import HTTPAdapter
import random
from logging import Logger
# from modulefinder import LOAD_CONST
from turtle import title
import urllib.request as req
from xml.dom.minidom import Identified
import requests #pip3 install requests
from bs4 import BeautifulSoup #pip3 install beautifulsoup4
import sys
import re
import string
import urllib.request
import urllib
import urllib3
import shutil
# id=["2231",2]
import time
ticks = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#from retrying import retry
#from retry import retry


id = 1
idend = 3638  # 最後一本的id


# 取得目前程式碼的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))

# 設定資料夾名稱和檔案名稱
folder_name = "novel"
file_name = "idend.txt"

# 要建立的資料夾的完整路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
folder_name = "novel"
file_name = "idend.txt"
folder_path = os.path.join(current_dir, folder_name)

# 確認 novel 資料夾是否存在，若不存在則建立
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 要建立的檔案的完整路徑
file_path = os.path.join(folder_path, file_name)

# 打開檔案進行操作
with open(file_path, 'a') as end:
    end.write("\n")
    end.write("endid:")
    end.write(str(idend))



base_folder = folder_path = os.path.join(current_dir, folder_name)  # 指定基础文件夹路径

# 要创建的子文件夹列表
subfolders = ['end', 'serialize']

# 循环检查和创建每个子文件夹
for subfolder in subfolders:
    folder_path = os.path.join(base_folder, subfolder)  # 构建子文件夹的完整路径
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"文件夹 '{folder_path}' 已创建")
    else:
        print(f"文件夹 '{folder_path}' 已存在")



# @retry(stop_max_attempt_number=8, wait_random_min=3, wait_random_max=10)

while id <= idend:

    # url="https://www.wenku8.net/modules/article/articleinfo.php?id=1"
    url = ("https://www.wenku8.net/modules/article/articleinfo.php?id="+str(id))
    txt_url = ("http://dl.wenku8.com/down.php?type=txt&id="+str(id))
    # txt_url=("http://dl.wenku8.com/txtgbk/2/"+id[0]+".txt")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"}

    time.sleep(2)

    http = urllib3.PoolManager()
    request = http.request('GET', url, headers=headers, retries=3)
    wenku8 = request.data.decode('gb18030')
#    print(wenku8)

#    requests.adapters.DEFAULT_RETRIES = 3
#    request = urllib.request.Request(url, headers={
#                                     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"})
#    with urllib.request.urlopen(request) as response:
#        wenku8 = response.read().decode("gb18030")

    soup = BeautifulSoup(wenku8, "html.parser")
    # print(soup.prettify())
    #result = soup.find("table")
    # print(result)
    classerror = soup.find("title")
    bookerror = (classerror.text)
    if bookerror == "出现错误":
        print(bookerror)
        print(id)
        print("\n")
        with open(file_path, 'a') as error:
            error.write("\n")
            error.write(str(id))
        id = id + 1
        continue
    classmain = soup.find_all("div", class_="main")
    # print(classmain[4])
    classtable = classmain[4].find("table")  # 抓取第五個main裡的table
    classtr = classtable.find_all("tr")  # 抓取table裡的全部tr

    # 獲取書名
    classtd1 = classtr[0].find_all("td")
    booknamebefore = (classtd1[1].text)
    # print(booknamebefore)
    booksymbolParentheses = "["
    bookname1 = booknamebefore.rsplit("[",1)
    #print(bookname1[0])
    bookname=re.sub("\[","［",bookname1[0])
    bookname=re.sub("\]","］",bookname)
    bookname=re.sub("\:|\*|\?|\/","",bookname)
    print(bookname)
  

    # 獲取作者
    classtd2 = classtr[2].find_all("td")  # 抓取第二個tr裡的全部td
    # print(classtd)
    authorbefore = (classtd2[1].text)
    statusbefore = (classtd2[2].text)
    # print(type(author))
    #print(authorbefore)
    # print(statusbefore)
    author1 = authorbefore[5:]
    author=re.sub("\[","［",author1)
    author=re.sub("\]","］",author)
    author=re.sub("\:|\*|\?|\/","",author)

    status = statusbefore[5:]
    print(author)
    print(status)
    print(id)
    print("\n")

    if status == "已完结":
        #downtxt = requests.get(txt_url,allow_redirects=True)
        # with open("./novel/end/"+str(bookname)+".txt",'wb') as f:
        # f.write(downtxt.content)
        #req = urllib.request.Request(txt_url, headers=headers)
        # with urllib.request.urlopen(req) as response:
        http = urllib3.PoolManager()
        with http.request('GET', txt_url, headers=headers, preload_content=False, retries=3) as r:
            #response = request.data.decode('gb18030')
            # print(response)
            file_path = os.path.join(base_folder, 'end', f"{bookname}@{author}.txt")
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(r, out_file)
                print(f"文件 '{file_path}' 已创建")     
        # print("1")
    elif status == "连载中":
        #downtxt = requests.get(txt_url,allow_redirects=True)
        # with open("./novel/serialize/"+str(bookname)+".txt",'wb') as f:
        #    f.write(downtxt.content)
        #req = urllib.request.Request(txt_url, headers=headers)
        # with urllib.request.urlopen(req) as response:
        #response =response.read().decode('gbk')
        http = urllib3.PoolManager()
        with http.request('GET', txt_url, headers=headers, preload_content=False, retries=3) as r:
            file_path = os.path.join(base_folder, 'serialize', f"{bookname}@{author}.txt")
            with open(file_path, 'wb') as out_file:
                shutil.copyfileobj(r, out_file)
                print(f"文件 '{file_path}' 已创建")
        # print("2")
    else:
        print("error1")

    id = id+1


# 打開檔案進行操作
with open(file_path, 'a') as end:
    end.write("endtime:")
    end.write(str(ticks))

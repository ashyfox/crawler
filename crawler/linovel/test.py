from requests.adapters import HTTPAdapter
import random
from logging import Logger
from modulefinder import LOAD_CONST
from turtle import title
import urllib.request as req
from xml.dom.minidom import Identified
import requests
from bs4 import BeautifulSoup
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
# from retrying import retry
# from retry import retry


id = 2013
idend = 2013  # 最後一本的id
chapterid = 14678
temp_urls = []
volume=[]
p_list = []
content_book=""
symbolor = "|"
symbolspace = " "
end = open("./novel/idend.txt", 'a')
end.write("\n")
end.write("endid:")
end.write(str(idend))
end.close

while id <=idend:
    book_url = ("https://w.linovelib.com/novel/" + str(id) +".html")
    #book_url=("https://w.linovelib.com/novel/1.html")
    #content_url = ("https://www.linovelib.com/novel/" +str(id)+"/"+str(chapterid)+".html")
    catalog_url = ("https://w.linovelib.com/novel/"+str(id)+"/catalog")

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.101 Mobile Safari/537.36"}



    time.sleep(2)

    http = urllib3.PoolManager()
    request = http.request('GET', book_url, headers=headers, retries=3)
    linovelib = request.data
    soup = BeautifulSoup(linovelib, "html.parser")

    classerror = soup.find("head")
    classerror = classerror.find("title").text
    bookerror = (classerror)
    if bookerror == "错误_哔哩轻小说":
        print(bookerror)
        print(id)
        print("\n")
        error = open("./novel/errorid.txt", 'a')
        error.write("\n")
        error.write(str(id))
        error.close
        id = id+1
        continue
    class_bookname=soup.find("h2",class_="book-title")
    booknamebefore = (class_bookname.text)
    bookname=re.sub("\:|\*|\?|\/","",booknamebefore)
    print(bookname)

    class_author=soup.find("div",class_="book-rand-a")
    authornamebefore=(class_author.text)
    authornamebefore=authornamebefore[1:-3]
    author=re.sub("\:|\*|\?|\/","",authornamebefore)
    print(author)

    class_status=soup.find_all("p",class_="book-meta")
    status=(class_status[1].text)
    status = status.rsplit("|",1)
    status=status[1]
    print(status)

    class_tag=soup.find_all("p",class_="book-meta")
    class_librarychina=soup.find("em",class_="tag-small gray").text
    class_comic=soup.find("em",class_="tag-small orange").text




    http = urllib3.PoolManager()
    request = http.request('GET', catalog_url, headers=headers, retries=3)
    linovelib_content = request.data
    soup = BeautifulSoup(linovelib_content, "html.parser")
    #class_volumename= soup.find_all("li", class_="chapter-bar chapter-li")
    class_chapter = soup.find_all("li", class_="chapter-li jsChapter")
    for node in class_chapter:  # 找到<class_clisturl>中的<li>
        temp_urls.append(node.a['href'])# 在每一行<class_clisturl>中的<li>找到<a>，存儲到一個list中
    print(temp_urls)
    #content_book=[]
    #content_book.append(bookname)
    content_book='{}'.format(bookname)
    for x in range(len(temp_urls)):
    #for x in range(0,3,1):
        time.sleep(1)
        http = urllib3.PoolManager()
        #request = http.request('GET',"https://w.linovelib.com/"+ str(x) , headers=headers, retries=3)
        request = http.request('GET',"https://w.linovelib.com"+ temp_urls[int(x)] , headers=headers, retries=3)
        print("https://w.linovelib.com"+ temp_urls[int(x)] )
        #print("https://w.linovelib.com"+ temp_urls[int(x)])
        linovelib_content = request.data
        soup = BeautifulSoup(linovelib_content, "html.parser")

        

        class_chaptername=soup.find("div",class_="atitle")
        volume=class_chaptername.find("h3").text
        chapter=class_chaptername.find("h1",id="atitle").text

        booktitle= ("\n") + volume + (" ") + chapter
        #print(booktitle)

        class_content=soup.find("div", id="acontent") 
        p_list=[]
        #for p in class_content.find_all("p"):
        p_list.append(booktitle)
        p_list.append(class_content.text)
        content = '\n'.join(p_list) 
        #content=booktitle + ("\n")+ (content)
        #print(content)
        content_book='{}\n{}'.format(content_book, content)
        

    #content_book='{}\n{}'.format(bookname, content)
    #content_book.append(bookname)
    #content_book =content_book.append(content)
    print(content_book)
        

    if class_librarychina == "华文轻小说":
        if status == "完结":
            with open( "./novel/china/end/"+bookname +"@" + author +".txt", 'w',encoding='UTF-8') as out_file:
                out_file.write(content_book)
                out_file.close()
        elif status == "连载":
            with open( "./novel/china/serialize/"+bookname +"@" + author +".txt", 'w',encoding='UTF-8') as out_file:
                out_file.write(content_book)
                out_file.close()
        else:
            print("error1")    
    else:
        if class_comic == "轻改漫画":
            with open( "./novel/comic/id.txt", 'a',encoding='UTF-8') as out_file:
                out_file.write("\n")
                out_file.write(str(id))
                out_file.close()                
        else:    
            if status == "完结":
                with open( "./novel/end/"+bookname +"@" + author +".txt", 'w',encoding='UTF-8') as out_file:
                    out_file.write(content_book)
                    out_file.close()
                print("1")
            elif status == "连载":
                with open( "./novel/serialize/"+bookname +"@" + author +".txt", 'w',encoding='UTF-8') as out_file:
                    out_file.write(content_book)
                    out_file.close()
                print("2")
            else:
                print("error1")

    id = id+1

end = open("./novel/idend.txt", 'a')
end.write("endtime:")
end.write(str(ticks))
end.close
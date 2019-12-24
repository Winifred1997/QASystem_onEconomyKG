import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import bs4
import json
import random

def getHTML(url,driver):
    try:
        driver.get(url)
        return driver.page_source
    except:
        print("a error happen when getting url")
        return ""

def getLinkCode(html,link,code):
    soup = BeautifulSoup(html,'html.parser')
    for tr in soup.find(name='tbody').children:
        if isinstance(tr,bs4.element.Tag):
            tds=tr('td')
            link.append(tds[1].find('a').get('href'))
            code.append(tds[1].string)

def main():
    #origin='http://q.10jqka.com.cn/usa/detailDefer/board/all/field/stockcode/order/asc/page/';
    #origin='http://q.10jqka.com.cn/hk/detailYs/board/all/field/stockname/order/asc/page/'
    origin='http://q.10jqka.com.cn/eu/detail/board/uk/field/stockcode/order/asc/page/'
    link=[]
    code=[]
    for i in range(1,95):
        driver = webdriver.Chrome(r"C:\Users\Junji\Downloads\chromedriver_win32\chromedriver.exe")
        url=origin+str(i)+'/ajax/1'
        print(url)
        html = getHTML(url,driver)
        driver.close()
        getLinkCode(html,link,code)
    dic = dict(zip(code,link))
    with open('USStockUK.txt','w') as a:
        json.dump(dic,a)

main()
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import bs4
import json
import random
import csv

#1.循环获取html页面，包括company 和 manager
#2.对company进行解析，并且添加（id，名称，代码，状态，标签）到company表格当中
#3.对manager进行解析，并且添加（id，名称，性别，年龄，公司股票代码，职位，标签）到manager表格当中，（添加的时候需要判断董事和高管是否有重复）
#4.通过manager和company的id，进行创建executive_stock，和director_stock

#初始化所有csv表格的表头
def initalFile():
    with open("HKStock.csv",'w',newline="",encoding='utf-8') as f:
        csv_write = csv.writer(f)
        data_row = ["index:ID", "name", "code", "status", ":LABEL"]
        csv_write.writerow(data_row)
    with open("HKHuman.csv",'w',newline="",encoding='utf-8') as f:
        csv_write = csv.writer(f)
        data_row = ["index:ID", "name", "gender","age","code", "job", ":LABEL"]
        csv_write.writerow(data_row)
    with open("HKExecutive_Stock.csv",'w',newline="",encoding='utf-8') as f:
        csv_write = csv.writer(f)
        data_row = [":START_ID", ":END_ID", "relation", ":TYPE"]
        csv_write.writerow(data_row)


#获取html页面
def getHTML(driver,url):
    try:
        driver.get(url)
        return driver.page_source
    except:
        print("some thing wrong in getting html of "+url)


#解析股票的页面并且将相应股票的ID，名称，代码，状态，和标签写入股票的csv文件
def parseStockAndStore(stock,ID,code):
    soup = BeautifulSoup(stock,'html.parser')
    basic = soup.find(name='div',attrs={'stat':'company_basic'})
    if isinstance(basic,bs4.element.Tag):
        tds = basic.find_all(name='td')
        name = tds[0].contents[3].string.replace('\t','').strip()
        with open("HKStock.csv",'a+',newline="",encoding='utf-8') as f:
            f_write = csv.writer(f)
            data_row=[ID,name,code,"normal","entrepreneur"]
            f_write.writerow(data_row)


#解析个人页面，并且将相应人的ID，姓名，性别，年龄，所在公司代码，工作，和标签写入人的csv文件
#于此同时，将个人ID，公司ID，关系，类型写入两个关系csv文件
#director==董事, manager==高管
def parseHumanAndStore(human,StockID,code,id):
    soup = BeautifulSoup(human,'html.parser')
    tables = soup.find_all(name='table',attrs={'class':'m_table ggintro pr'})
    for table in tables:
        tds = table.find_all(name='td')
        name = tds[0].string
        job = tds[1].string
        age = tds[3].string.split(' ')[1]
        gender = tds[3].string.split(' ')[0]
        with open("HKHuman.csv", 'a', newline="",encoding='utf-8') as f:
            csv_write = csv.writer(f)
            data_row = [id, name, gender, age, code, job, 'executive']
            csv_write.writerow(data_row)
        with open("HKExecutive_stock.csv", 'a', newline="", encoding='utf-8') as f:
            csv_write = csv.writer(f)
            data_row = [id, StockID, job, "executive"]
            csv_write.writerow(data_row)
        id=id+1
    return id

def main():
    #initalFile()
    linkdata = json.load(open("HKStockTest.txt"))
    UKStockID=602085
    UKHumanID=7000029951
    for item in linkdata:
        driver = webdriver.Chrome(r"C:\Users\Junji\Downloads\chromedriver_win32\chromedriver.exe")
        try:
            stock=linkdata[item]+'company'
            human=linkdata[item]+'manager'
            print(stock+'  '+human)

            stock=getHTML(driver,stock)
            parseStockAndStore(stock,UKStockID,item)

            human=getHTML(driver,human)
            UKHumanID = parseHumanAndStore(human,UKStockID,item,UKHumanID)
            driver.close()
            UKStockID=UKStockID+1
        except:
            driver.close()
            continue
main()
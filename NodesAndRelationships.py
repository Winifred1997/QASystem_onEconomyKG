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
    with open("USStock.csv",'w',newline="",encoding='utf-8') as f:
        csv_write = csv.writer(f)
        data_row = ["index:ID", "name", "code", "status", ":LABEL"]
        csv_write.writerow(data_row)
    with open("USHuman.csv",'w',newline="",encoding='utf-8') as f:
        csv_write = csv.writer(f)
        data_row = ["index:ID", "name", "gender","age","code", "job", ":LABEL"]
        csv_write.writerow(data_row)
    with open("USExecutive_Stock.csv",'w',newline="",encoding='utf-8') as f:
        csv_write = csv.writer(f)
        data_row = [":START_ID", ":END_ID", "relation", ":TYPE"]
        csv_write.writerow(data_row)
    with open("USDirector_Stock.csv",'w',newline="",encoding='utf-8') as f:
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
    tbody = soup.find(name='tbody')
    if isinstance(tbody,bs4.element.Tag):
        tds = tbody.find_all(name='td')
        name = tds[3].contents[1]
        with open("USStock.csv",'a+',newline="",encoding='utf-8') as f:
            f_write = csv.writer(f)
            data_row=[ID,name,code,"normal","entrepreneur"]
            f_write.writerow(data_row)


#解析个人页面，并且将相应人的ID，姓名，性别，年龄，所在公司代码，工作，和标签写入人的csv文件
#于此同时，将个人ID，公司ID，关系，类型写入两个关系csv文件
#director==董事, manager==高管
def parseHumanAndStore(human,StockID,HumanIDs,code):
    soup = BeautifulSoup(human,'html.parser')
    #parse the director
    director = soup.find(name='div',attrs={'stat':'director_produce'})
    writeFile(director,'director',"USDirector_Stock.csv",StockID,HumanIDs,code)

    #parse the executive
    executive = soup.find(name='div',attrs={'stat':'manager_produce'})
    writeFile(executive,'executive',"USExecutive_Stock.csv",StockID,HumanIDs,code)

def writeFile(manager, label, file,StockID, HumanIDs,code):
    if isinstance(manager,bs4.element.Tag):
        trs=manager.find_all(name='tr')
        for i in range(1,len(trs)):
            tds = trs[i].find_all(name='td')
            job = tds[2].string
            a = tds[0].find(name='a')
            id = a.attrs.get("manager-id")
            id = id[2:len(id)]
            if id not in HumanIDs:
                HumanIDs.append(id)
                name = tds[0].string
                gender='male'
                if tds[1].string =="女":
                    gender='female'
                elif tds[1].string =="男":
                    gender='male'
                else:
                    gender='unKnown'
                age = tds[3].string
                if age=="--":
                    age='unKnown'
                with open("USHuman.csv", 'a', newline="",encoding='utf-8') as f:
                    csv_write = csv.writer(f)
                    data_row = [id, name, gender, age, code, job, label]
                    csv_write.writerow(data_row)
            with open(file, 'a', newline="",encoding='utf-8') as f:
                csv_write = csv.writer(f)
                data_row = [id,StockID,job,label]
                csv_write.writerow(data_row)

def main():
    #initalFile()
    linkdata = json.load(open("USStock.txt"))
    USStockID=500001
    HumanIDS=[]
    for item in linkdata:
        driver = webdriver.Chrome(r"C:\Users\Junji\Downloads\chromedriver_win32\chromedriver.exe")
        try:
            stock=linkdata[item]+'company'
            human=linkdata[item]+'manager'
            print(stock+'  '+human)

            stock=getHTML(driver,stock)
            parseStockAndStore(stock,USStockID,item)

            human=getHTML(driver,human)
            parseHumanAndStore(human,USStockID,HumanIDS,item)

            driver.close()
            USStockID=USStockID+1
        except:
            driver.close()
            continue

main()
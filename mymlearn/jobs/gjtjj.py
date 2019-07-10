# coding:utf8
import numpy as np
import pandas as pd
import datetime,time
import requests,json
from sqlalchemy import create_engine
from utils.mymysql import MyMySQL
from . import crawl_parent


class GjtjjClass(crawl_parent.CrawlParent):
    '''
    国家统计局-月季年行业指数、行业预警指数
    '''
    url = "http://www.shclearing.com/shchapp/web/valuationclient/findvaluationdata"
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://spider:SzPj24^365wx@39.97.184.89:3306/spider?charset=utf8',encoding='utf8')
        self.start_date = [2016,2,4]
        self.count = 0 # API计数 每周限额50W个单元格
        self.max = None
        self.table = "zqgz_spider"
        self.headers =  {
            'User-Agent':self.UA,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://www.shclearing.com/cpgz/zqjqysp/zqgz/'
        }

    def __enter__(self):
        return self

    def getNextDay(self):
        if self.start_date[1]==12:
            y = self.start_date[0]
            self.start_date = [self.start_date[0]+1,1,4]
            return str(y+1)+ '-01-03'
        else:
            m = self.start_date[1]
            self.start_date = [self.start_date[0],m+1,4]
            return str(self.start_date[0]) +"-{}".format(str(m+1).zfill(2)) +'-03'

    def run(self):
        while True:
            from_date = str(self.start_date[0])+'-{}'.format(str(self.start_date[1]).zfill(2))+'-04'
            end_date = self.getNextDay()
            print(end_date)
            if (datetime.datetime.today() - datetime.datetime(*map(int,end_date.split('-')))).days<=0:
                print(end_date)
                break
            self.page = 0
            self.max = None
            data = self.getOnePage(from_date,end_date)
            print(data["data"]["datas"])
            df = pd.DataFrame(data["data"]["datas"]).drop(["attach"],axis=1)
            df.to_sql(self.table,self.engine,index=False)
            with MyMySQL() as m:
                m.execute_sql("create table if not exists com_{0} like {0}".format(self.table))
                m.execute_sql("insert into com_{0} select * from {0}".format(self.table))
                m.execute_sql("drop table {0}".format(self.table))
            while self.page<=self.max:
                try:
                    data = self.getOnePage(from_date,end_date)
                except:
                    with open("error.log","a") as fp:
                        print(f"{from_date},{end_date},page:{self.page-1}")
                        fp.write(f"{from_date},{end_date},page:{self.page-1}\r\n")
                else:
                    df = pd.DataFrame(data["data"]["datas"]).drop(["attach"], axis=1)
                    df.to_sql(self.table, self.engine, index=False)
                    with MyMySQL() as m:
                        m.execute_sql("create table if not exists com_{0} like {0}".format(self.table))
                        m.execute_sql("insert into com_{0} select * from {0}".format(self.table))
                        m.execute_sql("drop table {0}".format(self.table))
            time.sleep(1)


    def getOnePage(self,start_date,end_date):
        print(f"正在请求第{self.page}/{None if not self.max else self.max}页")
        postdata = {
            'startTime': start_date,
            'endTime': end_date,
            'bondNames': '',
            'bondCodes': '',
            'bondTypes': '402880e5438a816001438a8273c20003',
            'limit': 50,
            'start': 50 * self.page,
            'sortFlag': 1,
            'sortNameFlag': 1,
            'sortDateFlag': 1
        }
        self.page +=1
        resp =  requests.post(self.__class__.url,headers = self.headers,data=postdata)
        resp.encoding = 'utf8'
        if not self.max:
            self.max = int(int(resp.json().get("totalProperty"))/50)
            print(f"一共{self.max}页")
        return resp.json()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__=="__main__":
    with GjtjjClass() as wp:
        wp.run()
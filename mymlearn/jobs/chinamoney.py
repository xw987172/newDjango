# coding:utf8
import numpy as np
import pandas as pd
import datetime,time
import requests,json
from sqlalchemy import create_engine
from utils.mymysql import MyMySQL
from . import crawl_parent


class ChinaMoneyClass(crawl_parent.CrawlParent):
    '''
    上海清算所-债券估值数据
    270101 中期票据
    260101 短期融资券
    '''
    url = f"http://www.chinamoney.com.cn/ags/ms/cm-u-bk-currency/BmarkBnd?referenceName={0}&appCycName={1}&flag=&t={2}"
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://spider:SzPj24^365wx@39.97.184.89:3306/spider?charset=utf8',encoding='utf8')
        self.count = 0 # API计数 每周限额50W个单元格
        self.max = None
        self.table = "chinamoney_spider"
        self.headers =  {
            'User-Agent':self.UA,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        }

    def __enter__(self):
        return self

    def run(self,type,period):
        data = self.getOnePage2(type,period)
        print(data)
        df = pd.DataFrame(data["records"])
        df["referenceName"] = data["data"]["referenceName"]
        df["period"] = data["data"]["appCycName"]
        df["cate"] = type
        df.to_sql(self.table,self.engine,index=False)
        with MyMySQL() as m:
            m.execute_sql("create table if not exists com_{0} like {0}".format(self.table))
            m.execute_sql("insert into com_{0} select * from {0}".format(self.table))
            m.execute_sql("drop table {0}".format(self.table))
        time.sleep(1)

    def run_all(self,type):
        periods = self.getAllPage(type)
        print("所有可获取的期 获取完毕！")
        for period in periods:
            self.run(type,period)

    def run_new_medium(self):
        '''获取最新一期中期票据（AAA）'''
        self.run(type=270101)

    def run_all_medium(self):
        '''获取全部期的中期票据（AAA）'''
        self.run_all(270101)

    def run_new_short(self):
        '''获取最新一期短期融资券'''
        self.run(type=260101,period=None)

    def run_all_short(self):
        '''获取所有期短期融资券'''
        self.run_all(260101)

    def getOnePage1(self,type = 270101, period = None):
        if not period:
            period = "".join(str(datetime.date.today()).split("-")[:2])
        print(f"正在请求中国货币网-中期票据第{period}期")
        url = self.__class__.url.format(type,period,int(1000*time.time()))
        resp =  requests.get(url,headers = self.headers)
        resp.encoding = 'utf8'
        return resp.json()


    def getOnePage2(self,type = 260101, period = '201920'):
        '''
        先获取应用周期，再获取最新的应用周期的内容
        :param type:
        :param period:
        :return:
        '''
        print(f"正在请求中国货币网-短期融资券第{period}期")
        url = "http://www.chinamoney.com.cn/ags/ms/cm-u-bk-currency/BmarkBndVP?referenceName={}".format(type)
        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf8'
        newPeriod = resp.json()["records"][-1]
        return self.getOnePage1(type=type,period=newPeriod)

    def getAllPage(self,type = 260101):
        '''
        先获取应用周期，再获取最新的应用周期的内容
        :param type:
        :param period:
        :return:
        '''
        print(f"正在请求中国货币网-短期融资券全部期数据")
        url = "http://www.chinamoney.com.cn/ags/ms/cm-u-bk-currency/BmarkBndVP?referenceName={}".format(type)
        resp = requests.get(url, headers=self.headers)
        resp.encoding = 'utf8'
        return resp.json()["records"]

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__=="__main__":
    with ChinaMoneyClass() as wp:
        wp.run_new_medium()
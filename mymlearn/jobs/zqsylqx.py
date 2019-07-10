# coding:utf8
import numpy as np
import pandas as pd
import datetime,time
import requests,json
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine
from utils.mymysql import MyMySQL
from . import crawl_parent


class ZqsylqxClass(crawl_parent.CrawlParent):
    '''
    上海清算所-债券收益率曲线
    '''
    url = "http://www.shclearing.com/shchapp/web/valuationclient/shortperiodsinglecurve"
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:20152825@172.17.140.6:3307/spider?charset=utf8',encoding='utf8')
        self.start_date = [2016,1,4]
        self.count = 0 # API计数 每周限额50W个单元格
        self.max = None
        self.table = "zqsylqx_spider"
        self.headers =  {
            'User-Agent':self.UA,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://www.shclearing.com/cpgz/zqjqysp/dqsylqx/'
        }

        self.types = self.getTypes()

    def __enter__(self):
        return self

    def getTypes(self):
        '''
        获取select下拉框列表项
        :return:
        '''
        url = "http://www.shclearing.com/shchapp/web/valuationclient/findshortproidcurve"
        resp = requests.get(url,headers = {"User-Agent":self.UA,"Content-Type":"application/json;charset=UTF-8"})
        resp.encoding = "utf8"
        return resp.json().get("combobox")

    def getNextDay(self):
        '''
        获取目标日期的生成器
        :return:
        '''
        start_day = datetime.date(*self.start_date)
        while start_day + datetime.timedelta(days=1)!=datetime.date.today():
            yield start_day + datetime.timedelta(days=1)
            start_day = start_day + datetime.timedelta(days=1)

    def run(self):
        for d in self.getNextDay():
            print(d)
            new_cates = [self.types[i:i+3] for i in range(0,len(self.types),3)]
            for three_cates in new_cates:
                print(three_cates)
                startTime = str(d)
                self.page = 0
                self.max = None
                if len(three_cates)==3:
                    data = self.getOnePage(startTime,curveOneId=three_cates[0]["data"],curveTwoId = three_cates[1]["data"],curveThreeId = three_cates[2]["data"])
                elif len(three_cates)==2:
                    data = self.getOnePage(startTime,curveOneId=three_cates[0]["data"],curveTwoId = three_cates[1]["data"],curveThreeId = None)
                else:
                    data = self.getOnePage(startTime,curveOneId=three_cates[0]["data"],curveTwoId = None,curveThreeId = None)
                if data["data"]:
                    df = pd.DataFrame(data["data"])
                    df["period"] = str(d)
                    df.to_sql(self.table,self.engine,index=False)
                    with MyMySQL() as m:
                        m.execute_sql("create table if not exists com_{0} like {0}".format(self.table))
                        m.execute_sql("insert into com_{0} select * from {0}".format(self.table))
                        m.execute_sql("drop table {0}".format(self.table))
                    while self.page<self.max:
                        try:
                            if len(three_cates) == 3:
                                data = self.getOnePage(startTime, curveOneId=three_cates[0]["data"],
                                                       curveTwoId=three_cates[1]["data"],
                                                       curveThreeId=three_cates[2]["data"])
                            elif len(three_cates) == 2:
                                data = self.getOnePage(startTime, curveOneId=three_cates[0]["data"],
                                                       curveTwoId=three_cates[1]["data"], curveThreeId=None)
                            else:
                                data = self.getOnePage(startTime, curveOneId=three_cates[0]["data"], curveTwoId=None,
                                                       curveThreeId=None)
                        except Exception as e:
                            print(e)
                            with open("zqsylqx_error.log","a") as fp:
                                print(f"{startTime},page:{self.page-1}")
                                fp.write(f"{startTime},page:{self.page-1}\r\n")
                        else:
                            if data["data"]:
                                df = pd.DataFrame(data["data"]["datas"]).drop(["attach"], axis=1)
                                df.to_sql(self.table, self.engine, index=False)
                                with MyMySQL() as m:
                                    m.execute_sql("create table if not exists com_{0} like {0}".format(self.table))
                                    m.execute_sql("insert into com_{0} select * from {0}".format(self.table))
                                    m.execute_sql("drop table {0}".format(self.table))
                time.sleep(1)


    def getOnePage(self,startTime,curveOneId,curveTwoId,curveThreeId,page = None):
        print(f"正在请求第{self.page}/{None if not self.max else self.max}页")
        curType = '2011-1002' #到期
        postdata = {
            'startTime': startTime,
            'endTime': '',
            'curveOneId': curveOneId,
            'curveTwoId': curveTwoId if curveTwoId else '',
            'curveThreeId': curveThreeId if curveThreeId else '',
            'curveOneTerm': '',
            'curveTwoTerm': '',
            'curveThreeTerm': '',
            'curveOneType': curType,
            'curveTwoType': curType if curveTwoId else '',
            'curveThreeType': curType if curveThreeId else '',
            'NOneTerm': '',
            'KOneTerm': '',
            'NTwoTerm': '',
            'KTwoTerm': '',
            'NThreeTerm': '',
            'KThreeTerm': '',
            'limit': 50,
            'start': 50 * self.page if not page else 50 * page,
        }
        self.page +=1
        resp =  requests.post(self.__class__.url,headers = self.headers,data=postdata)
        resp.encoding = 'utf8'
        print(resp.json())
        if not self.max:
            self.max = int(int(resp.json().get("totalProperty"))/50)
            print(f"一共{self.max}页")
        return resp.json()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


if __name__=="__main__":
    with ZqsyqxClass() as wp:
        wp.run()

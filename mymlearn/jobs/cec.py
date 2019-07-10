# coding:utf8
import time
import requests
from utils.myprocessbar import ProgressBar
from . import crawl_parent
from bs4 import BeautifulSoup as bs

class CecItem(crawl_parent.DbItem):
    def __init__(self):
        self.news_time = None #文件时间
        self.title = None #文件标题
        self.label = None #标签
        self.link_url = None #链接地址
        self.file_content = None # 文件内容
        self.file_url = None # 文件地址


class CecClass(crawl_parent.CrawlParent):

    url = "http://www.cec.org.cn/guihuayutongji/tongjxinxi/yuedushuju/"

    def __init__(self):
        pass

    @staticmethod
    def say():
        progress = ProgressBar(total = 10)
        for i in range(10):
            progress.move()
            progress.log("I'm running...{}".format(i+1))
            time.sleep(0.3)

    def run(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'www.cec.org.cn',
            'Referer': 'http://www.cec.org.cn/guihuayutongji/tongjxinxi/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': self.UA,
        }
        resp = requests.get(self.__class__.url, headers = headers)
        resp.encoding = "gbk"
        soup = bs(resp.text, "lxml")
        content_list = soup.find_all("div", attrs={"class" : "gjzz_nr_lb"})[0].find_all("ul")[0].find_all("li")
        line = CecItem()
        if content_list:
            for content in content_list:
                file_time = content.span.text
                if file_time is not None:
                    line.news_time = file_time.strip("[]")
                else:
                    line.news_time = ""
                file_title = content.a.get("title")
                linkUrl = content.a.get("href")
                line.title = file_title
                line.link_url = linkUrl
                print(linkUrl, file_title)
                line.insert("edb_infor")


if __name__ == "__main__":

    c = CecClass()
    c.run()

# coding:utf8
import time
import requests
from utils.myprocessbar import ProgressBar
from . import crawl_parent
from utils.mymysql import MyMySQL


class DfcfClass(crawl_parent.CrawlParent):

    start_urls = [
        'http://bond.eastmoney.com/news/czqxw.html',
        'http://finance.eastmoney.com/news/cgsxw.html',
    ]

    def __init__(self):
        pass

    @staticmethod
    def get_host(url):
        if "bond" in url:
            return "bond.eastmoney.com"
        else:
            return "finance.eastmoney.com"

    @staticmethod
    def say():
        progress = ProgressBar(total = 10)
        for i in range(10):
            progress.move()
            progress.log("I'm running...{}".format(i+1))
            time.sleep(0.3)

    def run(self):
        headers = {

            "User-Agent": self.UA

        }
        sess = requests.get(self.__class__.url)
        print(sess.status_code)
        print(sess.text)


if __name__ == "__main__":

    c = DfcfClass()
    c.run()

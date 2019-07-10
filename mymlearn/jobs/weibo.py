# coding: utf8
import time,os
from selenium import webdriver
import re
import requests
import urllib

def web_driver():
    chromedriver_path = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver_path

    browser = webdriver.Chrome(chromedriver_path)
    browser.get("https://login.sina.com.cn/signup/signin.php")
    time.sleep(2)

    browser.find_element_by_id('username').send_keys('17621064595')
    browser.find_element_by_id('password').send_keys('zhouhen987')
    time.sleep(2)
    browser.find_element_by_xpath("//div[@class='btn_mod']/input[@class='W_btn_a btn_34px']").click()
    time.sleep(10)


def precrawl(username="17621064595"):
    '''
    模拟网络请求执行赞评转
    :param username:
    :return:
    '''
    s = requests.Session()
    prelogin_url = 'https://passport.weibo.cn/signin/login'
    resp = s.get(prelogin_url)
    resp.encoding="gbk"
    url = "https://login.sina.com.cn/sso/prelogin.php?checkpin=1&entry=mweibo&su=MTc2MjEwNjQ1OTU=&callback=jsonpcallback"
    '''获取nonce，public key'''
    resp = s.get(url)
    print(resp.text)


if __name__=="__main__":
    #precrawl("17621064595")
    web_driver()
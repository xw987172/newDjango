from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import json
import requests
from django.db import connection
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
# Create your views here.

def aindex(request):
    #page = request.GET.get("page")
    #pSize = request.GET.get("pageSize")
    response = {}
    total =  0
    with connection.cursor() as cur:
        cur.execute("select count(1) from spider.com_news")
        total = cur.fetchall()[0][0]
    response["total"] = total
    response["data"] = []
    with connection.cursor() as cur:
        cur.execute("select title,entityurl,entitytime,rate from spider.com_news where rate is null order by entitytime desc limit 50")
        data = cur.fetchall()
    response["data"] = [{"title":x,"entityurl":y,"entitytime":z,"rate":k} for x,y,z,k in data]
    return render(request,"article/index.html",response)

def detail(request):
    url = request.GET.get("entityurl")
    title = request.GET.get("title")
    rate = request.GET.get("rate")
    return render(request,"article/detail.html",{"title":title,"entityurl":url,"rate":rate})

def setRate(request):
    entityurl = request.POST.get("entityurl")
    rate = request.POST.get("rate")
    with connection.cursor() as cur:
        cur.execute("update spider.com_news set rate = '{0}',ready=1 where entityurl = '{1}'".format(rate,entityurl))
    return JsonResponse({"status":'success'})

def search(request):
    response = {}
    ifcate = request.POST.get("ifcate")
    main_key = request.POST.get("main_key")
    cate = 0
    if ifcate in ["cate","nocate"]:
        with connection.cursor() as cur:
            cur.execute("select title,entityurl,entitytime,rate from spider.com_news where ready={0} and data_source is null order by data_source asc limit 100".format(1 if ifcate=="cate" else 0))
            data = cur.fetchall()
    elif ifcate!="train":
        with connection.cursor() as cur:
            cur.execute("select title,entityurl,entitytime,rate from spider.com_news where title like '%%{0}%%'".format(main_key))
            data = cur.fetchall()
    else:
        c = "C1,C2,C3,C4,C6,C8,C3_tt,Other,risk,instInfo"
        cate=1
        with connection.cursor() as cur:
            cur.execute("select {0} from com_news_train".format(c))
            data = cur.fetchall()
    if cate ==0:
        response["data"] = [{"title":x,"entityurl":y,"entitytime":z,"rate":k} for x,y,z,k in data]
        return render(request,"article/lists.html",response)
    else:
        cList = c.split(",")
        response["data"] =  [{cList[0]:x0,cList[1]:x1,cList[2]:x2,cList[3]:x3,cList[4]:x4,cList[5]:x5,cList[6]:x6,cList[7]:x7,cList[8]:x8,cList[9]:x9} for x0,x1,x2,x3,x4,x5,x6,x7,x8,x9 in data]
        return render(request,"article/lists_train.html",response)

def doExcelIndex(request):
    return render(request,"article/excelindex.html")

def getNews(request):
    content = request.FILES.get('myexcel').read()
    soup = bs(content,"lxml")
    trs = soup.find("table").find_all("tr")
    for tr in trs:
        name = tr.find_all("td")[1].text
        rate = tr.find_all("td")[3].find("span").text
        getUrl(name,rate)
    return redirect("http://39.97.184.89:5050/articleaindex/")

def getUrl(name,rate):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
    }
    s = requests.session()
    s.get("https://www.baidu.com/",headers=headers)
    url = """https://www.baidu.com/s?wd={0}""".format(quote(name,'utf-8'))
    entityurl = None
    try:
        resp = s.get(url,headers= headers)
        resp.encoding = "utf8"
        soup = bs(resp.text,"lxml")
        content = soup.find_all("div",attrs={"id":"content_left"})[0]
        lists = content.find_all("div",attrs={"class":"result c-container"})
        for li in lists:
            aa = li.find_all("a")
            for tt in aa:
                if name in tt.text:
                    entityurl = tt.get("gref")
                    break
        if entityurl == None:
            entityurl = lists[0].find_all("a")[0].get("href")
    except:
        pass
    finally:
        if entityurl!=None:
            with connection.cursor() as cur:
                cur.execute("select title from com_news where title='{0}'".format(name))
                result = cur.fetchone()
                if result == None:
                    print(name)
                    cur.execute("insert into com_news(title,entityurl,rate,ready) values('%s','%s','%s',0)" %(name,entityurl,rate))
                    connection.commit()


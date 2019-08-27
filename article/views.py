from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import json
from django.db import connection
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

    return render(request,"article/detail.html",{"title":title,"entityurl":url})

def setRate(request):
    entityurl = request.POST.get("entityurl")
    rate = request.POST.get("rate")
    with connection.cursor() as cur:
        cur.execute("update spider.com_news set rate = '{0}' where entityurl = '{1}'".format(rate,entityurl))
    return JsonResponse({"status":'success'})

def search(request):
    response = {}
    ifcate = request.POST.get("ifcate")
    main_key = request.POST.get("main_key")
    cate = 0
    if ifcate in ["cate","nocate"]:
        with connection.cursor() as cur:
            cur.execute("select title,entityurl,entitytime,rate from spider.com_news where rate is {0} null order by entitytime desc limit 50".format('not' if ifcate=="cate" else ""))
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

from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
# Create your views here.
from mymlearn.main import w,work
def index(request):
    result = dict()
    with connection.cursor() as cursor:
        cursor.execute("select m,c,f,d,last_time from spider.crawl_setting where isvalid=1")
        result["headers"] = ["模块","类","类实例方法","说明","上次执行时间"]
        result["data"] = cursor.fetchall()
    return render(request,'crawl_index.html',result)

def action(request):
    m = request.GET.get("m")
    c = request.GET.get("c")
    f = request.GET.get("f")
    work([m,c,f])
    return HttpResponse(w(m,c,f)+"执行完成")

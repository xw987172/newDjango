from django.shortcuts import render
import pdfkit
import os
from django.db import connection
# Create your views here.
from django.http import HttpResponse,Http404,FileResponse
def index(request):
	return render(request,'index.html')

def myprofile(request):
    file_path="static/myprofile.pdf"
	#pdf = pdfkit.from_file('myprofile.pdf',False)
    with open(file_path,'rb') as f:
        response = FileResponse(f)
        response['content_type'] = "application/octet-stream"
        #response['content_type'] = "application/x-msdownload"
        response["Content-Disposition"] = 'attachment; filename=' + os.path.basename(file_path)
        return response

def search(request):
    result = dict()
    if request.method=='POST':
        key = request.POST.get("main_key")
        with connection.cursor() as cursor:
            cursor.execute("SELECT table_schema,table_name,data_length,table_comment FROM information_schema.`TABLES` WHERE table_comment LIKE \"%%{0}%%\" or table_name like '%%{0}%%'".format(key))
            result["table"] = cursor.fetchall()
            result["table_headers"] = ["数据库名","数据表名","行数","备注"]
            cursor.execute("select table_schema,table_name,column_name,column_comment from information_schema.columns where column_comment like '%%{0}%%' or column_name like '%%{0}%%'".format(key))
            result["column"] = cursor.fetchall()
            result["column_headers"] = ["数据库名","数据表名","字段","字段备注"]
    return render(request,'search.html',result)

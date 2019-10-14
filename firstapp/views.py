from django.shortcuts import render
import pdfkit
import os
import pandas as pd
from io import BytesIO
from django.db import connection
# Create your views here.
from django.http import HttpResponse,Http404,FileResponse
def data_index(request):
    cursor = connection.cursor()
    try:
        cursor.execute(f"select name from spider.django_get_data")
        data = cursor.fetchall()
    except Exception as err:
        print(err)
        return HttpResponse("select name from spider.django_get_data 这句话查询有问题，请检查数据库连接或表有问题")
    step = 4
    data1 = [data[i:i + step] for i in range(0, len(data), step)]
    return render(request,'get_data_index.html',{"dataSetInfo":data1})

def getDataSetByName(request):
    name = request.POST.get("data_name")
    with connection.cursor() as cursor:
        cursor.execute(f"select data_desc from spider.django_get_data where name = '{name}'")
        print(f"select data_desc from spider.django_get_data where name = '{name}'")
        data = cursor.fetchall()
        cursor.execute(data[0][0])
        columns = [col[0] for col in cursor.description]
        data0 = cursor.fetchall()
        pd_data = pd.DataFrame(list(data0),columns = columns)

        response = HttpResponse(content_type='application/vnd.ms-excel')
        execl_name = name
        response['Content-Disposition'] = 'attachment;filename={0}.xlsx'.format(execl_name)
        outfile = BytesIO()
        pd_data.to_excel(outfile, index=False)
        response.write(outfile.getvalue())
        return response


def index(request):
    return render(request,"index.html")

def myprofile(request):
    file_path="static/myprofile.pdf"
	#pdf = pdfkit.from_file('myprofile.pdf',False)
    with open(file_path,'rb') as f:
        response = FileResponse(f)
        response['content_type'] = "application/octet-stream"
        #response['content_type'] = "application/x-msdownload"
        response["Content-Disposition"] = 'attachment; filename=' + os.path.basename(file_path)
        return response

def checkExcelSample(request):
    excel = request.FILES.get("myExcel")
    response = HttpResponse()
    result = ""
    try:
        pd_data = pd.read_excel(excel)
    except:
        pd_data = pd.read_csv(excel)
    if "证券代码" not in pd_data.columns.tolist():
        result += '因公司名称时常发生变更，所以需要证券代码，请补充证券代码\n'
    else:
        pd_data["证券代码"] = pd_data["证券代码"].fillna('999999')
        dList = pd_data[pd_data["证券代码"]=='999999'].index.tolist()
        pd_data = pd_data.drop(dList)
        stocks = pd_data["证券代码"].values.tolist()
        compcode = list()
        excepts_stocks = list()
        with connection.cursor() as cursor:
            for stock in stocks:
                sql = f"select s_info_compcode from cbondissuer where s_info_szcode = '{stock}' or substring_index(s_info_szcode,'.',1) = '{stock}'"
                cursor.execute(sql)
                data =  cursor.fetchall()
                if len(data)==0 or data[0][0]==None:
                    excepts_stocks.append(str(stock))
                else:
                    compcode.append(str(data[0][0]))
        if len(excepts_stocks)>0:
            estocks = ",".join(excepts_stocks)
            result += f"{estocks}未能在spider.cbondissuer证券表中寻找到对应公司\n\n"
        compcode_str = ",".join(compcode)
        columns = pd_data.columns.tolist()
        excepts_columns = list()
        for cl in columns:
            if cl in ("公司名称","证券代码"):
                continue
            with connection.cursor() as cursor:
                sql = f"select table_name,column_name,column_comment from information_schema.columns where table_name in ('sz_company','com_report_total','com_financial_analyse','com_report_total_tb','com_financial_analyse_tb','com_report_total_zjz','com_financial_analyse_zjz') and column_comment='{cl}'"
                cursor.execute(sql)
                data0 =  cursor.fetchall()
                if len(data0) == 0:
                    excepts_columns.append(cl)
        if len(excepts_columns)>0:
            ecolumns = ",".join(excepts_columns)
            result += f"{ecolumns}未能找到\r\n"
    if result =="":
        response.write("OK")
    else:
        response.write("<span style='color:red'>"+result+"</span>")
    return response


def getExcelSample(request):
    excel = request.FILES.get("myExcel")
    year = request.POST.get("report_period")
    try:
        pd_data = pd.read_excel(excel)
    except:
        pd_data = pd.read_csv(excel)
    if "证券代码" not in pd_data.columns.tolist():
        response = HttpResponse()
        response.write("<script>alert('因公司名称时常发生变更，所以需要证券代码，请补充证券代码')</script>")
    else:
        pd_data["证券代码"] = pd_data["证券代码"].fillna('999999')
        dList = pd_data[pd_data["证券代码"]=='999999'].index.tolist()
        pd_data = pd_data.drop(dList)
        stocks = pd_data["证券代码"].values.tolist()
        compcode = list()
        excepts_stocks = list()
        with connection.cursor() as cursor:
            for stock in stocks:
                sql = f"select s_info_compcode from cbondissuer where s_info_szcode = '{stock}' or substring_index(s_info_szcode,'.',1) = '{stock}'"
                cursor.execute(sql)
                data =  cursor.fetchall()
                if len(data)==0 or data[0][0]==None:
                    excepts_stocks.append(str(stock))
                else:
                    compcode.append(str(data[0][0]))
        if len(excepts_stocks)>0:
            estocks = ",".join(excepts_stocks)
            pd_data = pd_data[~pd_data["证券代码"].astype("str").isin(excepts_stocks)]
        compcode_str = ",".join(compcode)
        columns = pd_data.columns.tolist()
        for cl in columns:
            if cl in ("公司名称","证券代码"):
                continue
            sql = f"select table_name,column_name,column_comment from 财务指标 where column_comment='{cl}'"
            with connection.cursor() as cursor:
                sql = f"select table_name,column_name,column_comment from information_schema.columns where table_name in ('sz_company','com_report_total','com_financial_analyse','com_report_total_tb','com_financial_analyse_tb','com_report_total_zjz','com_financial_analyse_zjz','com_report_zb') and column_comment='{cl}'"
                cursor.execute(sql)
                data0 =  cursor.fetchall()
                if len(data0) == 0:
                    continue
                else:
                    values = []
                    for code in compcode:
                        if data0[0][0] =="sz_company":
                            sql = f"select {data0[0][1]} from {data0[0][0]} where id ={code}"
                        else:
                            sql = f"select {data0[0][1]} from {data0[0][0]} where report_period ='{year}' and s_info_compcode ={code}"
                        cursor.execute(sql)
                        data =  cursor.fetchall()
                        v = data[0][0] if len(data)==1 else None
                        values.append(v)
                    pd_data[cl] = values
        response = HttpResponse(content_type='application/vnd.ms-excel')
        execl_name = "数据集"
        response['Content-Disposition'] = 'attachment;filename={0}.xlsx'.format(execl_name)
        outfile = BytesIO()
        pd_data.to_excel(outfile, index=False)
        response.write(outfile.getvalue())
        return response

def getDataSet(request):
    data_name = request.POST.get("data_name")
    data_desc = request.POST.get("data_desc")
    with connection.cursor() as cursor:
        try:
            print(data_desc)
            cursor.execute(data_desc)
            data = cursor.fetchall()
        except Exception as err:
            return HttpResponse("sql语法有误，请重新检查")
        else:
            print(f"insert into spider.django_get_data(name,data_desc) values('{data_name}',\"{data_desc}`)\"")
            try:
                cursor.execute(f"insert into spider.django_get_data(name,data_desc) values('{data_name}',\"{data_desc}\")")
                cursor.execute(f"select name from spider.django_get_data")
                data = cursor.fetchall()
            except:
                return HttpResponse("重复录入")
            html = "<table class=\"table\">"
            step = 4
            data1 = [data[i:i + step] for i in range(0, len(data), step)]
            for dt in data1:
                html +="<tr>"
                for name in dt:
                    name = name[0]
                    html += f"<td><button class='btn-primary'>{name}</button></td>"
                html += "</tr>"
            return HttpResponse(html)
                

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

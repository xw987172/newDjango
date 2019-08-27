from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
import joblib
import pandas as pd
import numpy as np
def fisher(request):
    model = joblib.load("files/model/fisher_judge_2019.pkl")
    # 系数与常数项
    w,w0 = model.coef_,model.intercept_
    data = dict()
    data["s_info_compname"] = ["西藏天路股份有限公司","京东方","中国天盈"]
    data["report_period"] = ["20181231","20181231","20181231"]
    data["带息债务/全部投入资本"] = [45.9478,105,90]
    data["总资产报酬率"] = [8.7751,20,16]
    data["流动负债/负债合计"] = [67.128,19,50]
    data["管理费用/营业总收入"] = [9.2959,10,40]
    data["预收账款"] = [13562.82,7000,50000]
    data["预付款项"] = [1890,2000,15000]
    data["流动资产周转率"] = [70,20,9]
    data["销售成本率"] = [10,20,30]
    data["总资产净利润"] = [200,100,50]
    data["固定资产"] = [32132,203721,29908]
    data["未分配利润"] = [809809,2132100,218309271]
    data["无形资产"] = [1000,2302,800]
    data["fcff/经营性净现金流"] = [10,20,30]
    grades = getGrades(pd.DataFrame(data).drop(["s_info_compname","report_period"],axis=1),w,w0)
    result = dict()
    result["s_info_compname"] =  data["s_info_compname"]
    result["report_period"] = data["report_period"]
    result["score"] = grades.tolist()
    return JsonResponse(result)

def getGrades(sample,w,w0):
    """
    判断样本结果
    """
    return -1*(np.dot(sample,w.T)+w0)

def getRank(inScore):
    """获取评级级别"""
    iIndex = [str(x) for x in reversed(range(0,100,5))]
    lPercentile = [np.percentile(inScore,float(x)) for x in iIndex]
    df = pd.DataFrame(lPercentile, index = iIndex)

    lLevel = []


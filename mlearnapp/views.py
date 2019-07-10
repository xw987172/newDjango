from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import pandas as pd
# Create your views here.
def mindex(request):
    data = dict()
    data["featureSelect"] = {
        "sklearn.decomposition-PCA":"主成分分析法",
        "sklearn.lda-LDA":"线性判别分析法",
        "k":"逐步回归降维法(P值)"
    }
    return render(request,"mlearnapp/index.html" ,data)

def modelList(request):
    mType = request.GET.get("modelType")
    data = {
        "分类":{
            "sklearn.linear_model-LogisticRegression":"逻辑斯遆回归",
            "sklearn.svm-SVC":"支持向量机",
            "sklearn.tree-DecisionTreeClassifier":"决策树",
            "sklearn.ensemble-RandomForestClassifier":"随机森林分类",
            "sklearn.neighbors-KNeighborsClassifier":"KNN",
            "sklearn.lda-LDA":"fisher判别",
        },
        "回归":{
            "sklearn.linear_model-LinearRegression":"简单线性回归",
        }
    }
    return JsonResponse({"modelList":data[mType]});

def fitp(request):
    from sklearn.model_selection import train_test_split
    pd_excel = pd.read_excel(request.FILES.get('train_test_file'))
    featureSelectMethod = request.POST.get("featureSelect")
    modelSelectMethod = request.POST.get("modelSelect")
    y = pd_excel["y"]
    if featureSelectMethod =="":
        X = pd_excel.drop(['y'],axis=1)
    else:
        fsclass = getReflectFunc(featureSelectMothod)
        oriX = pd_excel.drop(['y'],axis=1)
        if "PCA" in featureSelectMethod:
            X = fsclass(2).fit_transform(oriX)
        elif "LDA" in featureSelectMethod:
            X = fsclass(2).fit_transform(oriX,y)
    train_X,test_X, train_y, test_y  = train_test_split(X,y,test_size = 0.3)
    mfunc = getReflectFunc(modelSelectMethod)
    clf = mfunc().fit(train_X,train_y)
    y_pred = clf.predict(test_X)
    err_no = (test_y!=y_pred).sum()
    message = "样本总数： %d，误差率：%d%%" % (test_X.shape[0],(100*abs(test_y.sum()-y_pred.sum())/test_y.sum()))
    return HttpResponse(message+str(test_y.tolist())+str(y_pred.tolist()))

def getReflectFunc(st):
    oriM = st.split(".")[0]
    ms,cs = st.split("-")
    m = __import__(ms,fromlist=(oriM,))
    c = getattr(m,cs)
    return c

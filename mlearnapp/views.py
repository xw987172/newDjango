from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import pandas as pd

from featureFunctions import stepwise_selection
# Create your views here.
def mindex(request):
    data = dict()
    data["featureSelect"] = {
        "sklearn.decomposition-PCA":"主成分分析法",
        "sklearn.discriminant_analysis-LinearDiscriminantAnalysis":"线性判别分析法",
        "self_P":"逐步回归降维法(P值)"
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
            "sklearn.discriminant_analysis-LinearDiscriminantAnalysis":"fisher判别",
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
    myfeatures = request.POST.get("mfeatures").split(",")
    X = pd_excel[myfeatures]
    train_X,test_X, train_y, test_y  = train_test_split(X,y,test_size = 0.3)
    mfunc = getReflectFunc(modelSelectMethod)
    clf = mfunc().fit(train_X,train_y)
    y_pred = clf.predict(test_X)
    err_no = (test_y!=y_pred).sum()
    if len(y.unique().tolist())>2:
        message = "样本总数： %d，误差率：%d%%" % (test_X.shape[0],(100*abs(test_y.sum()-y_pred.sum())/test_y.sum()))
    else:
        message = "样本总数： %d 错误样本数 : %d，正确率：%d%%" % (test_X.shape[0],err_no,(100*(test_X.shape[0]-err_no)/test_X.shape[0]))
    return HttpResponse(message+str(test_y.tolist())+str(y_pred.tolist()))

def getFileHeader(request):
    mFile_pd = pd.read_excel(request.FILES.get("train_test_file"));
    html = "<table class='table'>"
    content = ""
    for cl in mFile_pd.columns:
        content += f"<tr><td>{cl}</td><td><select name='cl_{cl}'><option value='1'>原值</option><option value='2'>不参与训练</option><option value='3'>归一化</option><option value='4'>标准化</option><option value='5'>独热编码</option>><option value='6'>预测值</option></select></td></tr>"
    html+=content+"</table>"
    return HttpResponse(html)

def getFeatures(request):
    mFile_pd = pd.read_excel(request.FILES.get("train_test_file"))
    y = mFile_pd['y']
    X = mFile_pd.drop(['y'],axis=1)
    fsMethod = request.POST.get("featureSelect")
    if "self" in fsMethod:
        columns = stepwise_selection(X,y)
    elif fsMethod=="":
        columns = X.columns
    elif "PCA" in fsMethod or "LinearDiscriminantAnalysis" in fsMethod:
        fsclass = getReflectFunc(fsMethod)
        columns = fsclass(2).fit_transform(X).columns
    else:
        raise Exception("选择特征异常")
    return HttpResponse(",".join(columns))

def getReflectFunc(st):
    oriM = st.split(".")[0]
    ms,cs = st.split("-")
    m = __import__(ms,fromlist=(oriM,))
    c = getattr(m,cs)
    return c


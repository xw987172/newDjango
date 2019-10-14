"""xwproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from firstapp.views import index,myprofile,search,data_index,getExcelSample,checkExcelSample,getDataSet,getDataSetByName
app_name = 'firstapp'
urlpatterns = [
	path('myprofile/', myprofile,name='myprofile'),
	path('search/',search,name='search'),
    path("data_index/",data_index,name='data_index'),
    path("getExcelSample/",getExcelSample,name='getExcelSample'),
    path("checkExcelSample/",checkExcelSample,name="checkExcelSample"),
    path("getDataSet/",getDataSet,name = "getDataSet"),
    path("getDataSetByName/",getDataSetByName,name = "getDataSetByName"),
]

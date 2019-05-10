from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
	return HttpResponse("这是地图app的首页")

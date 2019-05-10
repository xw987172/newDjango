from django.shortcuts import render
import pdfkit
# Create your views here.

def index(request):
	return render(request,'index.html')

def myprofile(request):
	pdf = pdfkit.from_file('myprofile.pdf',False)
	return render(request,'myprofile.html',{'pdf':pdf})

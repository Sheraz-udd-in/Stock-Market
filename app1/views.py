from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def fun(request):
    return render(request, 'index.html')

def fun1(request):
    return render(request, 'market.html')

def fun2(request):
    return render(request, 'register.html')

def fun3(request):
    return render(request,'login.html')

def fun4(request):
    return render(request,'logout.html')
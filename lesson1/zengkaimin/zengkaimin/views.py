#coding=utf8
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def firstpage(request):
    return render(request,'index2.html')

def mylogin(request):
    if request.method == 'GET':
        return render(request,'pages/examples/login.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        passwd = request.POST.get('passwd')
        user =  authenticate(username=name,password=passwd)
        ret = { }
        if user is not None:
            login(request, user)
            ret['status'] = 0
        else:
            ret['status'] = 1

        return JsonResponse(ret)





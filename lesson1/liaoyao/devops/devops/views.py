#encoding: utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request,'index.html')


def needlogin(request):
    print(request.POST)
    if request.method == 'GET':
        nexturl = request.GET.get('next')
        print(nexturl)
        return render(request, 'pages/examples/login.html',{'nexturl':nexturl})
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        user = authenticate(username=name,password=pwd)
        result = {}
        if user:
            login(request,user)
            result['status'] = 0
        else:
            result['status'] = 1
        return JsonResponse(result)

def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/logout')


def test(request):
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'test.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        result = {name: pwd}
        return JsonResponse(result)


@login_required
def hello(request):
    return HttpResponse('Hello!!')

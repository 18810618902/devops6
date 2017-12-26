from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse

# Create your views here.

def hello(request):
    # return HttpResponse('hello')
    users = {'users':[{'name':'name1','id':'id1'},{'name':'name2','id':'id2'}]}
    # return render(request,'hello.html',users,{'username':'51reboot'})
    return render(request,'index.html')
def user(request,id):
    return HttpResponse(id)

def add(request,id1,id2):
    return HttpResponse(int(id1)+int(id2))

def users1(request,**kwargs):
    pk = kwargs.get('pk2')
    return HttpResponse(pk)

def argstest(request):
    uname = request.GET.get('username')
    uid = request.GET.get('id')
    rel = {'nmae':uname,'id':uid}

    return JsonResponse(rel)



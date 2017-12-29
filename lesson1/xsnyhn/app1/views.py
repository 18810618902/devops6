#coding=utf-8
from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.
from django.http.response import JsonResponse
import json
#json.dumps(字典)


def hello(request):
    #return HttpResponse('hello app1!')
    context = {}
    lans=['python','java','go','javascript','node']
    users = [
        {'name':'sam','id':1},
        {'name':'xu','id': 2},
        {'name':'samxu','id':3}
    ]
    context['username'] = 'samxu'
    context['lans'] = lans
    context['users'] = users
    context['n1'] = 20
    context['n2'] = 70
    #return  render(request,'hello.html',{'username':'samxu'},context) #默认去找myweb下面的templates的对应的html
    return render(request, 'hello.html', context)

def users(request,pk):
    return HttpResponse('id is %s'%pk)

def add(request,n1,n2):
    sum = int(n1) + int(n2)
    return HttpResponse(sum)

def users1(request,**kwargs):
    print request.META
    print request.user
    pk1 = kwargs.get('pk')
    return HttpResponse('user name:%s'%pk1)
def argstest(request):
    name = request.GET.get('username')
    uid = request.GET.get('id')
    ret = {'name':name,'id':uid}
    return JsonResponse(ret)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
import random

from django.views import View
from django.views.generic import TemplateView, ListView

from .models import *

from django.shortcuts import render

# # Create your views here.
# def hello(request):
#     return HttpResponse('Hello django!')

# def users(reuqest,pk,pk2):
#     # print pk
#     # a=int(pk)+int(pk2)
#     return HttpResponse(pk)

class user1(View):
    def get(self,reuqest,**kwargs):
        # print kwargs
        # print reuqest.user
        pk1=kwargs.get('pk')
        # pk1=self.kwargs.get('pk')
        # a=int(pk)+int(pk2)
        return HttpResponse(pk1)

class hello(TemplateView):
    template_name = 'hello.html'
    def get_context_data(self, **kwargs):
        context=super(hello, self).get_context_data(**kwargs)
        # context={}
        context['username']='韩寒'
        context['lags']=['python','js','java']
        if context['pm'] is None:
            context['pm']=1
        return context


class authorlist(ListView):

    model = Author

    template_name = 'app1/authors.html'
    context_object_name = 'authors'

    paginate_by = 10

    def get_context_data(self, **kwargs):

        context = super(authorlist, self).get_context_data(**kwargs) # 生成分页数据
        print context
        context['job'] = 'pythoner'

        return context

    def get_queryset(self):

        return self.model.objects.order_by('-name')


# @login_required
# def hello(request):
#     context={}
#     # context['SITE_NAME']=settings.SITE_NAME
#     context['n1']=random.randint(0,99)
#     context['n2']=random.randint(0,50)
#     context['name']='lilei'
#     context['lags']=['java','python','javascript','php','go']
#     context['data']=[
#         {'name':'name1','id':1},
#         {'name':'name2','id':2},
#         {'name':'name3','id':3}
#     ]
#     print context
#     return render(request,'hello.html',context)


class ADD(View):
    def get(self,request,a,b):
        pk=int(a)+int(b)
        return HttpResponse(pk)
#
# def ADD(request,a,b):
#     pk=int(a)+int(b)
#     return HttpResponse(pk)

class argstest(View):
    def get(self,request):
        name=request.GET.get('name',None)
        uid=request.GET.get('id',None)
        ret={'name':name,'id':uid}
        return JsonResponse(ret)

# def argstest(request):
#     name=request.GET.get('name',None)
#     uid=request.GET.get('id',None)
#     ret={'name':name,'id':uid}
#     return  JsonResponse(ret)

# def plus(request,n1,n2):
#     ret=int(n1)+int(n2)
#     return HttpResponse(str(ret))


class plus(View):
    def get(self,request,n1,n2):
        ret=int(n1)+int(n2)
        return HttpResponse(str(ret))


# def bookquery(request):
#     # data=[i for i in Book.objects.all().values('name','price')]
#     data=[i.todict for i in Book.objects.all()]
#     return JsonResponse({'status':0,'msg':'ok','data':data})

class bookquery(View):
    def get(self,reuqest):
        data=[i.todict for i in Book.objects.all()]
        return JsonResponse({'status':0,'msg':'ok','data':data})

class authquery(View):
    def get(self,request):
        qs = Author.objects.all()
        qsf = qs.order_by('-fans')[:2]
        qsi = qs.order_by('-income')[:2]
        qsr = list(set(qsf).union(set(qsi)))
        data = [i.todict for i in qsr]
        # data=[i.todict for i in Author.objects.all()]
        return JsonResponse({'status': 0, 'msg': 'ok', 'data': data})


# def authquery(request):
#     # data=[i for i in Book.objects.all().values('name','price')]
#     qs=Author.objects.all()
#     qsf=qs.order_by('-fans')[:2]
#     qsi=qs.order_by('-income')[:2]
#     qsr=list(set(qsf).union(set(qsi)))
#     data=[i.todict for i in qsr]
#     # data=[i.todict for i in Author.objects.all()]
#     return JsonResponse({'status':0,'msg':'ok','data':data})


class users(View):
    def get(self,request):
        return  HttpResponse('Hello world')







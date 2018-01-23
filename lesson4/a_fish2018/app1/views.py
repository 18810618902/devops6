# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import  HttpResponse,JsonResponse,HttpResponseRedirect
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import json
from .models import *
from django.views import View
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic import ListView,DetailView
import datetime
from django.http import QueryDict
from page import JuncheePaginator
from django.db.models import Q

@method_decorator(login_required,name='dispatch')
class firstpage(TemplateView):
    template_name = "index2.html"


# @csrf_exempt
class mylogin(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        nexturl = self.request.GET.get("next")
        return {'nexturl':nexturl}


    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        ret = {}
        if user is not None:
            login(request,user)
            ret['status'] = 0
        else:
            ret['status'] = 1
        return JsonResponse(ret)

class mylogout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('firstpage'))

class bookquery(View):
    def get(self,request):
        data = [i.todict for i in Book.objects.all()]
        return JsonResponse({'status': 0, 'data': data})

class authorquery(View):
    def get(self,request):
        qs = Author.objects.all()
        qsfans = qs.order_by('-fans')[:2]
        qsincome = qs.order_by('income')[:2]
        qsret = list(set(qsfans).union(set(qsincome)))
        data = [i.todict for i in Author.objects.all()]
        return JsonResponse({'status': 0, 'data': data})


class users(View):
    def get(self,request):
        return HttpResponse('Hello world')

class users1(View):
    def get(self,request,**kwargs):
        print request.user
        pk1 = self.kwargs.get('pk')
        return HttpResponse(pk1)


class hello(TemplateView):
    template_name = 'hello.html'

    def get_context_data(self,**kwargs):
        kwargs['username'] = "韩寒"
        kwargs['lans'] = ['python','flask','django','java']
        print kwargs
        return kwargs

# class authorlist(ListView):
#     model = Author
#     template_name = 'authors.html'
#     context_object_name = 'authors'
#     paginate_by = 3
#     search = 'search'
#
#     def get_context_data(self, **kwargs):
#         context = super(authorlist,self).get_context_data(**kwargs)
#         context['job'] = 'pythonor'
#         return context
#     def get_queryset(self):
#         return self.model.objects.order_by('-name')


class authorapi(View):
    pk_url_kwarg = 'pk'
    model = Author
    def get(self,request,*args,**kwargs):
        pk = kwargs.get(self.pk_url_kwarg)
        if pk:
            obj = self.model.objects.get(pk=pk)
            data = obj.todict
            return JsonResponse(data)
        else:
            qs = self.model.objects.all()
            qs = qs.filter(createtime__gt='2018-01-05')
            qsincome = qs.order_by('-income')[:2]
            qsfansnum = qs.order_by('-fansnum')[:2]
            qslist = list(set(qsincome).union(set(qsfansnum)))
            data = [i.todict for i in qslist]
            ret = {}
            ret['data'] = data
            ret['status'] = 0
            return JsonResponse(ret)


# class authordetail(DetailView):
#     model = Author
#     bookmodel = Book
#     context_object_name = "author"
#     pk_url_kwarg = 'pk'
#     template_name = "authordetail.html"
#
#     def get_context_data(self, **kwargs):
#         kwargs['timenow'] = datetime.datetime.now()
#         return super(authordetail,self).get_context_data(**kwargs)
#
#     # 增
#     def post(self,request,*args,**kwargs):
#         # 接收前端数据
#         rqs = QueryDict(request.body).dict()
#         rqsbooks = rqs['books']
#         print rqsbooks
#         books = [book.strip() for book in json.loads(rqsbooks)]
#         # 判断书在不在数据库，在单独话存数据，不在返回错误信息
#         errorinfo = []
#         bookobjs = []
#         for book in books:
#             try:
#                 bookobj = self.bookmodel.objects.get(name=book)
#             except self.bookmodel.DoesNotExist:
#                 errorinfo.append({'name':book})
#             else:
#                 bookobjs.append(bookobj)
#         if errorinfo:
#             return JsonResponse({'status':-1,'data':errorinfo})
#         # 创建作者对象（即除了书以外的）
#         rqs.pop('books')
#         authorobj = self.model.objects.create(**rqs)
#         # 写作者和书的manytomany关系
#         for bookobj in bookobjs: bookobj.author.add(authorobj)
#         return JsonResponse({'status':0})
#
#     # 改
#     def put(self,request,*args,**kwargs):
#         bookidskey = 'bookids'
#         pk = self.kwargs.get(self.pk_url_kwarg)
#         rqs = QueryDict(request.body).dict()
#         print rqs
#         bks = rqs.get(bookidskey)
#         print bks
#         bks = [int(bookid) for bookid in json.loads(bks)]
#         if rqs.get(bookidskey): rqs.pop(bookidskey)
#         authorbookids = [bk.id for bk in self.model.objects.get(pk=pk).book_set.all()]
#         diffids = list(set(authorbookids).difference(set(bks)))
#         if diffids:
#             for bookid in diffids:
#                 bkobj = self.bookmodel.objects.get(pk=bookid)
#                 authorobj = self.model.objects.get(pk=pk)
#                 authorobj.book_set.remove(bkobj)
#         self.model.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg)).update(**rqs)
#         return JsonResponse({'status':0})
#
#     # 删
#     def delete(self,request,*args,**kwargs):
#         pk=self.kwargs.get(self.pk_url_kwarg)
#         self.model.objects.get(pk=pk).delete()
#         return JsonResponse({'status': 0})

class authorinfo(View):
    template_name="authordetail.html"
    model = Author

    def get(self,request,*args,**kwargs):
        pk = kwargs.get("pk")
        obj = self.model.objects.get(pk=pk)
        data = model_to_dict(obj, exclude=[])
        print data
        return render(request,self.template_name, {'data': data})

class authorlist(View):
    template_name = 'authors.html'  # 模板名
    model = Author
    bookmodel = Book
    pk_url_kwarg = 'pk'
    search = 'search'

    def get_queryset(self, search):  # 数据库查询的结果
        qs = self.model.objects.all()
        if search:
            qs = qs.filter(Q(name__contains=search)|Q(note__contains=search))  # 模糊搜索匹配search的（name或note）
        return qs

    def get(self, request, *args, **kwargs):
        pk = kwargs.get(self.pk_url_kwarg)
        if pk:
            obj = self.model.objects.get(pk=pk)
            data = model_to_dict(obj, exclude=[])
            return JsonResponse({'status':0, 'data':data})
        else:
            page_num = request.GET.get('page', 1)  # 请求的第几页
            search = request.GET.get(self.search)
            qs = self.get_queryset(search)
            pageobj = JuncheePaginator(qs)
            wdata = pageobj.pagecomputer(page_num)
            return render(request, self.template_name, {'res_data': wdata[0], 'allpages': wdata[1], 'search':search})

    # 增
    def post(self,request,*args,**kwargs):
        # 接收前端数据
        rqs = QueryDict(request.body).dict()
        rqsbooks = rqs['books']
        print rqsbooks
        books = [book.strip() for book in json.loads(rqsbooks)]
        # 判断书在不在数据库，在单独话存数据，不在返回错误信息
        errorinfo = []
        bookobjs = []
        for book in books:
            try:
                bookobj = self.bookmodel.objects.get(name=book)
            except self.bookmodel.DoesNotExist:
                errorinfo.append({'name':book})
            else:
                bookobjs.append(bookobj)
        if errorinfo:
            return JsonResponse({'status':-1,'data':errorinfo})
        # 创建作者对象（即除了书以外的）
        rqs.pop('books')
        authorobj = self.model.objects.create(**rqs)
        # 写作者和书的manytomany关系
        for bookobj in bookobjs: bookobj.author.add(authorobj)
        return JsonResponse({'status':0})

    # 改
    def put(self,request,*args,**kwargs):
        bookidskey = 'bookids'
        rqs = QueryDict(request.body).dict()
        pk = rqs.get('pk')
        bks = rqs.get(bookidskey)
        bks = [int(bookid) for bookid in json.loads(bks)]
        if rqs.get(bookidskey): rqs.pop(bookidskey)
        authorbookids = [bk.id for bk in self.model.objects.get(pk=pk).book_set.all()]
        diffids = list(set(authorbookids).difference(set(bks)))
        if diffids:
            for bookid in diffids:
                bkobj = self.bookmodel.objects.get(pk=bookid)
                authorobj = self.model.objects.get(pk=pk)
                authorobj.book_set.remove(bkobj)
        rqs.pop("pk")
        self.model.objects.filter(pk=pk).update(**rqs)
        return JsonResponse({'status':0})

    # 删
    def delete(self,request,*args,**kwargs):
        pk=self.kwargs.get(self.pk_url_kwarg)
        self.model.objects.get(pk=pk).delete()
        return JsonResponse({'status': 0})
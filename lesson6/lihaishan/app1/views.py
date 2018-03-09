# coding=utf8
# Create your views here.
from django.views.generic.base import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, QueryDict
from django.http.response import JsonResponse
from django.shortcuts import render
from django.conf import settings
from .models import *
import datetime
import random
import json
from django.db.models import Q
from django.forms import model_to_dict
from page import JuncheePaginator


#作者相关信息
class AuthorList(ListView):
    model = Author
    template_name = 'app1/authors.html'
    context_object_name = 'authors'
    paginate_by = 5

class AuthorApi(View):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        obj = Author.objects.get(pk=pk)
        data = obj.todict
        return JsonResponse({'status':0, 'data':data})

class AuthorDetail(DetailView):
    model = Author
    template_name = 'app1/author_detail.html'
    context_object_name = 'author1'  # 前端
    bookmodel = Book
    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        return context
    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        booksdata = webdata.get('books')
        errorinfo = []
        bookobjs = []
        for bk in json.loads(booksdata):
            try:
                obj = self.bookmodel.objects.get(name=bk)
            except self.bookmodel.DoesNotExist:
                errorinfo.append({'name':bk})
            else:
                bookobjs.append(obj)
        if errorinfo:
            return JsonResponse({'status':1,'data':errorinfo})
        webdata.pop('books')  # 字典删除书的信息
        authorobj = self.model.objects.create(**webdata)  # 写作者信息
        for bookobj in bookobjs:
            authorobj.book_set.add(bookobj)  # 写作者与书的关联关系
        return JsonResponse({'status':0})

    def put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()#接受修改后的前端数据
        print webdata
        pk = kwargs.get('pk')  #获取作者id
        bookids = webdata.get('bookids')  #获取书的id
        bkqs = Book.objects.filter(id__in=json.loads(bookids))#修改后书的qs
        print(bkqs)
        # 改作者和书的关系
        authorobj = self.model.objects.get(pk=pk)  # 作者对象
        authorobj.book_set.set(bkqs)  # 修改作者对象的书关系
        # 改作者数据
        webdata.pop('bookids')
        self.model.objects.filter(pk=pk).update(**webdata)
        return JsonResponse({'status':0})

    #获取前端修改后的信息及对应id，再获取到书的id，获取修改后的书籍信息，修改作者和书的关系，去除掉书的字段，更新作者相关信息




#书相关信息

#class BookList(ListView):
    #template_name ='app1/books.html'
    #model = Book
    #context_object_name = 'Books'
    #paginate_by = 5



class BookApi(View):
    def get(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        bobj=Book.objects.get(pk=pk)
        data=bobj.todict
        return JsonResponse({'status':0,'data':data})

class BookDetail(DetailView):
    template_name = 'app1/books.html'
    model=Book
    Authormodel=Author
    Publish=Publish
    context_object_name = 'Books1'
    search='search'


    def get_queryset(self,search):
        qs=self.model.objects.all()
        if search:
            qs=qs.filter(Q(name__contains=search)|Q(note__contains=search))
        return  qs


    #def get_context_data(self, **kwargs):
       # context=super(BookDetail,self).get_context_data(**kwargs)
       # return context

    def get(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        if pk:
            obj=self.model.objects.get(pk=pk)
            data=model_to_dict(obj,exclude=[])
            return JsonResponse({'status':0,'data':data})
        else:
            page_num=request.GET.get('page',1)
            search=request.GET.get(self.search)
            qs=self.get_queryset(search)
            pageobj=JuncheePaginator(qs)
            wdata=pageobj.pagecomputer(page_num)
            return render(request,self.template_name,{'res_data':wdata[0],'allpages':wdata[1],'search':search})


    def post(self,request,**kwargs):
        wdata=QueryDict(request.body).dict()
        authordata=wdata.get('author')#获取作者信息
        publishdata=wdata.get('publish')#获取出版社信息
        print publishdata
        #Pulishobj=Publish.objects.get(name=publishdata)
        #wdata['publish']=Pulishobj

        #作者信息
        erroinfo=[]
        authorobj=[]
        for bk in json.loads(authordata):
            try:
                obj=self.Authormodel.objects.get(name=bk)
            except self.Authormodel.DoesNotExist:
                erroinfo.append({'name':bk})
                print erroinfo
            else:
                authorobj.append(obj)
        if erroinfo:
            return JsonResponse({'status': 1, 'data':erroinfo})
        wdata.pop('author')

        #出版社信息
        puberror = []
        try:
            ob=self.Publish.objects.get(name=publishdata)
        except self.Publish.DoesNotExist:
            puberror.append({'publish': publishdata})
            print puberror
            return JsonResponse({'status': -1, 'data': puberror})
        else:
            Pulishobj = Publish.objects.get(name=publishdata) #实例出版社信息
            wdata['publish'] = Pulishobj
        bookobj=self.model.objects.create(**wdata)

        #添加作者信息
        for auth in authorobj:
            bookobj.author.add(auth)
        return JsonResponse({'status':0})



    def put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()#接受修改后的前端数据
        print webdata
        pk = kwargs.get('pk')  #获取作者id
        authors = webdata.get('authorids')  #获取作者的信息
        bkqs = Author.objects.filter(id__in=json.loads(authors))#修改后作者的qs
        print(bkqs)
        # 改作者和书的关系
        bookobj = self.model.objects.get(pk=pk)  # 书对象
        for auth in bkqs:
            bookobj.author.add(auth)
        #bookobj.book_set.set(bkqs)  # 修改书对象的作者关系
        # 改出版社数据
        webdata.pop('authorids')
        publish=webdata.get('publish')
        try:
            publishobj=Publish.objects.get(name=publish)
        except self.Publish.DoesNotExist:
            return JsonResponse({'status':2})
        else:
            webdata['publish'] = publishobj
            self.model.objects.filter(pk=pk).update(**webdata)
        return JsonResponse({'status':0})

    def delete(self, request, *args, **kwargs):
        pk=self.kwargs.get('pk')
        self.model.objects.get(pk=pk).delete()
        return JsonResponse({"status":0})




































































































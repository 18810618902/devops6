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
from app1.models import  *
import datetime
import random
import json

class AuthorList(ListView):
    model = Author
    template_name = 'app1/authors.html'
    context_object_name = 'authors'
    paginate_by = 5

class AuthorDetail(DetailView):
    model = Author
    template_name = 'app1/author_detail.html'
    context_object_name = 'author'
    bookmodel = Book
    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['timenow'] = datetime.datetime.now()
        return  context

    def post(self, request, **kwargs):
        res = {'code':0}
        webdata = QueryDict(request.body).dict()
        booksdata = webdata.get('books')
        errorinfo = []      #错误信息列表
        bookobjs = []       #存在的书列表
        # 判断书是否存在,如果存在加入书列表bookobjs,如果不存在写入errorinfo列表
        for bk in json.loads(booksdata):
            try:
                obj = self.bookmodel.objects.get(name=bk)
            except self.bookmodel.DoesNotExist:
                errorinfo.append({'name': bk})
            else:
                bookobjs.append(obj)
        #如果有错误信息说明书不存在,返回错误信息
        if errorinfo:
            return JsonResponse({'code': 1, 'data': errorinfo})

        # 删掉书的元素，写作者信息
        webdata.pop('books')
        try:
            authorobj = self.model.objects.create(**webdata)
        except  Basemodel as e:
            res['code'] = 1
            res['error']  =  '字段不合法'
        # 写作者与书的关联关系
        for bookobj in bookobjs:
            authorobj.book_set.add(bookobj)
        return JsonResponse(res)

    def put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        bookids = webdata.get('bookids')
        bkqs = Book.objects.filter(id__in=json.loads(bookids))
        print(bkqs)
        # 改作者和书的关系
        authorobj = self.model.objects.get(pk=pk)  # 作者对象
        authorobj.book_set.set(bkqs)  # 修改作者对象的书关系
        # 改作者数据
        webdata.pop('bookids')
        self.model.objects.filter(pk=pk).update(**webdata)
        return JsonResponse({'code':0})

    def delete(self, request, **kwargs):
        ret = {"code": 0}
        webdata = QueryDict(request.body).dict()
        try:
            Author.objects.get(id=webdata.get('id',"")).delete()
        except Author.DoesNotExist:
            ret = {"code": 1,"err":"User Does Not Exist "}

        return  JsonResponse(ret)




class AuthorApi(View):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        obj = Author.objects.get(pk=pk)
        data = obj.todict
        return JsonResponse({'code':0,'data':data})







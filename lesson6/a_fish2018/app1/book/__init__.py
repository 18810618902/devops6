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
from django.forms.models import model_to_dict

class BookList(ListView):
    model = Book
    template_name =  "app1/booklist.html"
    context_object_name = 'books'
    paginate_by = 5


class BookDetail(DetailView):
    model = Book
    template_name = "app1/book_detail.html"
    context_object_name = 'book'
    Publishmodel = Publish


    def post(self, request, **kwargs):
        res = {'code':0}
        webdata = QueryDict(request.body).dict()
        publishid = webdata.get('publish')
        #通过外键对象查询出出版社,修改出版社对象
        Publishobj = Publish.objects.get(id=publishid)
        webdata['publish'] = Publishobj

        #提交书籍信息
        try:
            bookrobj = self.model.objects.create(**webdata)
        except Basemodel as e:
            res['code'] = 1
            res['error'] = "书籍添加错误,请联系管理员"
        return  JsonResponse(res)

    def put(self, request, **kwargs):
        res = {'code':0}
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')

        #通过publishid  获取publish对象
        publishid = webdata.get('publish')
        Publishobj = Publish.objects.get(id=publishid)

        #重新赋值publish对象,通过bookid更新书籍信息
        webdata['publish'] = Publishobj
        try:
            self.model.objects.filter(pk=pk).update(**webdata)
        except Basemodel as e:
            res['code'] = 1
            res['error'] = "修改错误请联系管理员"
        return JsonResponse(res)

    def  delete(self, request, **kwargs):
        res = {'code':0}
        webdata = QueryDict(request.body).dict()
        try:
            self.model.objects.filter(pk=webdata.get('id',"")).delete()
        except Basemodel as e:
            res['code']  = 1
            res['error'] = "删除错误请联系管理员"
        return JsonResponse(res)




class BookApi(View):
    def get(self, request, **kwargs):
        Publish_obj = Publish.objects.all()
        Publish_list = (list(Publish_obj.values("id", "name")))
        return JsonResponse({'code':0,'data':Publish_list})
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


class PublishList(ListView):
    model = Publish
    template_name =  "app1/publishlist.html"
    context_object_name = 'publishs'
    paginate_by = 5

class PublishDetail(DetailView):
    model = Publish
    template_name = "app1/publish_detail.html"
    context_object_name = 'publishs'
    Bookmodel = Book

    def post(self, request, **kwargs):
        res = {'code':0}
        webdata = QueryDict(request.body).dict()
        try:
            publishrobj = self.model.objects.create(**webdata)
        except Basemodel  as e:
            res['code'] = 1
            res['error'] = "出版社添加错误"

        return  JsonResponse(res)
    def put(self, request, **kwargs):
        res = {'code':0}
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        try:
            publishrobj = self.model.objects.filter(pk=pk).update(**webdata)
        except Basemodel  as e:
            res['code'] = 1
            res['error'] = "出版社修改错误"

        return  JsonResponse(res)



    def  delete(self, request, **kwargs):
        res = {'code':0}
        webdata = QueryDict(request.body).dict()
        #通过出版社对象查所在该出版社的书籍，如果有关联书籍不可以删除，没有关联书籍可以删除
        try:
            Publishobj = Publish.objects.get(pk=webdata.get('id',""))
            if  not   Publishobj.book_set.all():
                self.model.objects.filter(pk=webdata.get('id',"")).delete()
            else:
                res['code'] = 1
                res['error'] = "该出版社有关联书籍,请联系管理员"
        except Basemodel as e:
            res['code'] = 1
            res['error'] = "删除错误请联系管理员"
        return JsonResponse(res)



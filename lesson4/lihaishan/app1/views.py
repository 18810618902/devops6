# coding=utf8
# Create your views here.
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, QueryDict
from django.http.response import JsonResponse
from django.shortcuts import render
from django.conf import settings
from .models import *
import json
from django.db.models import Q
from django.forms import model_to_dict
from page import JuncheePaginator



class authorapi(View):
    pk_url_kwarg = 'pk'
    model = Author

    def get(self, request, *args, **kwargs):
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
            qslist = list(set(qsincome).union(set(qsfansnum)))  # queryset并集并去重（可切片），得到的是list
            data = [i.todict for i in qslist]
            ret = {}
            ret['data'] = data
            ret['status'] = 0
            return JsonResponse(ret)




class authordetail(LoginRequiredMixin, View):
    model = Author
    bookmodel = Book
    template_name='app1/authors.html'
    context_object_name = 'authors'
    pk_url_kwarg = 'pk'
    search = 'search'

    def get_queryset(self,search):   # 数据库查询的结果
        qs=self.model.objects.all()
        if search:
            qs=qs.filter(Q(name__contains=search)|Q(note__contains=search))
        return qs

    def get(self,request,*args,**kwargs):
        pk=kwargs.get(self.pk_url_kwarg)
        if pk:
            obj=self.model.objects.get(pk=pk)
            data=model_to_dict(obj,exclude=[])
            return JsonResponse({'statue':0,'data':data})
        else:
            page_num=request.GET.get('page',1)   # 请求的第几页
            search=request.GET.get(self.search)  #搜索项
            qs=self.get_queryset(search)  #返回查找出所有数据（QuerySet）
            pageobj=JuncheePaginator(qs)
            wdata=pageobj.pagecomputer(page_num)
            print request.path
            print wdata
            return render(request,self.template_name,{'res_data':wdata[0],'allpages':wdata[1],'search':search})


    def post(self, request, *args, **kwargs):
        # 接受前端的数据
        rqs = QueryDict(request.body).dict()
        print request.body
        rqsbooks = rqs['books']
        books = [book.strip() for book in json.loads(rqsbooks)]  #json.dumps是将一个Python数据类型列表进行json格式的编码解析;json.loads解码python json格式
        # 判断数在不在数据库，在的话存数据，不在返回错误信息
        errorinfo = []
        bookobjs = []
        for book in books:
            try:
                bookobj = self.bookmodel.objects.get(name=book)
            except self.bookmodel.DoesNotExist:
                errorinfo.append({'name': book})
            else:
                bookobjs.append(bookobj)
        if errorinfo:
            return JsonResponse({'status': -1, 'data': errorinfo})
        ##### 写除了书以外的字段
        rqs.pop('books')
        authorobj = self.model.objects.create(**rqs)
        #### 写作者和书的manytomay关系
        for bookobj in bookobjs:
            bookobj.author.add(authorobj)
        return JsonResponse({'status': 0})

    def put(self, request, *args, **kwargs):
        # rqs = request.PUT.get('name')
        bookidskey = 'bookids'
        pk = self.kwargs.get(self.pk_url_kwarg)
        rqs = QueryDict(request.body).dict() #接受修改后的前端数据
        print rqs
        bks = rqs.get(bookidskey)
        bks = [int(bookid) for bookid in json.loads(bks)]
        if rqs.get(bookidskey):
            rqs.pop(bookidskey)  # 从字典里删除bookids，为后面修改作者数据准备
        authorbookids = [bk.id for bk in self.model.objects.get(pk=pk).book_set.all()] #获取修改前作者的书籍id
        print authorbookids
        diffids = list(set(authorbookids).difference(set(bks)))  # 求作者的书 和前端传来的书 的差集
        # 删除作者的diffids书关联
        if diffids:
            for bookid in diffids:
                bkobj = self.bookmodel.objects.get(pk=bookid)
                authorobj = self.model.objects.get(pk=pk)
                authorobj.book_set.remove(bkobj)
        # self.model.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg)).update(**QueryDict(request.body).dict())
        self.model.objects.filter(pk=self.kwargs.get(self.pk_url_kwarg)).update(**rqs)  # 修改其它字段信息
        return JsonResponse({'status': 0})

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        self.model.objects.get(pk=pk).delete()
        return JsonResponse({'status': 0})
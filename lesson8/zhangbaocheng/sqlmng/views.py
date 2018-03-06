# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View,ListView,DetailView,TemplateView
from django.http import JsonResponse, QueryDict
import inception
from django.shortcuts import render
from .models import *
from .pagerange  import get_pagerange
from django.core.paginator import  Paginator, PageNotAnInteger ,EmptyPage
from django.db.models import Q
from django.contrib.auth.mixins import  LoginRequiredMixin

# Create your views here.



class inception_commit(LoginRequiredMixin,TemplateView):
    model = dbconf
    template_name = 'sqlmng/inception_commit.html'
    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        username = request.user.get_username()
        #inc11321eption.table_structure(webdata['sqlcontent'])
        #dbname, env, sqlcontent, note
        #通过前端的数据，拼接目标地址
        obj  = self.model.objects.get(name=webdata.get('dbname'))
        dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s' % (obj.user, obj.password, obj.host, obj.port)
        sql_review = inception.table_structure(dbaddr, obj.name, webdata['sqlcontent'])
        for perrz in sql_review:
            if perrz[4] != 'None':
                print(perrz[4])
                return JsonResponse({'status':-2, 'msg':perrz[4]})

        #保存正常的SQL
        print(sql_review)
        userobj = User.objects.get(username=request.user)
        webdata['commiter'] = username
        webdata['treater'] = username
        sqlobj = InceptSql.objects.create(**webdata)
        sqlobj.sqlusers.add(userobj)
        return JsonResponse({'status':0})



class  dbconfig(LoginRequiredMixin,TemplateView,get_pagerange):
    model = dbconf
    template_name = 'sqlmng/dbconfig.html'
    per = 10
    paginate_by = 10
    befor_range_num = 5
    after_range_num = 5

    def get_context_data(self, **kwargs):
        context = super(dbconfig, self).get_context_data(**kwargs)
        search = self.request.GET.get("search_data", None)                #获取搜索字段数据
        page_num = int(self.request.GET.get("page",1))                    #获取page id

        if search:
            obj_list = dbconf.objects.filter(Q(name__contains=search)|Q(host__contains=search)|Q(port__contains=search)|Q(user__contains=search)) #取搜索字段
        else:
            obj_list = dbconf.objects.all().order_by('id')

        paginator = Paginator(obj_list,self.per)
        pages_nums = paginator.num_pages #总分页数
        # 处理搜索条件

        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except BaseException as  e:
            pass
        context.update(search_data.dict())
        context['search_data'] = search_data.urlencode()

        try:
            context['page_obj'] = paginator.page(page_num)
        except PageNotAnInteger: #返回第一页数据
            context['page_obj'] = paginator.page(1)
        except EmptyPage:        #返回最后一页数据
            context['page_obj'] = paginator.page(pages_nums)

        context['page_range'] = self.get_pageranges(context["page_obj"]) #page_range分页列表数据
        context['object_list'] = context['page_obj'].object_list         #页面数据
        return  context

    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        name=webdata.get('name')
        env=webdata.get('env')
        dbqs=self.model.objects.filter(name=name,env=env)
        if dbqs:
            return JsonResponse({'status':-1})
        self.model.objects.create(**webdata)
        return JsonResponse({'status':0})


    def  put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        print(webdata)
        pk = kwargs.get('pk')
        self.model.objects.filter(pk=pk).update(**webdata)
        return JsonResponse({'status': 0})
    def delete(self,request, **kwargs):
        pk = kwargs.get('pk')
        self.model.objects.get(pk=pk).delete()
        return   JsonResponse({'status': 0})


class autoselect(LoginRequiredMixin,View):
    def post(self, request):
        webdata = QueryDict(request.body).dict()
        env = webdata.get('env')
        qs = dbconf.objects.filter(env=env)
        dbs = [obj.name for obj in qs]
        return  JsonResponse({'status': 0,'data':dbs})
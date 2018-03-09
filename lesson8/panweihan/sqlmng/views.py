# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View,ListView,DetailView,TemplateView
from django.http import JsonResponse, QueryDict
import inception
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(login_required, name='dispatch')
# 审查SQL语句，并将数据添加到SQL上线列表
class inception_commit(TemplateView):
    template_name = 'sqlmng/inception_commit.html'
    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        dbqs = dbconf.objects.filter(name=webdata['name'], env=webdata['env'])
        sqltext = inception.table_structure('check',webdata['sqlcontent'],dbqs[0])
        ret = {}
        message = []
        for i in sqltext:
            # 语句有错误，保存报错信息
            if i[2] != 0:
                x = []
                x.append(i[5])
                x.append(i[4])
                message.append(x)
                ret['errormessage'] = message
                ret['status'] = -1
            # 语句合法，读取用户名、语句等信息
            else:
                ret['status'] = 0
                userobj = self.request.user
                webdata['username'] = userobj.first_name
                webdata['sqlcontent'] = webdata['sqlcontent'].lower()
        # 保存信息到数据库
        print ret
        if ret['status'] == 0:
            sqlconf.objects.create(**webdata)
        return JsonResponse(ret)

# SQL上线列表
class inception_list(ListView):
    template_name = 'sqlmng/inception_list.html'
    context_object_name = 'res_data'
    paginate_by = 10
    model = sqlconf

    # 获取语句详情/执行数据库语句
    def post(self,request,**kwargs):
        pk = kwargs.get('pk')
        webdata = QueryDict(request.body).dict()
        sqlobj = self.model.objects.get(pk=pk)
        # 获取语句详情
        if webdata['todo'] == 'details':
            data = sqlobj.sqlcontent
            return JsonResponse({'status':0,'data':data})
        # 备注详情
        elif webdata['todo'] == 'note':
            data = sqlobj.note
            return JsonResponse({'status': 0, 'data': data})
        # 执行SQL语句
        else:
            # 获取数据库服务器信息
            dbqs = dbconf.objects.filter(name=sqlobj.name, env=sqlobj.env)
            # 执行SQL语句
            incobj = inception.table_structure('execute', sqlobj.sqlcontent,dbqs[0])
            affected_rows = 0
            execute_time = 0
            for i in incobj:
                affected_rows += int(i[6])
                execute_time += float(i[9])
            # 修改状态,写入SQL语句额外参数
            self.model.objects.filter(id=pk).update(operate=3,condtion=2)
            backid = ''
            for i in incobj:
                if i[3] == "Execute Successfully\nBackup successfully":
                    backid += "%s,"%i[7]
            self.model.objects.filter(pk=pk).update(backdb= i[8],backid=backid)
            return JsonResponse({'status':0,'execute_time':execute_time,'affected_rows':affected_rows})

    # 回滚
    def put(self, request, **kwargs):
        pk = kwargs.get('pk')
        sqlobj = self.model.objects.get(pk=pk)  # 获取SQL列表对象
        dbqs = dbconf.objects.filter(name=sqlobj.name, env=sqlobj.env)  # 获取数据库配置的对象
        # 将读出的ID（字符串格式）转成列表
        bkids = sqlobj.backid.split(',')
        # 因为ID的字符串结尾是逗号，转换后会生成一个空字符，因此用remove做下处理
        while '' in bkids:
            bkids.remove('')
        # 获取回滚语句
        affected_rows = 0
        execute_time = 0
        for backid in bkids:
            rollback = inception.rollbackdb(sqlobj.backdb,backid)
            # 执行回滚
            for i in rollback:
                incobj = inception.table_structure('execute',i[0], dbqs[0])
                for i in incobj:
                    affected_rows += int(i[6])
                    execute_time += float(i[9])
        self.model.objects.filter(pk=pk).update(operate=0, condtion=4)
        return JsonResponse({'status': 0, 'execute_time': execute_time, 'affected_rows':affected_rows})

    # 拒绝
    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update(operate=0, condtion=3,)
        return JsonResponse({'status':0})

@method_decorator(login_required, name='dispatch')
class dbconfig(ListView):
    model = dbconf
    template_name = 'sqlmng/dbconfig.html'
    paginate_by = 5
    context_object_name = 'res_data'

    def get_queryset(self):
        qs = self.model.objects.all()
        souword = self.request.GET.get('souword')
        if souword:
            qs = qs.filter(name__contains=souword)
        return qs

    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        name = webdata.get('name')
        env = webdata.get('evn')
        dbqs = self.model.objects.filter(name=name,env=env)
        if dbqs:
            return JsonResponse({'status':-1})
        self.model.objects.create(**webdata)
        return JsonResponse({'status':0})

    def put(self,request,**kwargs):
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        self.model.objects.filter(pk=pk).update(**webdata)
        return JsonResponse({'status': 0})

    def delete(self,request,**kwargs):
        pk = kwargs.get('pk')
        self.model.objects.get(pk=pk).delete()
        return JsonResponse({'status': 0})

@method_decorator(login_required, name='dispatch')
class autoselect(View):
    def post(self,request):
        webdata = QueryDict(request.body).dict()
        env = webdata.get('env')
        dbs = [obj.name for obj in dbconf.objects.filter(env=env)]
        use = [obj.first_name for obj in User.objects.filter(last_name=env)]
        useobj = self.request.user
        # if useobj.first_name in use:
        #     use.remove(useobj.first_name)
        return JsonResponse({'status':0,'data':dbs,'usename':use})

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View,ListView,DetailView,TemplateView
from django.http import JsonResponse, QueryDict
import inception
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

import dbcrypt

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
# 审查SQL语句，并将数据添加到SQL上线列表
class inception_commit(TemplateView):
    template_name = 'sqlmng/inception_commit.html'
    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        dbqs = dbconf.objects.filter(name=webdata['dbname'], env=webdata['env'])
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
                webdata['commiter'] = userobj.first_name
                webdata['user_obj'] = userobj
                webdata['sqlcontent'] = webdata['sqlcontent'].lower()
        # 保存信息到数据库
        if ret['status'] == 0:
            sqlconf.objects.create(**webdata)
        return JsonResponse(ret)

# SQL语句列表
class inception_list(ListView):
    template_name = 'sqlmng/inception_list.html'
    context_object_name = 'res_data'
    paginate_by = 10
    model = sqlconf

    # 依据职位权限显示数据
    def get_context_data(self, **kwargs):
        context = super(inception_list, self).get_context_data(**kwargs)
        userobj = self.request.user
        groupque = userobj.groups.all()
        # 超级管理员能看所有记录
        if userobj.is_superuser:
            context['res_data'] = sqlconf.objects.all()
        # 经理级以上人员能看自己和下属记录
        elif int(userobj.userprofile.role) < 3 and int(userobj.userprofile.role) != 0:
            sqlque = userobj.sqlconf_set.all()   # 通过多对一关系获取SQL语句
            for groupobj in groupque:
                userque = groupobj.user_set.all()  # 获取组内用户集合(QuerySet)
                for u_obj in userque:
                    if int(u_obj.userprofile.role) > int(userobj.userprofile.role) and int(userobj.userprofile.role) != 0:
                        sqlque = sqlque | u_obj.sqlconf_set.all()   # 合并自己和下属的SQL语句
            context['res_data'] = sqlque
        # 研发和无岗位人员只能看自己的记录
        elif int(userobj.userprofile.role) >= 3 or int(userobj.userprofile.role) == 0:
            context['res_data'] = userobj.sqlconf_set.all()
        return context

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
        elif webdata['todo'] == 'pause':
            sqlobj.condtion = -2
            sqlobj.save()
            return JsonResponse({'status': 0})
        # 执行SQL语句
        else:
            # 获取数据库服务器信息
            dbqs = dbconf.objects.get(name=sqlobj.dbname, env=sqlobj.env)
            # 执行SQL语句
            incobj = inception.table_structure('execute',sqlobj.sqlcontent,dbqs)
            message = []
            ret = {}
            affected_rows = 0
            execute_time = 0
            rollbackopid = ''
            for i in incobj:
                print i
                # 执行失败
                if i[4] != 'None':
                    x = []
                    x.append(i[5])
                    x.append(i[4])
                    message.append(x)
                    ret['errormessage'] = message
                    ret['status'] = -1
                    sqlobj.condtion = 2
                    sqlobj.save()
                    return JsonResponse(ret)
                    break
                # 执行、备份成功
                elif i[3] == "Execute Successfully\nBackup successfully":
                    print 1111
                    rollbackopid += "%s," % i[7]
                    affected_rows += int(i[6])
                    execute_time += float(i[9])
                    self.model.objects.filter(pk=pk).update(condtion = 0)
                else:
                    affected_rows += int(i[6])
                    execute_time += float(i[9])
            self.model.objects.filter(pk=pk).update(backdb=i[8], rollbackopid=rollbackopid)
            if webdata['treater'] != request.user.first_name:
                self.model.objects.filter(pk=pk).update(daiwork = request.user.first_name)
                # sqlobj.daiwork = request.user.first_name
                # sqlobj.save()
            ret['status'] = 0
            ret['execute_time'] =execute_time
            ret['affected_rows'] =affected_rows
            return JsonResponse(ret)

    # 回滚
    def put(self, request, **kwargs):
        pk = kwargs.get('pk')
        sqlobj = self.model.objects.get(pk=pk)  # 获取SQL列表对象
        dbqs = dbconf.objects.filter(name=sqlobj.dbname, env=sqlobj.env)  # 获取数据库配置的对象
        # 将读出的ID（字符串格式）转成列表
        bkids = sqlobj.rollbackopid.split(',')
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
                print incobj
                for i in incobj:
                    affected_rows += int(i[6])
                    execute_time += float(i[9])
        self.model.objects.filter(pk=pk).update(condtion=-3)
        return JsonResponse({'status': 0, 'execute_time': execute_time, 'affected_rows':affected_rows})

    # 拒绝
    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        self.model.objects.filter(id=pk).update( condtion=1,)
        return JsonResponse({'status':0})

@method_decorator(login_required, name='dispatch')
class dbconfig(ListView):
    model = dbconf
    template_name = 'sqlmng/dbconfig.html'
    paginate_by = 5
    context_object_name = 'res_data'
    # mipasswd = dbcrypt('abcdabcdabcd')

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
        # webdata['password'] = self.mipasswd.encrypt(webdata['password'])
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

# 主页单选按钮
@method_decorator(login_required, name='dispatch')
class autoselect(View):
    def post(self,request):
        webdata = QueryDict(request.body).dict()
        env = webdata.get('env')
        dbs = [obj.name for obj in dbconf.objects.filter(env=env)]
        userobj = self.request.user
        groupque = userobj.groups.all()
        if env == '2':
            use = [userobj.first_name]
        else:
            # 获取当前用户直属领导中文名,没有领导的获取当前用户的中文名
            use = []
            for groupobj in groupque:
                userque = groupobj.user_set.all()  # 获取组内用户QuerySet集合
                for u_obj in userque:
                    if int(u_obj.userprofile.role) == int(userobj.userprofile.role) - 1:
                        use.append(u_obj.first_name)
            if len(use) == 0:
                use = [userobj.first_name]
        return JsonResponse({'status':0,'data':dbs,'usename':use})


class inc_show(TemplateView):
    template_name = "sqlmng/inc_show.html"
    def get_context_data(self, **kwargs):
        context = super(inc_show, self).get_context_data(**kwargs)
        inc_test = inception.inc_show('inc_test')
        inc_test2 = inception.inc_show('inc_test2')
        context['inc_test'] = inc_test
        context['inc_test2'] = inc_test2
        return context
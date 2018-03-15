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
from django.contrib.auth.models import  User
# Create your views here.
from  dbcrypt import  prpcrypt

saltpwd = prpcrypt('98b85629951ad584')


class inception_commit(LoginRequiredMixin,TemplateView):
    model = dbconf
    template_name = 'sqlmng/inception_commit.html'
    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        print(webdata)
        username = request.user.get_username()
        #inc11321eption.table_structure(webdata['sqlcontent'])
        #dbname, env, sqlcontent, note
        #通过前端的数据，拼接目标地址
        obj  = self.model.objects.get(Q(name=webdata.get('dbname')) & Q(env=webdata.get('env')))
        dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s' % (obj.user, saltpwd.decrypt(obj.password), obj.host, obj.port)
        sql_review = inception.table_structure(dbaddr, obj.name, webdata['sqlcontent'])
        for perrz in sql_review:
            if perrz[4] != 'None':
                print(perrz[4])
                return JsonResponse({'status':-2, 'msg':perrz[4]})

        #保存正常的SQL
        print(sql_review)
        userobj = User.objects.get(username=request.user)
        webdata['commiter'] = username
        sqlobj = InceptSql.objects.create(**webdata)
        treaterobj = User.objects.get_or_create(username=webdata['treater'])[0]
        sqlobj.sqlusers.add(userobj,treaterobj)         #绑定提交人

        return JsonResponse({'status':0})



class  dbconfig(LoginRequiredMixin,TemplateView,get_pagerange,prpcrypt):
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
        print(webdata)
        name=webdata.get('name')
        env=webdata.get('env')
        dbqs=self.model.objects.filter(name=name,env=env)
        if dbqs:
            return JsonResponse({'status':-1})
        # 加密密码字段
        webdata['password'] = saltpwd.encrypt(webdata['password'])
        self.model.objects.create(**webdata)
        return JsonResponse({'status':0})

    def  put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        db_obj = dbconf.objects.get(pk=pk)

        #判断密码是否被修改,被修改则加密密码,没被修改则直接提交密码
        if db_obj.password  == webdata['password']:
            self.model.objects.filter(pk=pk).update(**webdata)
        else:
            webdata['password'] = saltpwd.encrypt(webdata['password'])
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

        #如果超级管理员账号,执行人返回自己
        userobj = request.user
        if userobj.is_superuser:
            mngs =[userobj.username]
            return JsonResponse({'status': 0, 'data': dbs, 'mngs': mngs})

        #1.)根据用户身份返回执行人数据： 研发 返回研发经理，经理返回经理以上返回自己的数据
        role  = userobj.userprofile.role

        #2.)根据环境判断,生产环境执行人为上级领导, 测试环境执行人为自己
        if env == '1':

            #3.)根据角色判断，如果是研发人员，返回研发人员所在分组经理
            if role == '3':
                ug = userobj.groups.first()

                #4.)如果没有上级返回空
                if not ug:
                    mngs = []
                else:
                    mngs = [u.username for u in ug.user_set.all() if u.userprofile.role == '2']
            else:
                mngs = [userobj.username]
        else:
            mngs = [userobj.username]

        return  JsonResponse({'status': 0,'data':dbs,'mngs':mngs})


class  inception_result(LoginRequiredMixin, ListView):
    template_name = 'sqlmng/inception_result.html'
    paginate_by = 10
    model = InceptSql
    dbmodel = dbconf
    context_object_name = 'res_data'

    def get_queryset(self):

        #1.)根据用户身份，返回和他有关系的sql
        userobj = self.request.user
        #2.)如果是超级管理员,返回所有sql
        if userobj.is_superuser:
            return self.model.objects.all()


        role = userobj.userprofile.role
        #3.)总监，返回他组内的所有人的sql
        if role == '1':
            qs = userobj.inceptsql_set.all()
            g = userobj.groups.first()
            for u in g.user_set.all():
                sqlret = u.inceptsql_set.all()
                qs = qs | sqlret

        #4.)研发或经理
        else:
            qs = userobj.inceptsql_set.all()
        return qs


    def  post(self, request, **kwargs):
        pk = kwargs.get('pk')
        actiontype = kwargs.get('actiontype')
        sqlobj = self.model.objects.get(pk=pk)
        ret  = {'status': 0}
        if  actiontype == 'execute':
            #根据id获取SQL的内容
            sqlcontent = sqlobj.sqlcontent
            dbobj = self.dbmodel.objects.get(Q(name=sqlobj.dbname) & Q(env=sqlobj.env))
            dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-execute' % (dbobj.user, saltpwd.decrypt(dbobj.password), dbobj.host, dbobj.port)
            print(saltpwd.decrypt(dbobj.password))
            exerz = inception.table_structure(dbaddr, dbobj.name, sqlcontent)  # 这里执行SQL语句
            print(exerz)
            affected_rows = 0    #影响行数
            execute_time = 0     #执行时间
            opidlist = []        #回滚id列表

            for i in exerz:            # 分析执行完的结果
                successcode = i[4]
                if successcode != 'None':  #执行失败的
                    sqlobj.status = 2
                    ret['status'] = -1
                    ret['msg'] =  i[4]
                    sqlobj.executerz =  i[4]
                    break
                else:                             #执行成功修改状态为已执行
                    opidlist.append(i[7])
                    affected_rows += 1
                    execute_time += float(i[9])
                    sqlobj.rollbackdb = i[8]
                    sqlobj.status = 0
                    sqlobj.exe_affected_rows = affected_rows
                    ret['status'] = 0
                    ret['affected_rows'] = affected_rows
                    ret['execute_time'] = execute_time
                    ret['Warning'] =  ''
            sqlobj.rollbackopid = opidlist



        elif actiontype == 'rollback':
            affected_rows = 0    #影响行数
            # 第一步：获取回滚语句
            rollbackopid  = sqlobj.rollbackopid   #取出回滚id列表
            rollbackdb = sqlobj.rollbackdb        #取出回滚库名
            backsqls = ''
            for opid in eval(rollbackopid)[1:]:   # 遍历回滚id，拼接回滚语句
                #1.)通过opid 备份库名, 查出备份库,备份表名
                sql = 'select tablename from $_$Inception_backup_information$_$ where opid_time = %s' % (opid)
                baktable = inception.getbak(sql, rollbackdb)[0][0]

                #2.)通过opid 及备份库表名查出回滚语句集合
                rollbacksql = 'select rollback_statement from %s where opid_time = %s' % (baktable, opid)
                perback = inception.getbak(rollbacksql, rollbackdb)
                '''
                ((u'DELETE FROM `inc_test2`.`mytable1` WHERE id=38;',),) 
                '''

                #3.) 循环回滚语句集合,拼接成一个字符串
                for baksql in perback:
                    backsqls += baksql[0]

            #第二步: 执行回滚语句
            dbobj = self.dbmodel.objects.get(Q(name=sqlobj.dbname) & Q(env=sqlobj.env))
            dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-execute' % (dbobj.user,saltpwd.decrypt(dbobj.password), dbobj.host, dbobj.port)
            try:
                #1.)执行回滚语句
                exerz = inception.table_structure(dbaddr, dbobj.name, backsqls)
                for i in exerz:               # 分析执行完的结果
                    successcode = i[4]
                    if successcode == 'None':  #回滚成功
                        sqlobj.status = -3
                        affected_rows += 1
                        sqlobj.roll_affected_rows   = affected_rows
                        ret['status'] = 0
                        ret['rollnum'] = affected_rows
            except  Basemodel as  e:
                print(e)
                ret['status'] = 3

        elif actiontype == 'pause':
            pk = kwargs.get('pk')
            actiontype = kwargs.get('pause')
            sqlobj = self.model.objects.get(pk=pk)
            sqlobj.status = -2

        elif actiontype == 'cancelpause':
            pk = kwargs.get('pk')
            actiontype = kwargs.get('pause')
            sqlobj = self.model.objects.get(pk=pk)
            sqlobj.status = -1

        elif actiontype == 'reject':
            pk = kwargs.get('pk')
            actiontype = kwargs.get('reject')
            sqlobj = self.model.objects.get(pk=pk)
            sqlobj.status = 1

        sqlobj.save()
        return  JsonResponse(ret)


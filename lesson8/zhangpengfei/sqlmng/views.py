# -*- coding: utf-8 -*-

from django.views.generic import View,ListView,DetailView,TemplateView
from django.http import JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import inception
from django.shortcuts import render
from .models import *
import pymysql
# Create your views here.

@method_decorator(login_required, name='dispatch')
class inception_commit(TemplateView):
    template_name = 'sqlmng/inception_commit.html'
    model = dbconf
    def post(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        username = request.user.get_username()
        print(webdata)
        # inception.table_structure(webdata['sqlcontent'])
        # 通过前端的数据 dbname, env, sqlcontent, note，拼接目标地址
        # --user=root;--password=123456;--host=192.168.1.233;--port=3306
        obj = self.model.objects.get(name=webdata.get('dbname'),env=webdata.get('env'))
        dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s; --enable-check;' % (obj.user, obj.password, obj.host, obj.port)
        sql_review = inception.table_structure(dbaddr, obj.name, webdata['sqlcontent'])
        for perrz in sql_review:
            if perrz[4] != 'None':
                return JsonResponse({'status':-2, 'msg':perrz[4]})
        # check通过的sql，保存
        userobj = User.objects.get(username=request.user)
        webdata['commiter'] = username
        webdata['treater'] = username
        sqlobj = InceptSql.objects.create(**webdata)
        sqlobj.sqlusers.add(userobj)
        print(sql_review)
        return JsonResponse({'status':0})

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
        env = webdata.get('env')
        # 判断name env 的数据是不重复的
        dbqs = self.model.objects.filter(name=name,env=env)
        if dbqs:
            return JsonResponse({'status':-1})
        self.model.objects.create(**webdata)
        return JsonResponse({'status':0})

    def put(self, request, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = kwargs.get('pk')
        print(webdata, pk)
        self.model.objects.filter(id=pk).update(**webdata)
        return JsonResponse({'status': 0})

    def delete(self, request, **kwargs):
        pk = kwargs.get('pk')
        self.model.objects.get(pk=pk).delete()
        return JsonResponse({'status': 0})

class autoselect(View):
    def post(self, request):
        webdata = QueryDict(request.body).dict()
        env = webdata.get('env')
        dbs = [obj.name for obj in dbconf.objects.filter(env=env) ]
        return JsonResponse({'status': 0, 'data':dbs})


class dbexe(ListView):
    template_name = 'sqlmng/t2.html'
    model = InceptSql
    paginate_by = 10
    context_object_name = 'res_data'

    def post(self, request,**kwargs):
        pk = kwargs.get('pk')
        obj_sql = self.model.objects.get(pk=pk)
        print(obj_sql.dbname,obj_sql.env)
        obj_db = dbconf.objects.get(name=obj_sql.dbname,env=obj_sql.env)
        print(obj_db)
        print(obj_sql)
        dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s;--enable-execute;' % (obj_db.user, obj_db.password, obj_db.host,obj_db.port)
        sql_review = inception.table_structure(dbaddr, obj_db.name, obj_sql.sqlcontent)
        for perrz in sql_review:
            if perrz[4] != 'None':
                return JsonResponse({'status':-2, 'msg':perrz[4]})
        obj_sql.status=0
        obj_sql.rollbackopid = sql_review[1][7]
        obj_sql.save()

        print(sql_review)
        return JsonResponse({'status': 0})

class dbrollback(View):

    def post(self, request,**kwargs):
        webdata = QueryDict(request.body).dict()
        pk = webdata['id']
        ## 获取要回滚的库名
        dbname = webdata['dbname']
        # 获取要回滚的表名
        obj_sql = InceptSql.objects.get(pk=pk)
        conn=pymysql.connect(host='127.0.0.1',user='root',passwd='123456',db='127_0_0_1_3306_' + dbname,port=3306)
        cur=conn.cursor()
        sql = 'select tablename from $_$Inception_backup_information$_$ where opid_time=%s;' %  obj_sql.rollbackopid
        cur.execute(sql)
        result=cur.fetchone()
        tablename = result[0]
        # 获取回滚sql
        sql = 'select rollback_statement from %s  where opid_time=%s;' % ( tablename, obj_sql.rollbackopid)
        cur.execute(sql)
        result=cur.fetchall()
        cur.close()
        conn.close()
        print(sql)
        print(result)
        rel = ''
        for r in result:
            rel += r[0]
        print(rel)
        ## 获取数据库账号密码
        obj_db = dbconf.objects.get(name=obj_sql.dbname,env=obj_sql.env)
        print(obj_db)
        print(obj_sql)
        dbaddr = '--user=%s; --password=%s; --host=%s; --port=%s;--enable-execute;' % (obj_db.user, obj_db.password, obj_db.host,obj_db.port)
        print(dbaddr)
        ## rollback
        sql_review = inception.table_structure(dbaddr, obj_db.name, rel)
        print(sql_review)
        obj_sql.status=-3 #标记为回滚
        obj_sql.save()
        return JsonResponse({'status': 0})

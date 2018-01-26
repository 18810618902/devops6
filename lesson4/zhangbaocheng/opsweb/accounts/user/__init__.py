#coding:utf-8
from  django.views.generic import  View,ListView, TemplateView
from django.shortcuts import render
from django.contrib.auth.models import  User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.http import  HttpResponse, JsonResponse, QueryDict
from  django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  permission_required, login_required
from django.core.paginator import  Paginator, PageNotAnInteger ,EmptyPage
from django.db.models import Q





class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'user/userlist.html'
    per = 10
    befor_range_num = 5
    after_range_num = 5
    ordering = "id"


    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search_data", None)                #获取搜索的用户名
        page_num = int(self.request.GET.get("page",1))                    #获取page id

        if search:
            user_list = User.objects.filter(Q(username__contains=search)|Q(email__contains=search) |Q(last_name__contains=search)) #取搜索数据
        else:
            user_list = User.objects.filter(is_superuser=False)           #过滤超级管理员账号

        paginator = Paginator(user_list,self.per)
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

        context['page_range'] = self.get_pagerange(context["page_obj"]) #page_range分页列表数据
        context['object_list'] = context['page_obj'].object_list        #用户数据
        return  context


    def get_pagerange(self, page_obj):
       current_index = page_obj.number
       start = current_index - self.befor_range_num
       end = current_index + self.after_range_num
       if start <= 0 :
           start = 1
       if end >=  page_obj.paginator.num_pages:
           end = page_obj.paginator.num_pages

       return range(start, end+1)




class ModifyUserView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        ret = {"code":0}
        try:
            User_obj = User.objects.create(**QueryDict(request.body).dict())

        except IntegrityError as e:
            ret = {"code": 1,"msg":"该用户已存在"}
        except  Exception as e:
            ret = {"code": 1, "msg": "未知错误请联系管理员"}
        return JsonResponse(ret)

    def delete(self, request, *args, **kwargs):
        ret = {"code": 0}
        try:
            idc_obj = User.objects.get(pk=QueryDict(request.body)['id']).delete()
        except User.DoesNotExist:
            ret = {"code": 1,"errmsg":"用户不存在"}
        return JsonResponse(ret)

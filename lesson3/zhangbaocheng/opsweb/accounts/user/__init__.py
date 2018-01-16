#coding:utf-8
from  django.views.generic import  View,ListView
from django.shortcuts import render
from django.contrib.auth.models import  User,Group
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.http import  HttpResponse, JsonResponse, QueryDict
from  django.db import IntegrityError
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  permission_required, login_required



class UserListView(LoginRequiredMixin, ListView):
    template_name = "user/userlist.html"
    model = User
    paginate_by = 10
    ordering = "id"

    def  get_queryset(self):
        queryset =  super(UserListView, self).get_queryset()
        queryset = queryset.filter(is_superuser=False)
        username = self.request.GET.get("search_username", None)
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset


class UserAddView(LoginRequiredMixin, View):
    def post(self, request):
        data = (request.POST.dict())
        ret = {"code":0}
        try:
            User_obj = User.objects.create_user(username=data['username'],
                                              last_name=data['last_name'],
                                              password=data['password'],
                                              email=data['email'],
                                               )
        except IntegrityError as e:
            ret = {"code": 1,"msg":"该用户已存在"}
        except  BaseException as e:
            ret = {"code": 1, "msg": "未知错误请联系管理员"}
        return JsonResponse(ret)

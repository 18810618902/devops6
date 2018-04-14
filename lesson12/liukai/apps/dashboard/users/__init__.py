#! /usr/bin/env python
# encoding: utf8

"""
@Author: liukai
@Date: 2018/3/26
"""
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.hashers import make_password

from django.conf import settings
from dashboard.models import UserProfile
from dashboard.forms import (
    UserForm, UserUpdateForm, UserProfileForm,
    UserPasswordForm)
from django.http import QueryDict
from django.contrib.auth.models import Permission, Group

import json
import logging

logger = logging.getLogger('opsweb')


class UserListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
    动作：getlist, create
    """
    model = UserProfile
    template_name = "dashboard/user_list.html"
    context_object_name = "userlist"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(username__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self, request):
        data = QueryDict(request.POST).dict()
        data['password'] = make_password('root1234')
        form = UserForm(data)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '用户成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        pk = QueryDict(request.body).dict().get('id', None)
        try:
            obj = self.model.objects.get(pk=pk)
            if obj:
                self.model.objects.filter(pk=pk).delete()
                res = {"code": 0, "result": "删除用户成功"}
            else:
                res = {"code": 1, "errmsg": "没有改用户，无法删除"}
        except Exception:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
        return JsonResponse(res, safe=True)


class UserDetailView(LoginRequiredMixin, DetailView):
    '''
    动作：getone, update, delete
    '''
    model = UserProfile
    template_name = "dashboard/user_edit.html"
    context_object_name = 'user'
    next_url = '/dashboard/userlist/'

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = UserUpdateForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            res = {"code": 0, "result": "更新用户成功", 'next_url': self.next_url}
        else:
            res = {"code": 1, "errmsg": form.errors, 'next_url': self.next_url}
        return render(request, settings.JUMP_PAGE, res)


class ModifyPwdView(LoginRequiredMixin, TemplateView):
    """
    修改密码
    """
    model = UserProfile
    template_name = "dashboard/change_passwd.html"
    context_object_name = 'user'
    next_url = '/dashboard/userlist/'
    res = {"code": 1, "errmsg": '', 'next_url': next_url}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uid = self.request.GET.get('uid', None)
        context['uid'] = uid
        return context

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('uid', None)
        # pk =kwargs.get('uid', None)
        password1 = request.POST.get('password1', None)
        password2 = request.POST.get('password2', None)
        if not pk:
            self.res['errmsg'] = '没有用户id'
            return render(request, settings.JUMP_PAGE, self.res)
        if not password1 and not password2:
            self.res['errmsg'] = '密码不能为空'
            return render(request, settings.JUMP_PAGE, self.res)
        if password1 != password2:
            self.res['errmsg'] = '两次密码不一致'
            return render(request, settings.JUMP_PAGE, self.res)
        user_object = self.model.objects.filter(pk=pk).first()
        if not user_object:
            self.res['errmsg'] = '没有此用户'
            return render(request, settings.JUMP_PAGE, self.res)
        # pk=QueryDict(request.body).dict().get('pk')
        # pk=kwargs.get('pk',None)
        # pk=self.kwargs.get(self.pk_url_kwarg)
        data = {}
        data['password'] = make_password(password1)
        form = UserPasswordForm(data, instance=user_object)
        if form.is_valid:
            form.save()
            self.res = {"code": 0, "result": "更新用户密码成功",
                        'next_url': self.next_url}
        else:
            self.res = {"code": 1, "errmsg": form.errors,
                        'next_url': self.next_url}

        return render(request, settings.JUMP_PAGE, self.res)


class UserGroupPowerView(DetailView):
    model = UserProfile
    template_name = "dashboard/user_group_power.html"
    context_object_name = 'user'
    next_url = '/dashboard/userlist/'

    def get_context_data(self, **kwargs):
        context = super(UserGroupPowerView, self).get_context_data(**kwargs)
        context['user_has_groups'] = self.user_has_groups()
        context['user_not_groups'] = self.user_not_groups()
        context['user_not_permissions'] = self.user_not_permissions()
        context['user_has_permissions'] = self.user_has_permissions()
        return context

    def user_has_permissions(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return []
        user_object = self.model.objects.filter(pk=pk).first()
        if not user_object:
            return []
        return user_object.user_permissions.all()

    def user_not_permissions(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return []
        user_object = self.model.objects.filter(pk=pk).first()
        if not user_object:
            return []
        return [user for user in Permission.objects.all() if user
                not in user_object.get_all_permissions()]

    def user_has_groups(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return []
        user_object = self.model.objects.filter(pk=pk).first()
        if not user_object:
            return []
        return user_object.groups.all()

    def user_not_groups(self):
        pk = self.kwargs.get('pk', None)
        if not pk:
            return []
        user_object = self.model.objects.filter(pk=pk).first()
        if not user_object:
            return []
        group_queryset = Group.objects.all()
        return [group for group in group_queryset if group not in
                user_object.groups.all()]

    def post(self, request, *args, **kwargs):
        groups_id_list = request.POST.getlist('groups_selected', [])
        perms_id_list = request.POST.getlist('perms_selected', [])
        pk = kwargs.get('pk', None)
        res = {"code": 1, "errmsg": "", 'next_url': self.next_url}
        if not pk:
            res["errmsg"] = '没有用户id'
            return render(request, settings.JUMP_PAGE, res)
        user_object = self.model.objects.filter(pk=pk).first()
        if not user_object:
            res['errmsg'] = '没有该用户'
            return render(request, settings.JUMP_PAGE, res)
        try:
            user_object.groups.clear()
            for group in groups_id_list:
                user_object.groups.add(group)
            user_object.user_permissions.clear()
            for perm in perms_id_list:
                user_object.user_permissions.add(perm)
            user_object.save()
            res.pop('errmsg')
            res['result'] = '修改成功'
            res['code'] = 0
            return render(request, settings.JUMP_PAGE, res)
        except Exception as e:
            print(e)
            res['errmsg'] = '修改失败，请联系管理员'
            return render(request, settings.JUMP_PAGE, res)

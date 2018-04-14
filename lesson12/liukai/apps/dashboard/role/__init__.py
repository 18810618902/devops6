#! /usr/bin/env python
# encoding: utf8

"""
@Author: liukai
@Date: 2018/3/26
"""
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from dashboard.forms import RoleForm, RoleUpdateForm
from django.http import QueryDict

import json
import logging

logger = logging.getLogger('opsweb')


class GroupListView(LoginRequiredMixin, PaginationMixin, ListView):
    '''
    动作：getlist, create
    '''
    model = Group
    template_name = "dashboard/group_list.html"
    context_object_name = "grouplist"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(GroupListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self, request):
        form = RoleUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '增加角色成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        pk = QueryDict(request.body).dict().get('id', None)
        # 通过角色对象查所在改角色下的用，如果有关联用户不可删除，没有关联用户可以删除
        try:
            obj = self.model.objects.get(pk=pk)
            if obj:
                user_queryset = obj.user_set.all()
                if not user_queryset:
                    obj.delete()
                    res = {"code": 0, "result": "删除角色成功"}
                    return JsonResponse(res, safe=True)
                res = {"code": 1, "errmsg": "该角色关联权限,请联系管理员"}
            else:
                res = {"code": 1, "errmsg": "该角色关联权限,请联系管理员"}
        except:
            res = {"code": 1, "errmsg": "删除角色请联系管理员"}
        return JsonResponse(res, safe=True)


class GroupDetailView(LoginRequiredMixin, DetailView):
    '''
    动作：getone, update, delete
    '''
    model = Group
    template_name = "dashboard/group_edit.html"
    context_object_name = 'group'
    next_url = '/dashboard/grouplist/'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        context['group_has_permissions'] = self.get_groups_permissions()
        context['group_not_permissions'] = self.get_groups_not_permissions()
        return context

    def post(self, request, *args, **kwargs):
        permission_id_list = request.POST.getlist('perms_selected', [])
        gid = request.POST.get('gid', None)
        name = request.POST.get('name', None)
        res = {"code": 1, "errmsg": "", 'next_url': self.next_url}
        if not gid:
            res["errmsg"] = "无改角色id"
            return render(request, settings.JUMP_PAGE, res)
        group = self.model.objects.filter(pk=gid).first()
        print(type(group))
        if not group:
            res["errmsg"] = "无改角色"
            return render(request, settings.JUMP_PAGE, res)
        try:
            group.permissions.clear()
            for permission_id in permission_id_list:
                group.permissions.add(permission_id)
            group.name = name
            group.save()
            res.pop('errmsg')
            res["code"] = 0
            res["result"] = "修改角色成功"
            return render(request, settings.JUMP_PAGE, res)
        except Exception:
            res["result"] = "修改角色失败，请联系管理员"
            return render(request, settings.JUMP_PAGE, res)

    def get_groups_permissions(self):
        pk = self.kwargs.get('pk', None)
        if pk:
            group = Group.objects.filter(pk=pk).first()
            if group:
                return group.permissions.all()
        return []

    def get_groups_not_permissions(self):
        pk = self.kwargs.get('pk', None)
        if pk:
            group = Group.objects.filter(pk=pk).first()
            prems_all = Permission.objects.all()
            if group:
                prems = [prem for prem in prems_all if
                         prem not in group.permissions.all()]
                return prems
        return []

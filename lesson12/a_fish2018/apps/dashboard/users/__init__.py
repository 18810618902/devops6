# coding=utf8
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.http import  HttpResponse, JsonResponse, QueryDict
from django.conf import settings
from django.contrib.auth.models import  Permission,Group
from dashboard.models import UserProfile
import json
import logging
import traceback
from  dashboard.forms import  UserUpdateForm,UserForm

logger = logging.getLogger('opsweb')


class UserListView(LoginRequiredMixin, PaginationMixin, ListView):
    '''
    动作：getlist, create
    '''
    model = UserProfile
    template_name = "dashboard/user_list.html"
    context_object_name = "userlist"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(username__icontains=self.keyword)|
                                       Q(name_cn__icontains=self.keyword)|
                                       Q(phone__icontains=self.keyword) |
                                       Q(email__icontains=self.keyword)
                                       )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context


    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # self.model.objects.create_user(username="fish2020", password="mm123456")
            res = {'code': 0, 'result': '用户添加成功'}
        else:
            res = {'code': 1, 'errmsg': form.errors}
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        # print data
        pk = data.get('id')
        # print "this is pk: %s" % pk
        try:
            self.model.objects.get(pk=pk).delete()
            res = {"code": 0, "errmsg": "删除成功"}
        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
        return JsonResponse(res, safe=True)




class UserDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "dashboard/user_edit.html"
    context_object_name = 'user'
    next_url = '/dashboard/userlist/'


    def post(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        u = UserProfile.objects.get(pk=pk)
        form = UserUpdateForm(request.POST, instance=u)
        if form.is_valid():
            form.save()
            res = {"code": 0, "result": "更新成功", 'next_url': self.next_url}
        else:
            res = {"code": 1, "errmsg": form.errors, 'next_url': self.next_url}
            logger.error("delete power  error: %s" % traceback.format_exc())
        return render(request, settings.JUMP_PAGE, res)





class UserGroupPowerView(LoginRequiredMixin, DetailView):

    model = UserProfile
    template_name = "dashboard/user_group_power.html"
    context_object_name = 'user'
    next_url = '/dashboard/userlist/'


    def get_context_data(self, **kwargs):
        context = super(UserGroupPowerView, self).get_context_data(**kwargs)
        # 获取用户
        user = kwargs.get('object')
        # 获取用户的所有组
        user_has_groups = user.groups.all()
        # 获取用户所在组的权限的id
        gids = []
        pids = []
        for group in user_has_groups:
            gids.append(group.id)
            for gps in group.permissions.all():
                pids.append(gps.id)
        # 获取用户所在组的所有权限
        user_groups_permissions = Permission.objects.all().filter(id__in=pids)
        # 获取用户的权限的id
        for up in user.user_permissions.all():
            pids.append(up.id)
        # 用户没有加入的组
        user_not_groups = Group.objects.all().exclude(id__in=gids )
        # 用户所有的权限
        user_has_permissions = Permission.objects.all().filter(id__in=pids)
        # 用户没有的权限
        user_not_permissions = Permission.objects.all().exclude(id__in=pids)
        context['user_groups_permissions'] = user_groups_permissions
        context['user_has_groups'] = user_has_groups
        context['user_not_groups'] = user_not_groups
        context['user_has_permissions'] = user_has_permissions
        context['user_not_permissions'] = user_not_permissions
        return context


    def post(self, request, *args, **kwargs):
        u = self.model.objects.get(pk=kwargs.get('pk'))
        perms = request.POST.getlist('perms_selected')
        groups = request.POST.getlist('groups_selected')

        try:
            u.groups = groups
            perm_ids = request.POST.getlist('perms_selected')
            u.user_permissions = perm_ids
            u.save()
            res = {"code": 0, "result": "更新成功", 'next_url': self.next_url}
        except:
            res = {"code": 1, "errmsg": "更新失败", 'next_url': self.next_url}
            logger.error("delete power  error: %s" % traceback.format_exc())

        return render(request, settings.JUMP_PAGE, res)




from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm

class ModifyPwdView(LoginRequiredMixin,PasswordChangeView):
    template_name = "dashboard/change_passwd2.html"
    form_class = PasswordChangeForm
    success_url = "/dashboard/userlist/"

    def dispatch(self, *args, **kwargs):
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)
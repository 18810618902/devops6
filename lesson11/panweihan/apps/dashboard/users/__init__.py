#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,QueryDict,Http404
from django.core.urlresolvers import reverse
from django.views.generic import View, ListView, DetailView,TemplateView
from django.db.models import Q
from django.contrib.auth.models import Permission,ContentType
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
# 自定义模块导入

from django.conf import settings
from pure_pagination.mixins import PaginationMixin
from ..forms import PermForm,PermUpdateForm,UserProfileForm,UserForm
from ..models import UserProfile

import traceback,json,logging


logger = logging.getLogger("opsweb")

class UserListView(LoginRequiredMixin,PaginationMixin,ListView):
    model = UserProfile
    template_name = 'dashboard/user_list.html'
    context_object_name = 'userlist'
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(UserListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(username__icontains = self.keyword)|
                                       Q(name_cn__icontains = self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['contents'] = ContentType.objects.all()
        return context

    def post(self, request,*args,**kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '添加用户成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
            print form.errors
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        pk = data.get('id')
        try:
            self.model.objects.filter(pk=pk).delete()
            res = {"code": 0, "result": "删除成功"}
        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
            logger.error("delete power error:%s" % traceback.format_exc())
        return JsonResponse(res, safe=True)

class UserDetailView(LoginRequiredMixin, DetailView):
    '''
    动作：getone, update, delete
    '''
    model = UserProfile
    template_name = "dashboard/user_edit.html"
    context_object_name = "user"

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        p = self.model.objects.get(pk=pk)
        form = UserForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            res = {"code": 0, "result": "更新成功"}
        else:
            res = {"code": 1, "errmsg": form.errors}
        return render(request, settings.JUMP_PAGE, res)

class ModifyPwdView(TemplateView):
    template_name = "dashboard/change_passwd.html"

    def get_context_data(self,**kwargs):
        context = super(ModifyPwdView,self).get_context_data(**kwargs)
        context['uid'] = self.request.GET.get('uid')
        return context

    def post(self,request,*args,**kwargs):
        webdata = QueryDict(request.body).dict()
        if webdata.get('password1') == webdata.get('password2'):
            userobj = UserProfile.objects.get(pk = webdata.get('uid'))
            userobj.set_password('password')
            userobj.save()
            res = {"code": 0, "result": "修改成功"}
        else:
            res = {"code": 1, "result": "两次密码不一样"}
        return render(request,settings.JUMP_PAGE,res)

class UserGroupPowerView(DetailView):
    model = UserProfile
    template_name = "dashboard/user_group_power.html"
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserGroupPowerView,self).get_context_data(**kwargs)
        userobj = self.get_object()
        context['user_has_groups'] = userobj.groups.all()
        context['user_not_groups'] = list(set(Group.objects.all()).difference(set(userobj.groups.all())))
        context['user_has_permissions'] = userobj.user_permissions.all()
        context['user_not_permissions'] = list(set(Permission.objects.all()).difference(set(userobj.user_permissions.all())))
        return context

    def post(self,request,*args,**kwargs):
        userobj = self.get_object()
        group_id_list = request.POST.getlist('groups_selected',[])
        perm_id_list = request.POST.getlist('perms_selected', [])
        try:
            userobj.groups = group_id_list
            userobj.user_permissions = perm_id_list
            res = {'code':0,'next_url':'/dashboard/userlist/','result':'用户角色权限修改成功'}
        except:
            res = {'code': 1, 'next_url': '/dashboard/userlist/', 'result': '用户角色权限更新失败'}
        return render(request,settings.JUMP_PAGE,res)








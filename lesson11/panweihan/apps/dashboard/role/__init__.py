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
from ..forms import PermForm,PermUpdateForm,UserProfileForm,UserForm,GroupForm
from ..models import UserProfile

import traceback,json,logging


logger = logging.getLogger("opsweb")

class GroupListView(LoginRequiredMixin,PaginationMixin,ListView):
    model = Group
    template_name = 'dashboard/group_list.html'
    context_object_name = 'grouplist'
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(GroupListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(name__icontains = self.keyword)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def post(self, request,*args,**kwargs):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '添加组成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
            print form.errors
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        pk = data.get('id')
        try:
            group_obj = self.model.objects.get(pk=pk)
            if group_obj.user_set.all():
                res = {"code": 1, "errmsg": "组内有成员，请先删除成员"}
            else:
                self.model.objects.filter(pk=pk).delete()
                res = {"code": 0, "result": "删除成功"}
        except:
            logger.error("delete power error:%s" % traceback.format_exc())
        return JsonResponse(res, safe=True)

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = "dashboard/group_edit.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        groupobj = self.get_object()
        context['group_has_permissions'] = groupobj.permissions.all()
        context['group_not_permissions'] = list(set(Permission.objects.all()).difference(set(groupobj.permissions.all())))
        return context

    def post(self,request,*args,**kwargs):
        groupobj = self.get_object()
        name = request.POST.get('name')
        permission_id_list = request.POST.getlist('perms_selected',[])
        try:
            groupobj.permissions = permission_id_list
            groupobj.name = name
            groupobj.save()
            res = {'code':0,'next_url':'/dashboard/grouplist/','result':'组更新成功'}
        except:
            res = {'code': 1, 'next_url': '/dashboard/grouplist/', 'result': '组更新失败'}
            logger.error("edit group error:%s" % traceback.format_exc())
        return render(request,settings.JUMP_PAGE,res)
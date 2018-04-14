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
# from dashboard.models import UserProfile
from django.contrib.auth.models import  Permission,Group
import json
import logging
import traceback
from  dashboard.forms import  GroupForm,GroupUpdateForm


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
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '角色添加成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        # print data
        pk = data.get('id')
        # print "this is pk: %s" % pk
        try:
            group_name  = self.model.objects.get(pk=pk)
            print group_name.id
            print group_name.user_set.all()
            if group_name.user_set.all():
                res = {"code": 1, "errmsg": "删除错误请联系管理员"}
            else:
                self.model.objects.get(pk=pk).delete()
                res = {"code": 0, "errmsg": "删除成功"}

        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
            #logger.error("")
        return JsonResponse(res, safe=True)




class GroupDetailView(LoginRequiredMixin, DetailView):

    model = Group
    template_name = "dashboard/group_edit.html"
    context_object_name = 'group'
    next_url = '/dashboard/grouplist/'


    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data(**kwargs)
        group_has_permissions = kwargs.get('object').permissions.all()
        ids = []
        for perm in group_has_permissions:
            ids.append(perm.id)
        context['group_has_permissions'] = group_has_permissions
        context['group_not_permissions'] = Permission.objects.all().exclude(id__in=ids )
        return context

    def post(self, request, *args, **kwargs):
        g = self.model.objects.get(pk=kwargs.get('pk'))
        form = GroupUpdateForm(request.POST, instance=g)
        if form.is_valid():
            form.save()
            perm_ids = request.POST.getlist('perms_selected')
            g.permissions = perm_ids
            g.save()
            res = {"code": 0, "result": "更新成功", 'next_url': self.next_url}
        else:
            res = {"code": 1, "errmsg": form.errors, 'next_url': self.next_url}
            logger.error("delete power  error: %s" % traceback.format_exc())

        return render(request, settings.JUMP_PAGE, res)


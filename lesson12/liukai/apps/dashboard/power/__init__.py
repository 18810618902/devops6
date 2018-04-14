# coding=utf8
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
# from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, ContentType
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from dashboard.forms import PowerForm, PowerUpdateForm
from django.http import QueryDict
from django.shortcuts import render

import json
import logging

logger = logging.getLogger('opsweb')


class PowerListView(LoginRequiredMixin, PaginationMixin, ListView):
    '''
    动作：getlist, create
    '''
    model = Permission
    template_name = "dashboard/power_list.html"
    context_object_name = "powerlist"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(PowerListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(name__icontains=self.keyword)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PowerListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        # context['authors']=Author.objects.all()
        context['contents'] = ContentType.objects.all()
        return context

    def post(self, request):
        form = PowerForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '添加权限成功'}
        else:
            res = {'code': 1, 'errmsg': form.errors}
        return JsonResponse(res, safe=True)

    def delete(self, request, **kwargs):
        data = QueryDict(request.body).dict()
        pk = data.get('id', None)
        if not pk:
            res = {'code': 1, 'errmsg': '无该权限id'}
            return JsonResponse(res, safe=True)
        power_object = self.model.objects.filter(pk=pk).first()

        if not power_object:
            res = {'code': 1, 'errmsg': '无该权限'}
            return JsonResponse(res, safe=True)
        if power_object.group_set.all() or power_object.user_set.all():
            res = {'code': 1, 'errmsg': '删除权限失败，权限已经被调用'}
        else:
            power_object.delete()
            res = {'code': 0, 'result': '删除权限成功'}
        return JsonResponse(res, safe=True)


class PowerDetailView(DetailView):
    model = Permission
    template_name = "dashboard/power_edit.html"
    context_object_name = 'power'
    next_url = '/dashboard/powerlist/'

    def get_context_data(self, **kwargs):
        context = super(PowerDetailView, self).get_context_data(**kwargs)
        context['contents'] = ContentType.objects.all()
        return context

    def post(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            res = {'code': 1, 'errmsg': '无该权限id'}
            return JsonResponse(res, safe=True)
        power_object = self.model.objects.filter(pk=pk).first()
        if not power_object:
            res = {'code': 1, 'errmsg': '无该权限'}
            return JsonResponse(res, safe=True)
        form = PowerUpdateForm(request.POST, instance=power_object)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '修改权限成功', 'next_url': self.next_url}
        else:
            res = {'code': 1, 'errmsg': form.errors}
        return render(request, settings.JUMP_PAGE, res)

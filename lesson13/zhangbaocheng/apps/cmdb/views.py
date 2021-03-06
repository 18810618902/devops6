# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse

from django.views.generic import View,  ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin
from django.db.models import Q
from django.core.urlresolvers import reverse

from .models import Host, Product
from utils.data_cloud import get_hosts_from_cloud,get_hosts_from_qcloud

# Create your views here.

class  ImportDataView(LoginRequiredMixin, View):
    def get(self, request):
        is_success = get_hosts_from_cloud()

        if is_success:
            print('主机更新/导入成功~')
            return  HttpResponse('主机更新/导入成功~')
        else:
            return HttpResponse('主机更新/导入失败~')


class  HostListView(LoginRequiredMixin, ListView):
    template_name = 'cmdb/host_list.html'
    model = Host
    paginate_by =  10
    context_object_name = 'host_list'
    keyword = ''
    def  get_queryset(self):
        queryset = super(HostListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(instance_name__icontains = self.keyword) |
                                       Q(description__icontains=self.keyword) |
                                       Q(cloud_type__icontains=self.keyword) |
                                       Q(private_ip__icontains=self.keyword) ).order_by('id')
        return  queryset

    def get_context_data(self, **kwargs):
        context = super(HostListView, self).get_context_data(**kwargs)
        context['keyword'] =  self.keyword
        return  context



class HostEditView(LoginRequiredMixin, UpdateView):
    """
    更新主机所属的产品线
    """

    template_name = 'cmdb/host_edit.html'
    model = Host
    fields = ('business_line',)

    def get_success_url(self):
        if '_edit' in self.request.POST:
            return reverse('cmdb:host_edit', kwargs={'pk': self.object.pk})
        return reverse('cmdb:host_list')

    def get_context_data(self, **kwargs):
        context = super(HostEditView, self).get_context_data(**kwargs)
        all_product_lines = Product.objects.filter(pid_id__gt=0).all().order_by('id')
        host = self.model.objects.filter(pk=self.kwargs['pk'])
        if host.exists():
            product_lines = host[0].business_line.all().values_list('id')
            product_lines = [int(product_line[0]) for product_line in product_lines]
        else:
            product_lines = []
        context['all_product_lines'] = all_product_lines
        context['product_lines'] = product_lines
        return context




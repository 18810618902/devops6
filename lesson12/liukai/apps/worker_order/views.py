from django.db.models import Q
from .models import WorkOrder, WorkEchartsData
from .forms import WorkOrderApplyForm, WorkOrderResultForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import (
    HttpResponse, HttpResponseRedirect, JsonResponse,
    QueryDict, Http404)
from django.urls import reverse
from django.views.generic import View, ListView, DetailView
from django.db.models import Q
from django.core.mail import send_mail
import traceback, json, logging
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination.mixins import PaginationMixin


# from django.core.


# Create your views here.

class WorkOrderApplyView(View):
    def get(self, request):
        forms = WorkOrderApplyForm()
        return render(request, 'order/workorder_apply.html', {'forms': forms})

    def post(self, request):
        forms = WorkOrderApplyForm(request.POST)
        if forms.is_valid():
            print(forms.cleaned_data)
            type = forms.cleaned_data['type']
            title = forms.cleaned_data['title']
            order_contents = forms.cleaned_data['order_contents']
            applicant = request.user
            assign_to = forms.cleaned_data['assign_to']
            data = {'type': type,
                    'title': title,
                    'order_contents': order_contents,
                    'applicant': applicant,
                    'status': 0,
                    'assign_to_id': int(assign_to)
                    }
            worker_order = WorkOrder.objects.create(**data)
            send_mail(worker_order.title,
                      worker_order.order_contents,
                      settings.EMAIL_FROM,
                      ['651002081@qq.com'],
                      fail_silently=False,
                      )
            return HttpResponseRedirect(reverse('worker_order:list'))
        else:
            return render(request, 'order/workorder_apply.html',
                          {'forms': forms, 'errmsg': '工单填写错误'})


class WorkOrderListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
        未处理工单列表展示
    """

    model = WorkOrder
    template_name = 'order/workorder_list.html'
    context_object_name = "orderlist"
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(WorkOrderListView, self).get_queryset()

        # 只显示状态小于2，即申请和处理中的工单
        queryset = queryset.filter(status__lt=2)

        # 如果不是sa组的用户只显示自己申请的工单，别人看不到你申请的工单，管理员可以看到所有工单
        if 'sa' not in [group.name for group in
                        self.request.user.groups.all()]:
            queryset = queryset.filter(applicant=self.request.user)

        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(title__icontains=self.keyword) |
                                       Q(
                                           order_contents__icontains=self.keyword) |
                                       Q(result_desc__icontains=self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WorkOrderListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

    def delete(self, request, *args, **kwargs):
        try:
            data = QueryDict(request.body)
            pk = data.get('id')
            work_order = self.model.objects.get(pk=pk)
            work_order.status = 3
            work_order.save()
            ret = {'code': 0, 'result': '取消工单成功！'}
        except:
            ret = {'code': 1, 'errmsg': '取消工单失败！'}
            # logger.error("delete order  error: %s" % traceback.format_exc())
        return JsonResponse(ret, safe=True)


class WorkOrderDetailView(DetailView):
    model = WorkOrder
    template_name = 'order/workorder_detail.html'
    context_object_name = 'work_order'

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        work_order_object = self.model.objects.filter(pk=pk).first()

        if work_order_object.status == 0:
            work_order_object.status = 1
            work_order_object.save()
            return render(request, 'order/workorder_detail.html',
                          {'work_order': work_order_object, 'msg': '您的工单已受理'})

        if work_order_object.status == 1:
            forms = WorkOrderResultForm(request.POST)
            if forms.is_valid():
                result_desc = request.POST.get('result_desc', '')
                work_order_object.result_desc = result_desc
                work_order_object.status = 2
                work_order_object.save()
                return HttpResponseRedirect(reverse('work_order:list'))
            else:
                return render(request, 'order/workorder_detail.html',
                              {'work_order': work_order_object,
                               'errmsg': '必须填写处理结果'})


class WorkOrderHistoryView(LoginRequiredMixin, PaginationMixin, ListView):
    model = WorkOrder
    template_name = 'order/workorder_history.html'
    context_object_name = 'historylist'
    paginate_by = 5
    keyword = ''

    def get_queryset(self):
        queryset = super(WorkOrderHistoryView, self).get_queryset()
        queryset = queryset.filter(status__gte=2)
        return queryset


class WorkEchartsView(View):
    model = WorkOrder

    def get(self, request):
        work_queryset = self.model.objects.all()
        name_list = list()
        if work_queryset:
            for work in work_queryset:
                applicant = work.applicant
                if applicant not in name_list:
                    name_list.append(applicant)
            print(name_list)
            data_list = list()
            web_list = list()
            task_list = list()
            config_list = list()
            other_list = list()
            name_ = list()
            for name in name_list:
                data = 0
                web = 0
                task = 0
                config = 0
                other = 0
                for work in work_queryset:
                    if name == work.applicant:
                        if work.type == 0:
                            data += 1
                        elif work.type == 1:
                            web += 1
                        elif work.type == 2:
                            task += 1
                        elif work.type == 3:
                            config += 1
                        else:
                            other += 1
                data_list.append(data)
                web_list.append(web)
                task_list.append(task)
                config_list.append(config)
                other_list.append(other)
            for name in name_list:
                name_.append(name.username)
            data = {'name_list': name_, 'data_list': data_list,
                    'web_list': web_list, 'task_list': task_list,
                    'config_list': config_list, 'other_list': other_list}
            print(data)
        else:
            data = {}
        return JsonResponse(data)


class WorkEchartsDataView(View):
    model = WorkEchartsData

    def get(self, request):
        echarts_object = self.model.objects.all().first()
        if echarts_object:
            data = json.loads(echarts_object.data)
        else:
            data = {}
        print('day', data)
        return JsonResponse(data)

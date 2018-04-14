# coding=utf8
from django.views.generic import ListView, DetailView, CreateView,View
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from pure_pagination.mixins import PaginationMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from  django.http import  HttpResponse, JsonResponse, QueryDict,Http404
from django.conf import settings
from dashboard.models import UserProfile
from django.contrib.auth.models import  Group, Permission
from  forms import WorkOrderApplyForm, WorkOrderCreateForm

from models import WorkOrder,Statistics
from . import tasks

from django.db.models import Count
from datetime import datetime,timedelta
# end_date = datetime.now()
end_date = datetime.now() + timedelta(days=1)
start_date = (datetime.now() - timedelta(days=7))



class  WorkOrderApplyView(LoginRequiredMixin, View):

    def get(self, request):
        forms  = WorkOrderApplyForm()
        return  render(request, 'order/workorder_apply.html', {'forms':forms})

    def post(self,request):
        forms = WorkOrderApplyForm(request.POST)
        if forms.is_valid():
            type = forms.cleaned_data["type"]
            title = forms.cleaned_data["title"]
            order_contents = forms.cleaned_data["order_contents"]
            assign_to = forms.cleaned_data["assign_to"]

            work_order = WorkOrder()
            work_order.type = int(type)
            work_order.title = title
            work_order.order_contents = order_contents
            work_order.assign_to_id = int(assign_to)
            work_order.applicant = request.user
            work_order.status = 0
            work_order.save()

            return HttpResponseRedirect('/search/?q=%s' % title)
        else:
            return render(request,'order/workorder_apply.html')



class WorkOrderListView(LoginRequiredMixin, PaginationMixin, ListView):
    '''
        未处理工地列表展示
    '''

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
        if 'sa' not in [group.name for group in self.request.user.groups.all()]:
            queryset = queryset.filter(applicant=self.request.user)

        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(title__icontains = self.keyword)|
                                       Q(order_contents__icontains = self.keyword)|
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
            work_order = WorkOrder.objects.get(pk=pk)
            work_order.status = 3
            work_order.save()
            ret = {'code': 0, 'result': '取消工单成功！'}
        except:
            ret = {'code': 1, 'errmsg': '取消工单失败！'}

        return JsonResponse(ret, safe=True)





class WorkOrderDetailView(LoginRequiredMixin, DetailView):

    model = WorkOrder
    template_name = "order/workorder_detail.html"
    context_object_name = 'work_order'
    next_url = '/work_order/list/'


    def post(self, request, *args, **kwargs):
        webdata = QueryDict(request.body).dict()
        status = webdata['status']
        id = webdata['id']
        ob = self.get_object()

        if  int(status) == 0:
            self.model.objects.filter(id__exact=id).update(status=1)
            res = {"code": 0, "result": "已接受工单", 'next_url': self.next_url}
        if  int(status) == 1:
            result_desc = webdata['result_desc']
            # 更新表方式一
            ob.result_desc=result_desc
            ob.save()
            # 更新表方式二
            self.model.objects.filter(id__exact=id).update(status=2)
            res = {"code": 0, "result": "已完成工单", 'next_url': self.next_url}

        return render(request, settings.JUMP_PAGE, res)





class WorkOrderHistoryView(LoginRequiredMixin,ListView):
    model = WorkOrder
    template_name = 'order/workorder_history.html'
    context_object_name = "historylist"
    paginate_by = 5
    keyword = ''


    def get_queryset(self):
        queryset = super(WorkOrderHistoryView, self).get_queryset()

        # 只显示状态小于2，即申请和处理中的工单
        queryset = queryset.filter(status__gt=1)

        # 如果不是sa组的用户只显示自己申请的工单，别人看不到你申请的工单，管理员可以看到所有工单
        if 'sa' not in [group.name for group in self.request.user.groups.all()]:
            queryset = queryset.filter(applicant=self.request.user)

        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(title__icontains=self.keyword) |
                                       Q(order_contents__icontains=self.keyword) |
                                       Q(result_desc__icontains=self.keyword))
        return queryset


    def get_context_data(self, **kwargs):
        context = super(WorkOrderHistoryView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        return context

class BarListView(LoginRequiredMixin,View):
    model = WorkOrder
    template_name = 'bar.html'


    def get(self, request, *args, **kwargs):
        # # 取出所有工单
        # # a = WorkOrder.objects.all()
        # # 取出所有提交者id
        # uids = []
        # for aa in WorkOrder.objects.all():
        #     uids.append(aa.applicant_id)
        # uids = list(set(uids))
        # # 查询每一个提交者最近一周提交的工单类型对应的数量
        # for id in uids:
        #     wo = WorkOrder.objects.filter(applicant_id=id, apply_time__range=(start_date, end_date))
        #     a = wo.filter(type__exact=0).count()
        #     b = wo.filter(type__exact=1).count()
        #     c = wo.filter(type__exact=2).count()
        #     d = wo.filter(type__exact=3).count()
        #     e = wo.filter(type__exact=4).count()
        #     print 'id: %s --------' % id,a, b, c, d, e
        #
        #     Statistics.objects.filter(applicant__exact=id).update(applicant=id, type0=a, type1=b, type2=c, type3=d,
        #                                                           type4=e)

        pk = kwargs.get('pk')
        s = Statistics.objects.filter(applicant__exact=pk).first()
        data = [int(s.type0), int(s.type1), int(s.type2), int(s.type3), int(s.type4)]
        # print s.applicant,data
        context = {}
        context['data'] = data
        return render(request,template_name='bar.html',context=context)
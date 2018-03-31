#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,QueryDict,Http404
from django.core.urlresolvers import reverse
from django.views.generic import View, ListView, DetailView
from django.db.models import Q
from django.contrib.auth.models import Permission,ContentType


from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

# 自定义模块导入

from django.conf import settings
from pure_pagination.mixins import PaginationMixin
from ..forms import PermForm,PermUpdateForm

import traceback,json,logging


logger = logging.getLogger("opsweb")


class PowerListView(LoginRequiredMixin, PaginationMixin, ListView):
    """
        查看所有用户:只有指定权限的用户可看
    """
    model = Permission
    template_name = 'dashboard/power_list.html'
    context_object_name = "powerlist"
    paginate_by = 5
    keyword = ''

    # @method_decorator(permission_required('dashboard', login_url='/'))
    def get_queryset(self):
        queryset = super(PowerListView, self).get_queryset()
        self.keyword = self.request.GET.get('keyword', '')
        if self.keyword:
            queryset = queryset.filter(Q(name__icontains = self.keyword)|
                                        Q(codename__icontains = self.keyword))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PowerListView, self).get_context_data(**kwargs)
        context['keyword'] = self.keyword
        context['contents'] = ContentType.objects.all()
        return context

    def post(self, request):
        form = PermForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': '添加策略成功'}
        else:
            # form.errors会把验证不通过的信息以对象的形式传到前端，前端直接渲染即可
            res = {'code': 1, 'errmsg': form.errors}
            print form.errors
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        pk = data.get('id')
        try:
            perm = self.model.objects.get(pk=pk)
            if perm.group_set.all() or perm.user_set.all():
                res = {"code": 1, "result": "改权限已被使用，删除失败"}
            else:
                self.model.objects.filter(pk=pk).delete()
                res = {"code": 0, "result": "删除成功"}
        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
            logger.error("delete power error:%s" % traceback.format_exc())
        return JsonResponse(res, safe=True)
    
class PowerDetailView(LoginRequiredMixin, DetailView):
    '''
    动作：getone, update, delete
    '''
    model = Permission
    template_name = "dashboard/power_edit.html"
    context_object_name = "power"

    def get_context_data(self, **kwargs):
        context = super(PowerDetailView, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        p  = self.model.objects.get(pk = pk)
        form = PermUpdateForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            res = {"code": 0, "result": "更新成功"}
        else:
            res = {"code": 1, "errmsg": form.errors}
        return render(request,settings.JUMP_PAGE,res)
        # return HttpResponseRedirect(reverse('books:publish_detail',args=[pk]))

    # def get_book_author(self,request,*args,**kwargs):
    #     pk = kwargs.get('pk')
    #     p = self.model.objects.get(pk=pk)
    #     authors_list = ['%s' a.id for a in p.author.all()]


    #
    # def delete(self, request, *args, **kwargs):
    #     data = QueryDict(request.body)
    #     pk = kwargs.get('pk')
    #     try:
    #         perm = self.model.objects.get(pk=pk)
    #         if perm.group_set.all() or perm.user_set.all():
    #             res = {"code": 1, "result": "改权限已被使用，删除失败"}
    #         else:
    #             self.model.objects.filter(pk=pk).delete()
    #             res = {"code": 0, "result": "删除成功"}
    #     except:
    #         res = {"code": 1, "errmsg": "删除错误请联系管理员"}
    #         logger.error("delete power error:%s" % traceback.format_exc())
    #     return JsonResponse(res, safe=True)
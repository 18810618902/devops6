# -*- coding: utf-8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import TemplateView

@method_decorator(login_required, name='dispatch')
class index(TemplateView):
    template_name = "index.html"
    def get_context_data(self,**kwargs):
        username = self.request.user
        userobj = User.objects.get(username=username)
        context = super(index, self).get_context_data(**kwargs)
        context['userobj'] = userobj
        return context


class mylogin(View):
# def mylogin(request):
    def get(self,request):
    # if request.method == 'GET':
        nexturl = request.GET.get('next')    # 获取前端传来的参数
        if nexturl == None:
            nexturl == '/'
        return render(request,'login.html',{'nexturl':nexturl}) # 将参数返回给前端
    def post(self, request):
    # if request.method == 'POST':
        name = request.POST.get('username')
        passwd = request.POST.get('passwd')
        user = authenticate(username=name,password=passwd)
        ret= {}
        if user is not None:
            ret['status'] = 0
            login(request,user)
        else:
            ret['status'] = 1
            ret['errmsg'] = '用户名或密码错误，请联系管理员'
        return JsonResponse(ret)


def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/login?next=/')
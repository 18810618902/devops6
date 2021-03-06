#coding=utf-8
from django.views.generic import View, TemplateView, ListView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http.response import JsonResponse

class mylogin(TemplateView):
    template_name = 'ucenter/login.html'
    def get_context_data(self, **kwargs):
        kwargs['next'] = self.request.GET.get('next')
        return super(mylogin, self).get_context_data(**kwargs)
    def post(self, request):
        uname = request.POST.get('username',None)
        passwd = request.POST.get('password',None)
        ret = {}
        user = authenticate(username=uname, password=passwd)  # django鉴权
        if user is not None:  # 用户密码及token正确
            login(request, user)
            next = request.get_full_path()
            ret['status'] = 0
            ret['next'] = next
        else:
            ret['status'] = 1
        print(ret)
        return JsonResponse(ret)

class mylogout(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/login/?next=/")


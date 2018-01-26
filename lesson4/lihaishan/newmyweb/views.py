#coding=utf8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import View,TemplateView,ListView
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required,name='dispatch')
class firstpage(TemplateView):
    template_name = 'index.html'


class mylogin(TemplateView): # 函数名不叫login
    template_name = 'login.html'
    #def get_context_data(self, **kwargs):
        #nexturl =self.request.GET.get('next')
        #print nexturl
        #return  {'nexturl':nexturl}
    def post(self,request):
        name = request.POST.get('username')
        passwd = request.POST.get('passwd')

        # ldap鉴权


        # django登录
        user = authenticate(username=name, password=passwd)  #1 鉴权
        print user
        ret = {}
        if user is not None:  # 用户存在，给他登录系统
            login(request, user)  # 2 登录
            ret['status'] = 0
            ret['next_url'] = request.GET.get("next") if request.GET.get("next", None) else "/"
        else:
            ret['status'] = 1
        print ret
        return  JsonResponse(ret)


class mylogout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('url_login')


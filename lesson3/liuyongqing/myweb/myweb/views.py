# -*- coding:utf8 -*-
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView


# @login_required
# def firstpage(request):
#     print request.user
#     # return HttpResponse('Hello django! Is Root')
#     return render(request,'index2.html')

@method_decorator(login_required,name='dispatch')
class firstpage(TemplateView):
    template_name = 'index2.html'


class mylogin(View):
    def get(self,request):
        nexturl=request.GET.get('next')
        # if nexturl is None:
            # nexturl='/'
        return render(request,'pages/examples/login.html',{'nexturl':nexturl})
    def post(self,request):
            name=request.POST.get('username',None)
            passwd=request.POST.get('passwd',None)
            ret={}
            user=authenticate(username=name,password=passwd)
            if user is not None: #用户存在，给他登陆系统的权限。
                login(request,user) #登陆
                ret['status']=0
            else:
                ret['status']=1
            print ret
            return JsonResponse(ret)

class mylogin2(TemplateView):
    template_name = 'pages/examples/login.html'
    def get_context_data(self, **kwargs):
        nexturl=self.request.GET.get('next')
        return {'nexturl':nexturl}

    def post(self,request):
            name=request.POST.get('username',None)
            passwd=request.POST.get('passwd',None)
            ret={}
            user=authenticate(username=name,password=passwd)
            if user is not None: #用户存在，给他登陆系统的权限。
                login(request,user) #登陆
                ret['status']=0
            else:
                ret['status']=1
            print ret
            return JsonResponse(ret)

class mylogout(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/login?next=/')


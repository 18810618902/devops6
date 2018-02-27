#coding=utf8
from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

'''
@login_required
def first(request):
    return render(request, 'index2.html')
'''

def autopage(request, path):
    return render(request, path)

class mylogin(TemplateView):  # 函数名不能叫login，和django的login重复
    template_name = 'pages/examples/login.html'
    def get_context_data(self, **kwargs):
        kwargs['nexturl'] = self.request.GET.get('next')
        return super(mylogin, self).get_context_data(**kwargs)
    def post(self, request):
        uname = request.POST.get('username')
        passwd = request.POST.get('passwd')
        """
            可在此处扩展ldap等方式的鉴权，
	    不通过直接返回登录失败，
	    通过则保存用户密码到User表 再进行如下的django鉴权流程
        """
        ret = {}
        user = authenticate(username=uname, password=passwd)  # django鉴权
        if user is not None:  # 用户密码正确
            login(request, user)
            ret['status'] = 0
        else:
            ret['status'] = -1
        return JsonResponse(ret)
    #else:
     #   nexturl = request.GET.get('next')
      #  return render(request, 'pages/examples/login.html', {'nexturl':nexturl})

def mylogout(request):
    logout(request)
    return HttpResponseRedirect("/login?next=/")


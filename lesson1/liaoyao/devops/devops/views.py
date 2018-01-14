#encoding: utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView

@login_required
def index(request):
    return render(request,'index.html')

class needlogin(View):
    def get(self,request):
        print(request.POST)
        nexturl = request.GET.get('next')
        if nexturl:
            return render(request, 'pages/examples/login.html',{'nexturl':nexturl})
        else:
            return render(request, 'pages/examples/login.html', {'nexturl':'/'})

    def post(self, request):
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        user = authenticate(username=name,password=pwd)
        result = {}
        if user:
            login(request,user)
            result['status'] = 0
        else:
            result['status'] = 1
        return JsonResponse(result)

class needlogin2(TemplateView):
    template_name = 'pages/examples/login.html'
    def get_context_data(self,**kwargs):
        nexturl = self.request.GET.get('next')
        if nexturl:
            kwargs['nexturl'] = nexturl
            #return {'nexturl':nexturl}
            return kwargs
        else:
            #return {'nexturl':'/'}
            kwargs['nexturl'] = '/'
            return kwargs

    def post(self, request):
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        user = authenticate(username=name,password=pwd)
        result = {}
        if user:
            login(request,user)
            result['status'] = 0
        else:
            result['status'] = 1
        return JsonResponse(result)

def mylogout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def test(request):
    print(request.POST)
    if request.method == 'GET':
        return render(request, 'test.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        result = {name: pwd}
        return JsonResponse(result)

@login_required
def hello(request):
    return HttpResponse('Hello!!')

class hello2(TemplateView):
    template_name = 'hello2.html'

    def get_context_data(self, **kwargs):
        #context = super(hello2, self).get_context_data(**kwargs)
        #context['username'] = '韩寒'
        #context['lans'] = ['python', 'mysql','docker']
        #return context
        kwargs['username'] = '韩寒'
        kwargs['lans'] = ['python', 'mysql','docker','shell']
        print(kwargs)
        #return super(hello2, self).get_context_data(**kwargs)
        return kwargs

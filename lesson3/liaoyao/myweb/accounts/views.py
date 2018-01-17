# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView,ListView
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Author

@method_decorator(login_required, name='dispatch')
class index(TemplateView):
    template_name = 'accounts/index.html'

class mylogin(TemplateView):
    template_name = 'accounts/pages/examples/login.html'

    def get_context_data(self, **kwargs):
        nexturl = self.request.GET.get('next')
        if nexturl:
            kwargs['nexturl'] = nexturl
        else:
            kwargs['nexturl'] = '/accounts'
        print kwargs
        return kwargs

    def post(self, request):
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        user = authenticate(username=name,password=pwd)
        result = {}
        print('name ==> {}'.format(name))
        print('pwd ==> {}'.format(pwd))
        if user:
            login(request,user)
            result['status'] = 0
        else:
            result['status'] = 1
        print result
        return JsonResponse(result)

class mylogout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/accounts/')

class authorquery(View):
    def get(self,request):
        qs = Author.objects.all()
        qsfans = qs.order_by('-fans')[:2]
        qsincome = qs.order_by('-income')[:2]
        qsret = list(set(qsfans).union(set(qsincome)))
        data = [i.todict for i in qsret]
        return JsonResponse({'status':0,'data':data})

def haha(request):
    return HttpResponse('haha')

class authorlist(ListView):
    model = Author
    template_name = 'accounts/authors.html'
    context_object_name = 'authors'
    paginate_by = 2


    def get_context_data(self, ** kwargs):
        context = super(authorlist, self).get_context_data(**kwargs)
        context['job'] = 'pythoner'
        return context

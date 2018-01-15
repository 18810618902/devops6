# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import  HttpResponse,JsonResponse,HttpResponseRedirect
import random
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import json
from .models import *
from django.views import View
from django.forms.models import model_to_dict
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.generic import ListView


@method_decorator(login_required,name='dispatch')
class firstpage(TemplateView):
    template_name = "index2.html"


# @csrf_exempt
class mylogin(TemplateView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        nexturl = self.request.GET.get("next")
        return {'nexturl':nexturl}


    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        ret = {}
        if user is not None:
            login(request,user)
            ret['status'] = 0
        else:
            ret['status'] = 1
        return JsonResponse(ret)

class mylogout(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('firstpage'))

class bookquery(View):
    def get(self,request):
        data = [i.todict for i in Book.objects.all()]
        return JsonResponse({'status': 0, 'data': data})

class authorquery(View):
    def get(self,request):
        qs = Author.objects.all()
        qsfans = qs.order_by('-fans')[:2]
        qsincome = qs.order_by('income')[:2]
        qsret = list(set(qsfans).union(set(qsincome)))
        data = [i.todict for i in Author.objects.all()]
        return JsonResponse({'status': 0, 'data': data})


class users(View):
    def get(self,request):
        return HttpResponse('Hello world')

class users1(View):
    def get(self,request,**kwargs):
        print request.user
        pk1 = self.kwargs.get('pk')
        return HttpResponse(pk1)

# class hello(TemplateView):
#     template_name = 'hello.html'
#
#     def get_context_data(self,**kwargs):
#         context = super(hello,self).get_context_data(**kwargs)
#         context['username'] = "韩寒"
#         context['lans'] = ['python','flask','django','java']
#         return context

class hello(TemplateView):
    template_name = 'hello.html'

    def get_context_data(self,**kwargs):
        kwargs['username'] = "韩寒"
        kwargs['lans'] = ['python','flask','django','java']
        print kwargs
        return kwargs

class authorlist(ListView):
    model = Author
    template_name = 'authors.html'
    context_object_name = 'authors'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        context = super(authorlist,self).get_context_data(**kwargs)
        context['job'] = 'pythonor'
        return context
    def get_queryset(self):
        return self.model.objects.order_by('-name')




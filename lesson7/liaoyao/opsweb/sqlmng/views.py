# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import View,ListView,DetailView,TemplateView
from django.http import  JsonResponse,QueryDict
from . import  inception




class inception_commit(TemplateView):
    template_name = 'sqlmng/inception_commit.html'


    def post(self,requests,**kwargs):
        webdata = QueryDict(requests.body).dict()
        print webdata
        inception.mysql_stuct(webdata['sqlcontent'])
        return JsonResponse({'status':0})
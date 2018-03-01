
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import View,TemplateView,ListView,DetailView
from django.http import JsonResponse,QueryDict
import inception



# Create your views here.

class inception_commit(TemplateView):

    template_name = 'sqlmng/inception_commit.html'

    def post(self,request,**kwargs):
        wdata = QueryDict(request.body).dict()
        mysql_structure = wdata['sqlcontent']
        inception.table_structure(mysql_structure)
        print wdata
        return JsonResponse({'status':0})


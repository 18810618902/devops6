# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def index_views(request):
    return  render(request,'index.html')

#! /usr/bin/env python
# encoding: utf8

"""
@Author: liukai
@Date: 2018/4/1
"""
from django.contrib.auth.models import Group


def context_data(request):
    group = Group.objects.all()
    data = dict()
    data['group'] = group
    return data
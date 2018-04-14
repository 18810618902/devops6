#! /usr/bin/env python
# encoding: utf8

"""
@Author: liukai
@Date: 2018/3/31
"""
from django.template import Library

register = Library()


@register.filter
def get_name(queryset):
    if len(queryset) < 3:
        return ','.join([quer.username for quer in queryset])
    else:
        return '%s...' % ','.join([quer.username for quer in queryset[0:2]])


@register.filter
def get_prems_name(queryset):
    if len(queryset) < 3:
        return ','.join([quer.name for quer in queryset])
    else:
        return '%s...' % ','.join([quer.name for quer in queryset[0:2]])

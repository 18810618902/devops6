#! /usr/bin/env python
# encoding: utf8

"""
@Author: liukai
@Date: 2018/3/31
"""
from django.template import Library

register = Library()


@register.filter
def get_object_name(object):
    result = object.name
    return result

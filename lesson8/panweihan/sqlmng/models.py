# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Basemodel(models.Model):
    '''
       基础表(抽象类)
    '''
    name = models.CharField(max_length=32, verbose_name='名字')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    note = models.TextField(default='', null=True, blank=True, verbose_name='备注')

    def __unicode__(self):
        return self.name  # 显示对象的名字

    class Meta:
        abstract = True  # 抽象类
        ordering = ['-id']  # 按id倒排

class dbconf(Basemodel):
    GENDER_CHOICES = (
                        ('1', u'生产'),
                        ('2', u'测试'),
    )
    user = models.CharField(max_length = 128)
    password = models.CharField(max_length = 128)
    host = models.CharField(max_length = 16)
    port = models.CharField(max_length = 5)
    env = models.CharField(max_length = 1, blank = True, null = True, choices = GENDER_CHOICES)

class sqlconf(Basemodel):
    GENDER_CHOICES = (
                        ('1', u'生产'),
                        ('2', u'测试'),
    )
    CONDTION_CHOICES = (
                        ('1', u'待执行'),
                        ('2', u'已执行'),
                        ('3', u'已拒绝'),
                        ('4', u'已回滚'),
    )
    OPERATE_CHOICES = (
                        ('1', u'执行'),
                        ('2', u'拒绝'),
                        ('3', u'回滚'),
    )
    username = models.CharField(max_length = 128)
    sqlcontent = models.CharField(max_length = 20000)
    treater = models.CharField(max_length = 128)
    condtion = models.CharField(max_length = 1,default = 1, choices = CONDTION_CHOICES)
    env = models.CharField(max_length = 1, blank = True, null = True, choices = GENDER_CHOICES)
    operate = models.CharField(max_length = 1, default=1,blank = True, null = True, choices = OPERATE_CHOICES)
    backid = models.CharField(max_length = 128,blank = True, null = True,)
    backdb = models.CharField(max_length = 128,blank = True, null = True,)




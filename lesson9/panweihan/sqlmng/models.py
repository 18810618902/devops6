# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    user = models.CharField(max_length=128)
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
                        (-3, u'已回滚'),
                        (-2, u'已暂停'),
                        (-1, u'待执行'),
                        (0, u'已执行'),
                        (1, u'已放弃'),
                        (2, u'执行失败'),
    )
    OPERATE_CHOICES = (
                        ('1', u'执行'),
                        ('2', u'拒绝'),
                        ('3', u'回滚'),
    )
    # 提交人名称
    commiter = models.CharField(max_length = 20,blank = True,null = True)
    # 数据库名
    dbname = models.CharField(max_length=20,blank = True,null = True)
    # 提交人在User表中的ID，多对一
    user_obj = models.ForeignKey(User,blank = True,null = True)
    # 提交的语句
    sqlcontent = models.TextField(blank = True, null = True)
    # 审核人
    treater = models.CharField(max_length = 128)
    # 语句目前状态
    condtion = models.IntegerField(default = -1, choices = CONDTION_CHOICES)
    # 数据库标识（测试、生产）
    env = models.CharField(max_length = 1, blank = True, null = True, choices = GENDER_CHOICES)
    # 提交语句的ID
    rollbackopid = models.TextField(blank=True, null=True)
    # 提交语句的目的表
    backdb = models.CharField(max_length = 100,blank = True, null = True,)
    # 代处理的人员
    daiwork = models.CharField(max_length = 20,blank = True,null = True)

# 扩展用户表
class UserProfile(models.Model):
    GENDER_CHOICES = (
                        ('0', u'无'),
                        ('1', u'总监'),
                        ('2', u'经理'),
                        ('3', u'研发'),
                    )
    user = models.OneToOneField(User, primary_key = True)         # 关联到User表
    phone = models.CharField(max_length = 11, default = '', blank = True)
    role = models.CharField(max_length = 1, default = '0', blank = True, choices = GENDER_CHOICES)
    note = models.CharField(max_length = 128, default = '', blank = True)

    def __unicode__(self):
        return self.role

@receiver(post_save, sender=User)       # 信号器，当User表完成修改后，启动后续代码
def create_save_user(sender, **kwargs):    # 修改userprofile表
    print kwargs
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if instance.is_superuser:
        return True
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()




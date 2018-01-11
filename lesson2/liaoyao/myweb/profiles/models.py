# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class UserProfile(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    phone = models.CharField(max_length=11, default='',blank=True,verbose_name='手机号码')
    address = models.CharField(max_length=128,default='',blank=True,verbose_name='地址')


    def __str__(self):
        return self.phone



@receiver(post_save,sender=User)
def create_save_user(sender,**kwargs):
    print('kwargs ==> {}'.format(kwargs))
    if kwargs['update_fields'] == frozenset([u'last_login']):return True
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

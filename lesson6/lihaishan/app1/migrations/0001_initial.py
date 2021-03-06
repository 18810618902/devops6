# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-06 19:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='\u540d\u5b57')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('note', models.TextField(blank=True, default='', null=True, verbose_name='\u5907\u6ce8')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='\u624b\u673a\u53f7\u7801')),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='\u540d\u5b57')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('note', models.TextField(blank=True, default='', null=True, verbose_name='\u5907\u6ce8')),
                ('price', models.IntegerField()),
                ('pub_date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name_plural': '\u56fe\u4e66',
            },
        ),
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='\u540d\u5b57')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65f6\u95f4')),
                ('note', models.TextField(blank=True, default='', null=True, verbose_name='\u5907\u6ce8')),
                ('city', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
    ]

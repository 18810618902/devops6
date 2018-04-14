#! /usr/bin/env python
# encoding: utf8

"""
@Author: liukai
@Date: 2018/4/11
"""

from .models import WorkOrder, WorkEchartsData

from celery import shared_task
import datetime
import json

print(datetime.datetime.now().date())


@shared_task
def send(**kwargs):
    work_queryset = WorkOrder.objects.filter(
        apply_time__gte=datetime.datetime.now().date())
    if work_queryset:
        name_list = list()
        for work in work_queryset:
            applicant = work.applicant
            if applicant not in name_list:
                name_list.append(applicant)
        data_list = list()
        web_list = list()
        task_list = list()
        config_list = list()
        other_list = list()
        name_ = list()
        print('name_list======>',name_list)
        for name in name_list:
            data = 0
            web = 0
            task = 0
            config = 0
            other = 0
            for work in work_queryset:
                if name == work.applicant:
                    if work.type == 0:
                        data += 1
                    elif work.type == 1:
                        web += 1
                    elif work.type == 2:
                        task += 1
                    elif work.type == 3:
                        config += 1
                    else:
                        other += 1
            data_list.append(data)
            web_list.append(web)
            task_list.append(task)
            config_list.append(config)
            other_list.append(other)
        for name in name_list:
            name_.append(name.username)
        data = {'name_list': name_, 'data_list': data_list,
                'web_list': web_list, 'task_list': task_list,
                'config_list': config_list, 'other_list': other_list}
    else:
        data = {}
    WorkEchartsData.objects.create(data=json.dumps(data))

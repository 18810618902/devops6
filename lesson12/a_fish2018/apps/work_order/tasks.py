# coding=utf8
from celery import platforms,task
from django.core.mail import send_mail
from django.conf import settings
from models import WorkOrder,Statistics
from datetime import datetime,timedelta
end_date = datetime.now() + timedelta(days=1)
start_date = datetime.now() - timedelta(days=7)

platforms.C_FORCE_ROOT = True


@task()
def add(x, y):
    return x + y

@task()
def mail(Title,Contents,From,To):
    send_mail(Title,
              Contents,
              From,
              To,
              )
    return 'ok'

@task()
def statistics():
    # 取出所有工单
    # a = WorkOrder.objects.all()
    # 取出所有提交者id
    uids = []
    for aa in WorkOrder.objects.all():
        uids.append(aa.applicant_id)
    uids = list(set(uids))
    # 查询每一个提交者最近一周提交的工单类型对应的数量
    for id in uids:
        wo = WorkOrder.objects.filter(applicant_id=id, apply_time__range=(start_date, end_date))
        a = wo.filter(type__exact=0).count()
        b = wo.filter(type__exact=1).count()
        c = wo.filter(type__exact=2).count()
        d = wo.filter(type__exact=3).count()
        e = wo.filter(type__exact=4).count()
        print 'id: %s --------' % id, a, b, c, d, e
        s = Statistics.objects.filter(applicant__exact=id)
        if s.exists():
            Statistics.objects.filter(applicant__exact=id).update(applicant=id, type0=a, type1=b, type2=c, type3=d,type4=e)
        else:
            Statistics.objects.create(applicant=id, type0=a, type1=b, type2=c, type3=d,type4=e)
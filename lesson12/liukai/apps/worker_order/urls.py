# _*_ coding: utf-8 _*_
from django.conf.urls import url
from .views import *
from worker_order.views import *

urlpatterns = [
    url('^apply/$', WorkOrderApplyView.as_view(), name='apply'),
    url('^list/$', WorkOrderListView.as_view(), name='list'),
    url('^detail/(?P<pk>[0-9]+)?/$', WorkOrderDetailView.as_view(),
        name='detail'),
    url('^history/$', WorkOrderHistoryView.as_view(), name='history'),
    url('^echarts/$', WorkEchartsView.as_view(), name='echarts'),
    url('^echarts_days/$', WorkEchartsDataView.as_view(), name='echarts_days'),

]

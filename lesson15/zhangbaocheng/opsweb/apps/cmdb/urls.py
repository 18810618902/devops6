# _*_ coding: utf-8 _*_
from django.conf.urls import url
from . import   views,product

urlpatterns = [

    url('^import_data/$', views.ImportDataView.as_view(), name='import_data'),
    url('^product_detail/(?P<pk>[0-9]+)?/$', product.ProductDetailView.as_view(), name='product_detail'),
    url('^product_add/$', product.ProductAddView.as_view(), name='product_add'),
    url('^hosts/$', views.HostListView.as_view(), name='host_list'),
    url('^hosts/(?P<pk>[0-9]+)?/$', views.HostEditView.as_view(), name='host_edit'),

]

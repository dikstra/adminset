#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from monitor import views

urlpatterns = [
    url(r'^monitor/$', views.index, name='monitor'),
    url(r'^monitor/host/tree/$', views.tree_node, name='host_tree'),
    url(r'^monitor/(?P<hostname>.+)/(?P<timing>\d+)/$', views.host_info, name='host_info'),
    url(r'^get/cpu/(?P<hostname>.+)/(?P<timing>\d+)/$', views.get_cpu, name='get_cpu'),
    url(r'^get/mem/(?P<hostname>.+)/(?P<timing>\d+)/$', views.get_mem, name='get_mem'),
    url(r'^open_monitor/(?P<hostname>.+)/(?P<timing>\d+)/$', views.open_monitor, name='open_monitor'),
    url(r'^close_monitor/(?P<hostname>.+)/(?P<timing>\d+)/$', views.close_monitor, name='close_monitor'),
]
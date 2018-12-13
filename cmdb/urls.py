#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from cmdb import api, asset, cloud , project


urlpatterns = [
    url(r'asset/$', asset.asset, name='cmdb'),
    url(r'^asset/add/$', asset.asset_add, name='asset_add'),
    url(r'^asset/del/$', asset.asset_del, name='asset_del'),
    url(r'^asset/edit/(?P<ids>\d+)/$', asset.asset_edit, name='asset_edit'),
    url(r'^asset/detail/(?P<ids>\d+)/$', asset.server_detail, name='server_detail'),
    url(r'^cloud/$', cloud.cloud, name='cloud'),
    url(r'^cloud/add/$', cloud.cloud_add, name='cloud_add'),
    url(r'^cloud/del/$', cloud.cloud_del, name='cloud_del'),
    url(r'^cloud/edit/(?P<cloud_id>\d+)/$', cloud.cloud_edit, name='cloud_edit'),
    url(r'^project/$', project.project, name='project'),
    url(r'^project/add/$', project.project_add, name='project_add'),
    url(r'^project/del/$', project.project_del, name='project_del'),
    url(r'^project/edit/(?P<project_id>\d+)/$', project.project_edit, name='project_edit'),
    # url(r'^cloud/edit/(?P<idc_id>\d+)/$', cloud.cloud_edit, name='cloud_edit'),
    url(r'^get/host/', api.get_host, name='get_host'),
]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
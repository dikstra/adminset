#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from webssh import views

urlpatterns = [
    url(r'^$', views.index_view, name='web'),
    url(r'^host/edit/(?P<ids>\d+)/$$', views.edit_view, name='webedit'),
    url(r'^webssh$', views.ssh_with_websocket, name='webssh'),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from accounts import user


urlpatterns = [
    # url(r'^$', user.user_list, name='accounts'),
    url(r'^login/$', user.login, name='login'),
    url(r'^logout/$', user.logout, name='logout'),
    url(r'^change/password/$', user.change_password, name='change_password'),
]
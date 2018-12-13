#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import models
from cmdb.models import Host


PROTOCOL = (
    (str(u"HTTP"), u"HTTP"),
    (str(u"HTTPS"), u"HTTPS"),
    (str(u"TCP"), u"TCP"),
    (str(u"TCP"), u"TCP"),
    (str(u"其它"), u"其它")
    )

class navi(models.Model):
    name = models.CharField(u"名称",max_length=50)
    description = models.CharField(u"描述",max_length=50)
    url = models.URLField(u"网址")

    def __str__(self):
        return self.name

class domain_manager(models.Model):
    domain=models.CharField(u"域名",max_length=50)
    ipaddress=models.GenericIPAddressField(u"域名对应ip", max_length=15,null=True)
    # backend_ip = models.ForeignKey(Host, verbose_name=u"后端内网IP", on_delete=models.SET_NULL, null=True, blank=True)
    protocol=models.CharField(u"协议", choices=PROTOCOL, max_length=30, blank=True)
    front_listen_port=models.CharField(u"前端侦听端口",max_length=50,null=True)
    back_end_port=models.CharField(u"后端侦听端口",max_length=50,null=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __str__(self):
        return self.domain

# class real_ip(models.Model):
#     vip = models.ForeignKey(domain_manager, verbose_name=u"vip", on_delete=models.SET_NULL, null=True, blank=True)
#     realip = models.ForeignKey(Host, verbose_name=u"内网IP", on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return self.realip

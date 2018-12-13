#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from cmdb.models import Host


class ssh_info(models.Model):
    public_ip=models.GenericIPAddressField(verbose_name=u"公网ip", null=True, blank=True)
    private_ip=models.GenericIPAddressField(verbose_name=u"私网ip", null=True, blank=True)
    # ids = models.ForeignKey(Host, to_field="id", on_delete=models.CASCADE, null=True, blank=True)
    ssh_port=models.CharField(u"ssh端口", max_length=30, default='22')
    ssh_user=models.CharField(u"ssh用户名",max_length=50,default='root')
    ssh_password=models.CharField(u"ssh登陆密码",max_length=50,null=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __str__(self):
        return self.ssh_password

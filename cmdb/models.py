#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
    )

ASSET_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器"),
    (str(4), u"其他")
    )


SYSTEM_TYPE = (
    (str(1), u"centos"),
    (str(2), u"ubuntu"),
    (str(3), u"redhat"),
    (str(4), u"windows server"),
    (str(5), u"windows plat"),
    (str(6), u"其他")
    )

CPU_NUM = (
    (str(1), u"1"),
    (str(2), u"2"),
    (str(3), u"4"),
    (str(4), u"8"),
    (str(5), u"16"),
    (str(6), u"32"),
    (str(7), u"64"),
    (str(8), u"其他")
    )

MEM_SIZE = (
    (str(1), u"1"),
    (str(2), u"2"),
    (str(3), u"4"),
    (str(4), u"8"),
    (str(5), u"16"),
    (str(6), u"32"),
    (str(7), u"64"),
    (str(8), u"其他")
    )

class UserInfo(models.Model):
    username = models.CharField(max_length=30,null=True)
    password = models.CharField(max_length=30,null=True)

    def __unicode__(self):
        return self.username


class Cloud(models.Model):
    cloud_ids = models.CharField(u"云服务提供商", max_length=255, unique=True,null=True)
    city = models.CharField(u"数据中心所在城市", max_length=100, blank=True)
    tech_tel = models.CharField(u"技术支持电话", max_length=30, blank=True)
    # contact = models.CharField(u"负责人", max_length=30, blank=True)
    # contact_phone = models.CharField(u"负责人电话", max_length=30, blank=True)
    domain = models.CharField(u"域名", max_length=30, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __str__(self):
        return self.cloud_ids

    class Meta:
        verbose_name = u"云服务商"
        verbose_name_plural = verbose_name

class Project(models.Model):
    project_name=models.CharField(u"项目名称", max_length=100, blank=True ,unique=True)
    cloud_address=models.ForeignKey(Cloud, verbose_name=u"项目位置", on_delete=models.CASCADE, null=True, blank=True)
    project_version=models.CharField(u"版本", max_length=30, blank=True)
    devolper_person = models.CharField(u"研发负责人", max_length=30, blank=True, unique=True)
    devops_person = models.CharField(u"运维负责人", max_length=30, blank=True )
    devops_phone = models.CharField(u"运维负责人电话", max_length=30, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __str__(self):
        return self.project_name

class Host(models.Model):
    id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=50, verbose_name=u"主机名")
    public_ip = models.GenericIPAddressField(u"公网IP", max_length=15,null=True,blank=True)
    private_ip=models.GenericIPAddressField(u"私有IP", max_length=15,null=True,blank=True)
    # cloud = models.ForeignKey(Cloud, to_field='cloud_ids',verbose_name=u"云服务提供商", on_delete=models.SET_NULL, null=True, blank=True)
    cloud = models.ForeignKey(Cloud, verbose_name=u"云服务提供商", on_delete=models.SET_NULL, null=True, blank=True)
    asset_type = models.CharField(u"设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField(u"操作系统", choices=SYSTEM_TYPE, max_length=30, blank=True)
    user_for= models.CharField(u"用途", max_length=100, blank=True)
    cpu_num = models.CharField(u"CPU数量", choices=CPU_NUM, max_length=100, blank=True)
    memory = models.CharField(u"内存大小", choices=MEM_SIZE, max_length=30, blank=True)
    hdd_disk = models.CharField(u"机械硬盘大小", max_length=255, blank=True)
    sdd_disk = models.CharField(u"固态硬盘大小", max_length=100, blank=True)
    # project = models.CharField(u"所属项目", max_length=100, blank=True)
    project=models.ForeignKey(Project, to_field='project_name', related_name="from_project_name", verbose_name=u"所属项目", on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.CharField(u"所属者", max_length=100, blank=True, null=True)
    ssh_port=models.CharField(u"SSH端口", max_length=30, default='22')
    ssh_user=models.CharField(u"SSH用户名",max_length=50,default='root')
    ssh_login_method=models.BooleanField(u"登陆方式",choices=((0,'密码登陆'),(1,'密钥登陆'),),default=0)
    # ssh_login=models.CharField(u"SSH用户名",max_length=50,default='root')
    ssh_password=models.CharField(u"SSH登陆密码",max_length=50,null=True)
    # ssh_cert = models.CharField(u"SSH登陆密钥", max_length=150, null=True)
    # owner = models.ForeignKey(Project, to_field='devolper_person',related_name="from_devolper_person",verbose_name=u"研发联系人", on_delete=models.SET_NULL, null=True, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __str__(self):
        return self.hostname

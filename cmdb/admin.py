#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from cmdb.models import Host, Cloud, UserInfo


class HostAdmin(admin.ModelAdmin):
    list_display = [
        'hostname',
        'public_ip',
        'private_ip',
        'os',
        # 'ssd_disk',
        'cpu_num',
        #'identity',
        ]

    # search_fields = ['cloud__cloud_ids']
class IpAdmin(admin.ModelAdmin):
    list_display = ['net',]


class CloudAdmin(admin.ModelAdmin):
    list_display = ['cloud_ids',
                    'city',
                    'tech_tel',
                    ]

    # search_fields = ['cloud_ids__name']

# class InterFaceAdmin(admin.ModelAdmin):
#     list_display = ['name',]

admin.site.register(Host, HostAdmin)
# admin.site.register(IpSource, IpAdmin)
admin.site.register(Cloud, CloudAdmin)
# admin.site.register(InterFace, InterFaceAdmin)
admin.site.register(UserInfo)
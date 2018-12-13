#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *

from .models import Host, Cloud, Project


class AssetForm(forms.ModelForm):


    class Meta:
        model = Host
        exclude = ("id",)
        widgets = {
            'hostname': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'public_ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;',}),
            'private_ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;','placeholder': u'必填项'}),
            'asset_type': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'status': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'os': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'user_for': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_num': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'memory': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'hdd_disk': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'sdd_disk': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            # 'cloud': Select(choices=AssetForm.set_choices, attrs={'class': 'form-control', 'style': 'width:530px;'}), #Select 方法不成功，不知道为什么
            'cloud': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'project': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'ssh_port': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'ssh_user': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'ssh_password': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'owner': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'memo': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:530px;'}),
        }


class CloudForm(forms.ModelForm):

    class Meta:
        model = Cloud
        exclude = ("id",)
        widgets = {
            'cloud_ids': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'city': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'tech_tel': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'domain': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'memo': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:530px;'}),
        }

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ("id",)

        widgets = {
            'project_name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'cloud_address': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'project_version': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'devolper_person': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'devops_person': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'devops_phone': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'memo': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:530px;'}),
        }

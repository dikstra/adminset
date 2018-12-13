#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *
from cmdb.models import Host

class WebsshForm(forms.ModelForm):

    class Meta:
        model = Host
        exclude = ("id",)
        # exclude = ()
        fields = ('public_ip','private_ip','ssh_port', 'ssh_user', 'ssh_password')
        widgets = {
            # 'public_ip': TextInput(attrs={'class': 'form-control','style': 'width:450px;','readonly': 'readonly' }),
            # 'private_ip': TextInput(attrs={'class': 'form-control','style': 'width:450px;','readonly': 'readonly' }),
            'public_ip': TextInput(attrs={'class': 'form-control','style': 'width:450px;' }),
            'private_ip': TextInput(attrs={'class': 'form-control','style': 'width:450px;' }),
            'ssh_port': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'ssh_user': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'ssh_password': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'memo': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:530px;'}),
        }

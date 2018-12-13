#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import navi, domain_manager
from django.forms.widgets import *


class navi_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(navi_form, self).clean()
        value = cleaned_data.get('name')
        try:
            navi.objects.get(name=value)
            self._errors['name']=self.error_class(["%s的信息已经存在" % value])
        except navi.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = navi
        exclude = ("id",)



class DomainForm(forms.ModelForm):

    class Meta:
        model = domain_manager
        exclude = ("id",)
        widgets = {
            'domain': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'ipaddress': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;','placeholder': u'必填项'}),
            'protocol': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'front_listen_port': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'back_end_port': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;','placeholder': u'必填项'}),
            'memo': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:530px;'}),
        }



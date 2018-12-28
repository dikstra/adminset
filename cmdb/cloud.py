#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from cmdb.forms import CloudForm
from .models import Cloud
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required()
def cloud(request):
    temp_name = "cmdb/cmdb-header.html"
    cloud_info = Cloud.objects.all()
    return render(request, 'cmdb/cloud.html', locals())


@login_required()
def cloud_add(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == "POST":
        cloud_form = CloudForm(request.POST)
        if cloud_form.is_valid():
            cloud_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "cmdb/cloud_base.html", locals())
    else:
        display_control = "none"
        cloud_form = CloudForm()
        return render(request, "cmdb/cloud_base.html", locals())


@login_required()
def cloud_del(request):
    temp_name = "cmdb/cmdb-header.html"
    cloud_id = request.GET.get('id', '')
    if cloud_id:
        Cloud.objects.filter(id=cloud_id).delete()
    if request.method == 'POST':
        cloud_items = request.POST.getlist('cloud_check', [])
        if cloud_items:
            for n in cloud_items:
                Cloud.objects.filter(id=n).delete()
    cloud_info = Cloud.objects.all()
    return render(request, "cmdb/cloud.html", locals())


@login_required()
def cloud_edit(request, cloud_id):
    project = Cloud.objects.get(id=cloud_id)
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        form = CloudForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cloud'))
    else:
        form = CloudForm(instance=project)
    display_control = "none"
    results = {
        'cloud_form': form,
        'cloud_id': cloud_id,
        'request': request,
        'temp_name': temp_name,
        'display_control': display_control,
    }
    return render(request, 'cmdb/cloud_base.html', results)

#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from cmdb.forms import ProjectForm
from .models import Project
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


@login_required()
def project(request):
    temp_name = "cmdb/cmdb-header.html"
    project_info = Project.objects.all()
    return render(request, 'cmdb/project.html', locals())


@login_required()
def project_add(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == "POST":
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "cmdb/project_base.html", locals())
        # return render(request, 'cmdb/cloud.html', locals())
    else:
        display_control = "none"
        project_form = ProjectForm()
        return render(request, "cmdb/project_base.html", locals())


@login_required()
def project_del(request):
    temp_name = "cmdb/cmdb-header.html"
    project_id = request.GET.get('id', '')
    if project_id:
        Project.objects.filter(id=project_id).delete()
    if request.method == 'POST':
        project_items = request.POST.getlist('project_check', [])
        if project_items:
            for n in project_items:
                Project.objects.filter(id=n).delete()
        project_info = Project.objects.all()
    return render(request, "cmdb/project.html", locals())


@login_required()
def project_edit(request, project_id):
    project = Project.objects.get(id=project_id)
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project'))
    else:
        form = ProjectForm(instance=project)
    display_control = "none"
    results = {
        'project_form': form,
        'project_id': project_id,
        'request': request,
        'temp_name': temp_name,
        'display_control': display_control,
    }
    return render(request, 'cmdb/project_base.html', results)

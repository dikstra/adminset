#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .models import navi, domain_manager
from .forms import DomainForm
from cmdb.api import pages, get_object
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required()
def index(request):
    temp_name = "navi/navi-header.html"
    domain_find = []
    # domain_info = domain_manager.objects.all()
    page_len = request.GET.get('page_len', '')
    keyword = request.GET.get('keyword', '')
    domain_ids = request.GET.get('domain', '')
    if domain_ids:
        domain_find =domain_manager.objects.filter(domain=domain_ids)
    else:
        domain_find=domain_manager.objects.all()
    if keyword:
        domain_find = domain_find.filter(Q(domain__contains=keyword)|Q(ipaddress__contains=keyword)|Q(protocol__contains=keyword))
    domain_list, p, domain, page_range, current_page, show_first, show_end, end_page = pages(domain_find, request)
    return render(request, "navi/index.html", locals())


@login_required()
def manage(request):
    temp_name = "navi/navi-header.html"
    # allnavi = navi.objects.all()
    return render(request, "navi/manage.html", locals())


@login_required()
def add(request):
    temp_name = "navi/navi-header.html"
    if request.method == "POST":
        a_form = DomainForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "navi/domain_add.html", locals())
    else:
        display_control = "none"
        a_form = DomainForm()
        return render(request, "navi/domain_add.html", locals())


@login_required()
def delete(request):
    domain_id = request.GET.get('id', '')
    if domain_id:
        domain_manager.objects.filter(id=domain_id).delete()
    if request.method == 'POST':
        domain_batch = request.GET.get('arg', '')
        domain_id_all = str(request.POST.get('asset_id_all', ''))
        if domain_batch:
            for asset_id in domain_id_all.split(','):
                asset_item = get_object(domain_manager, id=asset_id)
                asset_item.delete()
    return HttpResponse(u'删除成功')

@login_required()
def edit(request, domain_id):
    status = 0
    obj = get_object(domain_manager, id=domain_id)
    if request.method == 'POST':
        af = DomainForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = DomainForm(instance=obj)

    return render(request, 'navi/domain_edit.html', locals())
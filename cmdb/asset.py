#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from cmdb.api import get_object, pages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import HttpResponse, render
from cmdb.forms import AssetForm
from cmdb.models import ASSET_STATUS, ASSET_TYPE, Host, Cloud , Project

try:
    reload(sys)  # Python 2
    sys.setdefaultencoding('utf8')
except NameError:
    pass         # Python 3


@login_required()
def asset(request):
    temp_name = "cmdb/cmdb-header.html"
    asset_find = []
    cloud_info = Cloud.objects.all()
    asset_types = ASSET_TYPE
    asset_status = ASSET_STATUS
    cloud_ids = request.GET.get('cloud', '')
    page_len = request.GET.get('page_len', '')
    asset_type = request.GET.get('asset_type', '')
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')
    cloud_id = request.GET.get("cloud_id", '')
    asset_id_all = request.GET.getlist("id", '')
    if cloud_id:
        cloud = get_object(Cloud, id=cloud_id)
        if cloud:
            asset_find = Host.objects.filter(cloud=cloud)
    else:
        asset_find = Host.objects.all()
    if cloud_ids:
        asset_find = asset_find.filter(cloud__cloud_ids=cloud_ids)
    if asset_type:
        asset_find = asset_find.filter(asset_type__contains=asset_type)
    if status:
        asset_find = asset_find.filter(status__contains=status)
    if keyword:
        asset_find = asset_find.filter(Q(hostname__contains=keyword)|Q(public_ip__contains=keyword)|Q(private_ip__contains=keyword)|Q(project__project_name__contains=keyword)|Q(cloud__cloud_ids__contains=keyword))
    assets_list, p, assets, page_range, current_page, show_first, show_end, end_page = pages(asset_find, request)
    return render(request, 'cmdb/index.html', locals())

@login_required()
def asset_add(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == "POST":
        a_form = AssetForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render(request, "cmdb/asset_add.html", locals())
    else:
        display_control = "none"
        a_form = AssetForm()
        return render(request, "cmdb/asset_add.html", locals())


@login_required()
def asset_del(request):
    asset_id = request.GET.get('id', '')
    if asset_id:
        Host.objects.filter(id=asset_id).delete()

    if request.method == 'POST':
        asset_batch = request.GET.get('arg', '')
        asset_id_all = str(request.POST.get('asset_id_all', ''))

        if asset_batch:
            for asset_id in asset_id_all.split(','):
                asset_item = get_object(Host, id=asset_id)
                asset_item.delete()

    return HttpResponse(u'删除成功')


@login_required
def asset_edit(request, ids):
    status = 0
    asset_types = ASSET_TYPE
    obj = get_object(Host, id=ids)

    if request.method == 'POST':
        af = AssetForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = AssetForm(instance=obj)

    return render(request, 'cmdb/asset_edit.html', locals())


@login_required
def server_detail(request, ids):
    host = Host.objects.get(id=ids)
    return render(request, 'cmdb/server_detail.html', locals())

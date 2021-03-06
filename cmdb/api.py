#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from cmdb.models import Host
from django.core.paginator import Paginator, EmptyPage, InvalidPage


try:
    import json
except ImportError:
    import simplejson as json


def str2gb(args):
    """
    :参数 args:
    :返回: GB2312编码
    """
    return str(args).encode('gb2312')


def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None
    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object


def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 4 if current - 6 > 0 else 1
    max_page = min_page + 6 if min_page + 6 < total else total

    return range(min_page, max_page + 1)


def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """

    page_len = request.GET.get('page_len', '')
    if not page_len:
        page_len = 10
    paginator = Paginator(post_objects, page_len)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)
    end_page = len(paginator.page_range)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    # if current_page >= 5:
    #     show_first = 1
    # else:
    show_first = 0
    #
    # if current_page <= (len(paginator.page_range) - 3):
    #     show_end = 1
    # else:
    show_end = 0

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end, end_page

def get_host(request):
    d = []
    try:
        hostname = request.GET['name']
    except Exception as msg:
        return HttpResponse(msg, status=404)
    if hostname == "all":
        all_host = Host.objects.all()
        ret_host = {'hostname': hostname, 'members': []}
        for h in all_host:
            ret_h = {'hostname': h.hostname, 'ipaddr': h.ip}
            ret_host['members'].append(ret_h)
        d.append(ret_host)
        return HttpResponse(json.dumps(d))
    else:
        try:
            host = Host.objects.get(hostname=hostname)
            data = {'hostname': host.hostname, 'ip': host.ip}
            return HttpResponse(json.dumps({'status': 0, 'message': 'ok', 'data': data}))
        except Exception as msg:
            return HttpResponse(msg, status=404)

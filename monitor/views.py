#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from monitor.api import Get_sys_data
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from cmdb.models import Host
from django.views.decorators.csrf import csrf_exempt
import time
import json
import monitor.install_monitor as install_monitor
# Create your views here.

TIME_SECTOR = (
            3600,
            3600*3,
            3600*5,
            86400,
            86400*3,
            86400*7,
)

@login_required()
def index(request):
    temp_name = "monitor/monitor-header.html"
    all_host = Host.objects.all()
    return render(request, "monitor/index.html", locals())

@login_required()
def get_cpu_status(request, hostname, timing):
    data_time = []
    cpu_percent = []
    range_time = TIME_SECTOR[int(timing)]
    cpu_data = Get_sys_data(hostname, "cpu", range_time)
    for item in cpu_data.get_data():
        unix_time = item['timestamp']
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        c_percent = item['percent']
        cpu_percent.append(c_percent)
    data = {"data_time": data_time, "cpu_percent": cpu_percent}
    return HttpResponse(json.dumps(data))


def host_tree():
    host_node = []
    for host in Host.objects.all():
        data = {"name": host.hostname, "open": False, "children": "", 'url': "/monitor/monitor/{}/0/".format(host.hostname), 'target':"myframe" }
        host_node.append(data)
    return host_node

@login_required
@csrf_exempt
def tree_node(request):
    all_node = host_tree()
    return HttpResponse(json.dumps(all_node))


@login_required()
def host_info(request, hostname, timing):
    temp_name = "monitor/monitor-header.html"
    return render(request, "monitor/host_info.html", locals())


@login_required()
def open_monitor(request, hostname, timing):
    temp_name = "monitor/monitor-header.html"
    return render(request, "monitor/monitor_info.html", locals())

@login_required()
def close_monitor(request, hostname, timing):
    temp_name = "monitor/monitor-header.html"
    connect=install_monitor.ssh_connect(hostname)
    install_monitor.stop_process(connect)
    return render(request, "monitor/host_info.html", locals())

@login_required()
def get_cpu(request, hostname, timing):
    data_time = []
    cpu_percent = []
    range_time = TIME_SECTOR[int(timing)]
    cpu_data = Get_sys_data(hostname, "cpustat", range_time)
    for doc in cpu_data.get_data():
        unix_time = float(doc['timestamp']/1000)
        times = time.localtime(unix_time)
        dt = time.strftime("%m/%d-%H:%M", times)
        data_time.append(dt)
        c_percent = doc['percent']
        cpu_percent.append(c_percent)
    data = {"data_time": data_time, "cpu_percent": cpu_percent}
    return HttpResponse(json.dumps(data))


@login_required()
def get_mem(request, hostname, timing):
    data_time = []
    mem_used = []
    range_time = TIME_SECTOR[int(timing)]
    m_total=0
    mem_data = Get_sys_data(hostname, "memstat", range_time)
    for doc in mem_data.get_data():
        unix_time = float(doc['timestamp']/1000)
        times = time.localtime(unix_time)
        dt = time.strftime("%m/%d-%H:%M", times)
        data_time.append(dt)
        m_used = doc['used']
        m_total=doc['total']
        mem_used.append(m_used)
    data = {"data_time": data_time,"mem_used":mem_used,"m_total":m_total}
    print(data)
    return HttpResponse(json.dumps(data))

@login_required()
def get_partition(request, hostname, timing):
    data_time = []
    partitionname=[]
    partition_used=[]
    partition_total=[]
    range_time = int(timing)
    partition = Get_sys_data(hostname, "partitionstat", range_time)
    for doc in partition.get_data():
        unix_time = float(doc['timestamp'] / 1000)
        times = time.localtime(unix_time)
        dt = time.strftime("%m/%d-%H:%M", times)
        data_time.append(dt)
        m_total = doc['total']
        partition_name = doc['partition'].split(':')[1]
        partitionname.append(partition_name)
        p_used=doc['used']
        partition_used.append(p_used)
        partition_total.append(m_total)
    data = {"data_time": data_time, "partition_name": partitionname, "partition_used":partition_used,"partition_total":partition_total}
    return HttpResponse(json.dumps(data))

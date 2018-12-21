#! /usr/bin/env python
# -*- coding: utf-8 -*-
import time
import datetime
import re
import subprocess
import traceback
import json

from pymongo import MongoClient
from subprocess import Popen, PIPE

import psutil
import pkg_resources
from threading import Thread, Event
psutil_version = pkg_resources.get_distribution("psutil").version.split(".")[0]

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from monitor.daemon import Daemon
evt = Event()

configfile = "/etc/sysprobe.conf"
logfile = "/tmp/sysprobe.log"
runfile = "/tmp/sysprobe.pid"
hostname="172.31.16.38"

def handler(signum):
    print('Signal handler called with signal', signum)
    evt.set()

def pick_mem(hostname, db):
    print(str(datetime.datetime.now()), "-- Get Mem")
    sys.stdout.flush()
    res = psutil.virtual_memory()
    # convert to base
    mem4db = {
        "timestamp": int(round(time.time() * 1000)),
        "total": res.total,
        "used": res.used,
        "free": res.free,
        "buffers": res.buffers,
        "cached": res.cached,
        "host": hostname
    }
    mem_id = db.memstat.insert(mem4db)
    db.hosts.update({"_id": hostname}, {"$set": {"mem": mem_id }})
    print(mem4db)

def get_partitions(hostname):
    _partitions = psutil.disk_partitions()
    parts = []
    for p in _partitions:
        res = {"_id": hostname + ":" + p.device,
               "dev": p.device,
               "mountpoint": p.mountpoint,
               "fs": p.fstype,
               "stat": None
               }
        parts.append(res)
    print(parts)
    return parts

def pick_partitions_stat(hostname ,db):
    print(str(datetime.datetime.now()), "-- Pick Partition Stats")
    sys.stdout.flush()
    _partitions = psutil.disk_partitions()
    for p in _partitions:
        part_stat = psutil.disk_usage(p.mountpoint)
        res = {
            "timestamp": int(round(time.time() * 1000)),
            "total": part_stat.total,
            "used": part_stat.used,
            "free": part_stat.free,
            "partition": hostname + ":" + p.device
        }
        partstat_id = db.partitionstat.insert(res)
        db.partitions.update({"_id": hostname + ":" + p.device},{"$set": {"stat":partstat_id}})
    print(res)

def get_netcard():
    netcard_info=[]
    info = psutil.net_if_addrs()
    for k,v in info.items():
        for item in v:
            if item[0] == 2 and not item[1]=='127.0.0.1':
                netcard_info.append(k)
    print(netcard_info)
    for net in netcard_info:
        d_info = get_network_info(net)
        print("net info for net : %s, info :%s "%(net,d_info))

def objToDict(obj, attrs):
    dict_res = {}
    for attr in attrs:
        if hasattr(obj, attr):
            dict_res[attr] = getattr(obj, attr)
    return dict_res

# cpu stat
# def pick_cpu_stat(hostname, db):
#     print(str(datetime.datetime.now()), "-- Pick CPU Stats")
#     sys.stdout.flush()
#     cputimes = psutil.cpu_times()
#     cpus_stat = objToDict(cputimes,
#                           ["user", "system", "idle", "iowait", "irq", "softirq", "steal", "guest", "guest_nice"])
#     cpus_stat["timestamp"] = int(round(time.time() * 1000))
#     cpus_stat["host"] = hostname
#     cpus_stat_hostx_id = db.cpustat.insert(cpus_stat)
#     db.hosts.update({"_id": hostname}, {"$set": {"stat": cpus_stat_hostx_id }})
#     print(cpus_stat)

def pick_cpu_stat(hostname, db):
    print(str(datetime.datetime.now()), "-- Get CPU Percent")
    sys.stdout.flush()
    res = psutil.cpu_percent()
    # convert to base
    cpu_percent = {
        "timestamp": int(round(time.time() * 1000)),
        "percent": res,
        "host": hostname
    }
    cpuid = db.cpustat.insert(cpu_percent)
    db.hosts.update({"_id": hostname}, {"$set": {"cpupercent": cpuid}})
    print(cpu_percent)

    # cpus_stat_hostx_id = db.cpustat.insert(cpus_stat)
    # db.hosts.update({"_id": hostname}, {"$set": {"cpus_stat": cpus_stat_hostx_id }})

def get_network_info(interface):
    output = subprocess.Popen(['ip', 'addr', 'show', 'dev', interface], stdout=subprocess.PIPE).communicate()[0].decode().rsplit('\n')
    mtu = re.findall('mtu ([0-9]+) ', output[0])[0]
    link_ha = re.findall('link/(\w+) ([0-9a-fA-F:]+) ', output[1])[0]
    inet = None
    inet6 = None
    for line in output[2:]:
        if not inet:
            tinet = re.findall('inet ([0-9\.]+)/([0-9]+) ', line)
            if tinet:
                inet = {"addr": tinet[0][0], "mask": tinet[0][1]}
                continue
        if not inet6:
            tinet6 = re.findall('inet6 ([0-9a-fA-F:]+)/([0-9]+) ', line)
            if (tinet6):
                inet6 = {"addr": tinet6[0][0], "mask": tinet6[0][1]}
        if inet and inet6:
            break
    return {"mtu": int(mtu), "link": link_ha[0], "HWaddr": link_ha[1], "inet": inet, "inet6": inet6}

def get_sys_disk():
    print(str(datetime.datetime.now()), "-- GET Disk Stats")
    sys_disk = {}
    partition_info = []
    partitions = psutil.disk_partitions()
    for p in partitions:
        partition_info.append(parser_sys_disk(p.mountpoint))
    sys_disk = partition_info
    print(sys_disk)

def parser_sys_disk(mountpoint):
    partitions_list = {}
    d = psutil.disk_usage(mountpoint)
    partitions_list['mountpoint'] = mountpoint
    partitions_list['total'] = round(d.total/1024/1024/1024.0, 2)
    partitions_list['free'] = round(d.free/1024/1024/1024.0, 2)
    partitions_list['used'] = round(d.used/1024/1024/1024.0, 2)
    partitions_list['percent'] = d.percent
    return partitions_list

def get_disk_info():
    ret = []
    cmd = "fdisk -l|egrep '\/dev/[a-z]{3}\:'|awk -F '[:\t]' '{print $1}'|awk '{print $2}'"
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    for i in stdout.decode().split('\n'):
        if i:
            ret.append(i)
    print(ret)
    return ret

disk_stat_hdr = ["rrqm_s", "wrqm_s", "r_s", "w_s", "rkB_s", "wkB_s"]
def pick_disk_stat(hw_disks, hostname, db):
    print(str(datetime.datetime.now()), "-- Pick Disk Stats")
    sys.stdout.flush()
    p = subprocess.Popen(args=['iostat', '-dx'] + [d for d in hw_disks], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    outdata, errdata = p.communicate()
    if len(errdata):
        raise RuntimeError('unable to run iostat: %s' % errdata)
    lines = outdata.decode().rstrip().splitlines()
    for d in hw_disks:
        dev = re.findall('.*/([a-zA-Z0-9]+)', d)[0]
        iostat = [line for line in lines if re.match(dev + '.*', line)]
        if iostat:
            lineio = iostat[0].split()[1:]
            diskstat = dict([(k, float(v.replace(',', '.'))) for k, v in zip(disk_stat_hdr, lineio)])
            diskstat["disk"] = d
            diskstat["timestamp"] = int(round(time.time() * 1000))
            disk_stat_id = db.diskstat.insert(diskstat)
            db.disks.update({"_id": hostname }, {"$set": {"stat": disk_stat_id }})
            print(diskstat)

class Repeater(Thread):
    # period in second
    def __init__(self, event, function, args=[], period=5.0):
        Thread.__init__(self)
        self.stopped = event
        self.period = period
        self.function = function
        self.args = args

    def run(self):
        while not self.stopped.wait(self.period):
            try:
                # call a function
                self.function(*self.args)
            except Exception as e:
                # try later
                print(str(datetime.datetime.now()), "-- WARNING : " + self.function.__name__ + " did not worked : ", e)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback)
                pass

def load_conf():
    return json.load(open(configfile,'r'))

class SysProbeDaemon(Daemon):

    def __init__(self, pidfile):
        Daemon.__init__(self, pidfile, stdout=logfile, stderr=logfile)

    def run(self):
        self.start_probe()

    @staticmethod
    def start_probe():

        print(str(datetime.datetime.now()))
        print("SysProbe loading")
        # load conf
        data = load_conf()

        hb_refresh = data.get("hb_refresh", 5)
        print("hb_refresh = ", hb_refresh)

        mem_refresh = data.get("mem_refresh", 60)
        print("mem_refresh = ", mem_refresh)

        partition_refresh = data.get("partition_refresh", 60)
        print("partition_refresh = ", partition_refresh)

        cpu_refresh = data.get("cpu_refresh", 60)
        print("cpu_refresh = ", cpu_refresh)

        disk_refresh = data.get("disk_refresh", 60)
        print("disk_refresh = ", disk_refresh)

        mongodb_host = data.get("mongodb_host", None)
        print("mongodb_host = ", mongodb_host)

        mongodb_port = data.get("mongodb_port", None)
        print("mongodb_port = ", mongodb_port)

        cpu_window = data.get("cpu_window", 1200)
        print("cpu_window = ", cpu_window)

        mem_window = data.get("mem_window", 1200)
        print("mem_window = ", mem_window)

        disk_window = data.get("disk_window", 1200)
        print("disk_window = ", disk_window)

        partition_window = data.get("partition_window", 1200)
        print("partition_window = ", partition_window)


        print("version psutil = ", psutil_version, " (", psutil.__version__, ")")
        if (psutil.__version__ < "1.2.1"):
            print("ERROR : update your psutil to a earlier version (> 1.2.1)")
            sys.exit(2)

        sys.stdout.flush()
        import socket
        hostname = socket.gethostname()
        print("hostname = ", hostname)
        HWdisks=get_disk_info()

        client = MongoClient(mongodb_host, mongodb_port)

        db = client[hostname]

        data["_id"] = hostname
        db.sysprobe.remove({'_id': hostname})
        db.sysprobe.insert(data)

        # disk_thread = None
        # if disk_refresh > 0:
        #     disk_thread = Repeater(evt, get_sys_disk, [db], disk_refresh)
        #     disk_thread.start()

        part_thread = None
        if partition_refresh > 0:
            disk_thread = Repeater(evt, pick_partitions_stat, [hostname, db], partition_refresh)
            disk_thread.start()


        disk_thread = None
        if disk_refresh > 0:
            disk_thread = Repeater(evt, pick_disk_stat, [HWdisks, hostname, db], disk_refresh)
            disk_thread.start()

        mem_thread = None
        if mem_refresh > 0:
            mem_thread = Repeater(evt, pick_mem, [hostname, db], mem_refresh)
            mem_thread.start()

        cpu_thread = None
        if cpu_refresh > 0:
            cpu_thread = Repeater(evt, pick_cpu_stat, [hostname, db], cpu_refresh)
            cpu_thread.start()


        # drop thread
        cpu_db_drop_thread = None
        if cpu_window > 0:
            cpu_db_drop_thread = Repeater(evt, drop_stat, [db, "cpustat", cpu_window], cpu_window)
            cpu_db_drop_thread.start()

        mem_db_drop_thread = None
        if mem_window > 0:
            mem_db_drop_thread = Repeater(evt, drop_stat, [db, "memstat", mem_window], mem_window)
            mem_db_drop_thread.start()

        disk_db_drop_thread = None
        if disk_window > 0:
            disk_db_drop_thread = Repeater(evt, drop_stat, [db, "diskstat", disk_window], disk_window)
            disk_db_drop_thread.start()

        part_db_drop_thread = None
        if partition_window > 0:
            part_db_drop_thread = Repeater(evt, drop_stat, [db, "partitionstat", partition_window], partition_window)
            part_db_drop_thread.start()

        import signal
        signal.signal(signal.SIGTERM, handler)

        while not evt.isSet():
            evt.wait(600)

        print(str(datetime.datetime.now()))
        print("SysProbe stopped")


def drop_stat(db, collection, window):
    before = int((time.time() - window) * 1000)
    print(str(datetime.datetime.now()), "-- drop Stats:", collection, "before", before)
    db[collection].remove({"timestamp": {"$lt": before}})


if __name__ == "__main__":
    # pick_mem()
    # get_partitions(hostname)
    # pick_partitions_stat(hostname)
    # get_netcard()
    # get_sys_disk()
    # HWdisks = get_disk_info()
    # pick_disk_stat(HWdisks)
    daemon = SysProbeDaemon(runfile)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'status' == sys.argv[1]:
            daemon.status()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'nodaemon' == sys.argv[1]:
            SysProbeDaemon.start_probe()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart|status|nodaemon" % sys.argv[0])
        sys.exit(2)
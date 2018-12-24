#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from monitor.sysprobe import load_conf
from pymongo import MongoClient
import time

class Get_sys_data(object):

    # db = get_dir("mongodb_collection")

    def __init__(self, hostname, monitor_data, timing, no=0):
        self.hostname = hostname
        self.monitor_data = monitor_data
        self.timing = timing
        self.no = no

    @classmethod
    def connect_db(cls):
        data = load_conf()
        mongodb_ip = data.get("mongodb_host", None)
        mongodb_port = data.get("mongodb_port", None)
        client = MongoClient(mongodb_ip, mongodb_port)
        return client

    # def get_data(self,monitor_items):
    def get_data(self):
        client = self.connect_db()
        db = client[self.hostname]
        collection = db[self.monitor_data]
        now_time = int(time.time())
        find_time = (now_time-self.timing)*1000
        # cursor = collection.find({'timestamp': {'$gte': find_time}}, {self.monitor_data: 1, "timestamp": 1}).limit(self.no)
        # cursor=collection.find_one()
        # data={}
        # for item in monitor_items:
        #     pass
        cursor = collection.find({'timestamp': {'$gte': find_time}})
        return cursor

def get_cpu(hostname, timing):
    data_time = []
    cpu_percent = []
    range_time = int(timing)
    cpu_data = Get_sys_data(hostname, "cpustat", range_time)
    for doc in cpu_data.get_data():
        unix_time = float(doc['timestamp']/1000)
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        c_percent = doc['percent']
        cpu_percent.append(c_percent)
    data = {"data_time": data_time, "cpu_percent": cpu_percent}
    print(data)

def get_mem(hostname, timing):
    data_time = []
    mem_used = []
    range_time = int(timing)
    m_total=0
    mem_data = Get_sys_data(hostname, "memstat", range_time)
    for doc in mem_data.get_data():
        unix_time = float(doc['timestamp']/1000)
        times = time.localtime(unix_time)
        dt = time.strftime("%m%d-%H:%M", times)
        data_time.append(dt)
        m_used = doc['used']
        m_total=doc['total']
        mem_used.append(m_used)
    data = {"data_time": data_time,"mem_used":mem_used,"m_total":m_total}
    print(data)

if __name__ == "__main__":
    TIME_SECTOR = (
                # 3600,
                3600,
                3600*3,
                3600*5,
                86400,
                86400*3,
                86400*7,
    )

    range_time = TIME_SECTOR[0]
    hostname=r"szx1-personal-xiemengyun-dev-010"
    # # client = GetSysData.connect_db()
    # # db = client[GetSysData.db]
    # cpu_data = Get_sys_data(hostname, "cpustat", range_time)
    # import pdb;pdb.set_trace()
    # for doc in cpu_data.get_data():
    #     pass
    # print(cpu_data)
    # print("=========")
    #get_cpu(hostname,range_time)
    get_mem(hostname, range_time)
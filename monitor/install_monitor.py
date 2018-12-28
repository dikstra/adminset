#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminset.settings")
django.setup()
from cmdb.models import Host
from monitor.utils.sshclient import SSHConnection

def ssh_connect(hostname):
    host_info = Host.objects.filter(hostname=hostname)
    for items in host_info:
        host_publicip=items.public_ip
        host_privateip=items.private_ip
        host_password=items.ssh_password
        host_user=items.ssh_user
        host_port=items.ssh_port
        if host_password:
            if host_publicip:
                try:
                    sshclient=SSHConnection(hostip=host_publicip,port=host_port,username=host_user,password=host_password)
                except Exception as e:
                    print("Connecting host %s failed")%(str(host_publicip))
            elif host_privateip:
                try:
                    sshclient=SSHConnection(hostip=host_privateip,port=host_port,username=host_user,password=host_password)
                except Exception as e:
                    print("Connecting host %s failed") % (str(host_privateip))
            else:
                raise("host ip not found!")
        else:
            pass
    return sshclient

def judge_process_running(sshclient):
    cmd="ps aux|grep sysprobe|grep -v grep"
    try:
        rst=sshclient.exec_command(cmd)
        p = str(rst).find("sysprobe.py start")
        if not p == -1:
            print("sysprobe is running")
            return True
        else:
            print("sysprobe is not run")
            return False
    except Exception as e:
        print("exec command failed!")

def pre_install_process(sshclient):
    yum_command={
        "yum -y install python-devel",
        "yum -y install gcc"
    }
    pre_install_cmds={
        "pip install pymongo",
        "pip install psutil"
    }
    for cmd in yum_command:
        yum_result=sshclient.exec_command(cmd)
        a=str(yum_result).find("already")
        b=str(yum_result).find("Complete")
        p = max(a,b)
        if not p == -1:
            print("yum command is installed")
        else:
            print("yum command is install failed")
            return False
    for cmd in pre_install_cmds:
        rst=sshclient.exec_command(cmd)
        a=str(rst).find("already")
        b=str(rst).find("Successfully installed")
        p = max(a, b)
        if not p == -1:
            print("pip command is installed")
        else:
            print("pip command install failed")
            return False
    return True

def stop_process(sshclient):
    cmd="python /tmp/monitor/sysprobe.py stop"
    try:
        sshclient.exec_command(cmd)
    except Exception as e:
        print("stop sysprobe.py failed")

def start_process(sshclient):
    cmd="python /tmp/monitor/sysprobe.py start"
    try:
        sshclient.exec_command(cmd)
    except Exception as e:
        print("start sysprobe.py failed")

def judge_install(sshclient):
    cmd="ls /etc/sysprobe.conf"
    try:
        rst=sshclient.exec_command(cmd)
        p = str(rst).find("No such file or directory")
        if not p == -1:
            # print("sysprobe is installed")
            # return True
            print("sysprobe is not installed")
            return False
        else:
            # print("sysprobe is not installed")
            # return False
            print("sysprobe is installed")
            return True
    except Exception as e:
        print("exec command failed!")

def copy_sysprobe(sshclient):
    basedir=os.path.dirname(os.path.abspath(__file__))
    python_file = ["daemon.py","sysprobe.py","__init__.py"]
    try:
        rst = sshclient.exec_command("mkdir /tmp/monitor")
        for file in python_file:
            sshclient.put(os.path.join(basedir,file),os.path.join("/tmp/monitor/",file))
            print("put python file success")
        sshclient.put(os.path.join(basedir,"utils/sysprobe.conf"),"/etc/sysprobe.conf")
        print("put configure file sucess")
    except Exception as e:
        print("put file command failed!")

if __name__ == "__main__":
    # hostname="szx1-personal-xiemengyun-dev-010"
    hostname="192.168.5.25"
    # hostname="server01"
    #judge_process_running(hostname)
    connect=ssh_connect(hostname)
    installed=judge_install(connect)
    if installed:
        rst=judge_process_running(connect)
        if not rst:
            start_process(connect)
    else:
        rst=pre_install_process(connect)
        if rst:
            copy_sysprobe(connect)
            start_process(connect)
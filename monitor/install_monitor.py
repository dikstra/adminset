#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from cmdb.models import Host
from monitor.utils.sshclient import SSHConnection


# def judge_process_running(hostname, private_ip , ssh_password=None, public_ip=None, cert=None):
def judge_process_running(hostname):
    host_info = Host.objects.filter(hostname=hostname)
    host_publicip=host_info.public_ip
    host_privateip=host_info.private_ip
    host_password=host_info.ssh_password
    host_user=host_info.ssh_user
    host_port=host_info.ssh_port
    if host_password:
        if host_publicip:
            pass
        elif host_privateip:
            pass
        else:
            pass
    else:
        pass
    strtmp = os.popen("ps aux|grep sysprobe|grep -v grep")
    print(type(strtmp))
    cmdback=strtmp.read()
    p=str(cmdback).find("sysprobe.py start")
    if not p == -1:
        print("sysprobe is running")
        return True
    else:
        print("sysprobe is not run")
        return False

def install_process():
    pass

def stop_process():
    pass



if __name__ == "__main__":
    hostname="szx1-personal-xiemengyun-dev-010"
    judge_process_running(hostname)
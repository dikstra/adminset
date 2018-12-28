#! /usr/bin/env python
# -*- coding: utf-8 -*-
import paramiko

class SSHConnection(object):
    def __init__(self, hostip, port, username, password=None, cert=None):
        self._host = hostip
        self._port = int(port)
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._cert = cert
        self._connect()

    def _connect(self):
        transport = paramiko.Transport((self._host, self._port))
        if self._cert:
            transport.connect(username=self._username, pkey=self._cert)
        else:
            transport.connect(username=self._username, password=self._password)
        self._transport = transport

    def download(self, remotepath, localpath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remotepath, localpath)

    def put(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localpath, remotepath)


    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
            result=self._client.exec_command(command)
            print(result)
        stdin, stdout, stderr = self._client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            print(data.strip())
            return data
        err = stderr.read()
        if len(err) > 0:
            print(err.strip())
            return err

    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()
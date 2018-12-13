#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from gevent import monkey

from gevent.pywsgi import WSGIServer

from geventwebsocket.handler import WebSocketHandler
from adminset.wsgi import application

monkey.patch_all()

version = "1.0.0"

root_path=os.path.dirname(__file__)

parser = argparse.ArgumentParser(
    description="autodevops"
)

parser.add_argument('--port','-p',type=int,default=8080,help="服务端口，默认8080")

parser.add_argument('--host','-H',
                    default="0.0.0.0",
                    help='服务器IP，默认为0.0.0.0')

args=parser.parse_args()

print('autodevops{0} running on {1}:{2}'.format(version,args.host,args.port))
print(args.host,args.port)

ws_server = WSGIServer(
    (args.host,args.port),
    application,
    log=None,
    handler_class=WebSocketHandler,
)

try:
    ws_server.serve_forever()
except KeyboardInterrupt:
    print("服务器关闭")
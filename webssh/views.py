import time
from django.db.models import Q
from cmdb.api import get_object, pages
from django.shortcuts import render
from cmdb.models import Host
from django.contrib.auth.decorators import login_required
from .forms import WebsshForm
from .models import ssh_info

# Create your views here.

@login_required()
def index_view(request):
    temp_name = "webssh/webssh-header.html"
    keyword1="public_ip"
    keyword2="private_ip"
    keyword3="ssh_port"
    keyword4="ssh_user"
    keyword5="ssh_password"
    ipaddress = Host.objects.values('id',keyword1,keyword2,keyword3,keyword4,keyword5)[0:]
    # userinfo = ssh_info.objects.all()
    return render(request, 'webssh/index.html',locals())

@login_required()
def edit_view(request, ids):
    status = 0
    obj = get_object(Host, id=ids)
    if request.method == 'POST':
        af = WebsshForm(request.POST, instance=obj)
        if af.is_valid():
            af.save()
            status = 1
        else:
            status = 2
    else:
        af = WebsshForm(instance=obj)
        # import pdb;pdb.set_trace()

    return render(request, 'webssh/webssh_edit.html', locals())


from paramiko.ssh_exception import AuthenticationException, SSHException
from dwebsocket.decorators import require_websocket
from webssh.websocket_handler import WebSocketHandler
from webssh.utils.ioloop import IOLoop
from webssh.utils.data_type import ClientData
from webssh.exceptions import *

@require_websocket
def ssh_with_websocket(request):
    # import pdb;pdb.set_trace()
    ws_handler = WebSocketHandler(request)
    ws_handler.open()
    IOLoop.instance()
    code = 1000
    reason = None
    if not request.is_websocket():
        raise exceptions.requests.InvalidSchema()
    else:
        try:
            while not request.websocket.has_messages():
                time.sleep(0.1)

            for message in request.websocket:
                if str(message).find('\u0004') > -1:
                    break
                _send_message(message, ws_handler)

        except AuthenticationException as e:
            code = 4000
            reason = 'Authentication failed:' + str(e.message)

        except SSHException as e:
            code = 4001
            reason = 'SSHException:' + str(e.message)

        except SSHShellException as e:
            code = 4001
            reason = 'SSHShellException:' + str(e.message)

        except AttributeError:
            pass

        finally:
            ws_handler.close(code=code, reason=reason)


def _send_message(message, ws_handler):
    client_data = ClientData(message)
    bridge = ws_handler.get_client()

    if ws_handler._is_init_data(client_data):
        if ws_handler._check_init_param(client_data.data):
            try:
                bridge.open(client_data.data)
            except AuthenticationException as e:
                raise e

            except SSHException as e:
                raise e

    else:
        try:
            if bridge:
                bridge.trans_forward(client_data.data)

        except SSHShellException as e:
            raise e

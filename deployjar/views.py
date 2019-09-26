from django.shortcuts import render
import paramiko
from dwebsocket.decorators import accept_websocket
from .models import *

# Create your views here.
def index(request):
    list_app = Jarapp.objects.all()
    content = {'list_app':list_app}
    return render(request,'module.html',content)

def deploy(request,app_id):
    app = Jarapp.objects.get(pk=app_id)
    list_user = HostUser.objects.all()
    list_script = Script.objects.all()
    content = {'list_user': list_user, 'list_scripts': list_script,'app':app}
    return render(request, 'deploy.html', content)

@accept_websocket
def exec_deployment(request):
    for message in request.websocket:
        message = message.decode('utf-8')
        info = message.split('#')
        ips = info[0]
        jarurl = info[1]
        scriptname = info[2]
        user = info[3]
        jardir = info[4]
        port = info[5]
        houstuser = HostUser.objects.get(name=user)
        script = Script.objects.get(name=scriptname)

        if ips == 'undefined':
            request.websocket.send('请选择服务器！'.encode('utf-8'))
            request.websocket.send('over')
        elif not jarurl:
            request.websocket.send('请输入包 URL！'.encode('utf-8'))
            request.websocket.send('over')
        else:
            for ip in ips.split(','):
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                s.connect(hostname=ip, username=houstuser.name, password=houstuser.password, port=22)
                cmd = 'sh ' + script.script_dir + ' ' + jarurl + ' ' + jardir + ' ' + port + ' ' '2>&1'
                stdin, stdout, stderr = s.exec_command(cmd)
                nullcount = 0
                while True:
                    outline = stdout.readline().strip().encode('utf-8')
                    request.websocket.send(outline)
                    if not outline:
                        nullcount = nullcount + 1
                        if nullcount == 100:
                            break
                s.close()

            request.websocket.send('over')

from django.shortcuts import render
import paramiko
from dwebsocket.decorators import accept_websocket
from .models import *
from django.core.paginator import Paginator
import json
from common.views import check_port

def deploy(request):
    model_list = JarModel.objects.all()
    name = request.GET.get('name')
    env = request.GET.get('env')
    instances = Instance.objects.filter(name__name=name,host__env=env)

    return render(request, 'deploy.html', {'instances': instances, 'name':name, 'env': env, 'model_list':model_list})

@accept_websocket
def exec_deployment(request):
    for message in request.websocket:
        data = json.loads(s=message.decode('utf-8'))
        ints = data["ints"]
        jarurl = data["jarurl"]

        if len(ints) == 0:
            request.websocket.send('请选择服务器！'.encode('utf-8'))
        elif not jarurl:
            request.websocket.send('请输入包 URL！'.encode('utf-8'))
        else:
            for int_id in ints:
                int = Instance.objects.get(pk=int_id)
                script = Script.objects.get(name='deploy_jar')
                ip = int.host.ip
                port = '%d' %int.port
                jarname = int.package
                jar_dir = int.dir
                script_dir = script.script_dir
                username = script.user.name
                password = script.user.password

                stat = check_port(ip, 22)
                if stat:
                    s = paramiko.SSHClient()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                    s.connect(hostname=ip, username=username, password=password, port=22)
                    cmd = 'sh ' + script_dir + ' ' + username + ' ' + jarurl + ' ' + jarname + ' ' + jar_dir + ' ' + port + ' 2>&1'
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
                else:
                    msg = "服务器 %s 无法连接！" %ip
                    request.websocket.send(msg.encode('utf-8'))
        request.websocket.send('over')

@accept_websocket
def control(request):
    for message in request.websocket:
        data = json.loads(s=message.decode('utf-8'))
        ints = data["ints"]
        type= data["type"]

        if len(ints) == 0:
            request.websocket.send('请选择服务器！'.encode('utf-8'))
        else:
            for int_id in ints:
                int = Instance.objects.get(pk=int_id)
                script = Script.objects.get(name='control_jar')
                ip = int.host.ip
                port = '%d' %int.port
                jarname = int.package
                jar_dir = int.dir
                script_dir = script.script_dir
                username = script.user.name
                password = script.user.password

                stat = check_port(ip, 22)
                if stat:
                    s = paramiko.SSHClient()
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                    try:
                        s.connect(hostname=ip, username=username, password=password, port=22)
                    except Exception as e:
                        msg = "服务器 %s 无法登陆！" % ip
                        request.websocket.send(msg.encode('utf-8'))
                        continue
                    cmd = 'sh ' + script_dir + ' ' + type + ' ' + username + ' ' + jarname + ' '+ jar_dir + ' ' + port + ' 2>&1'
                    stdin, stdout, stderr = s.exec_command(cmd)
                    nullcount = 0
                    msg = "### 开始在服务器 %s 上开始执行！" %ip
                    request.websocket.send(msg.encode('utf-8'))
                    while True:
                        outline = stdout.readline().strip().encode('utf-8')
                        request.websocket.send(outline)
                        if not outline:
                            nullcount = nullcount + 1
                            if nullcount == 100:
                                break
                    s.close()
                else:
                    msg = "服务器 %s 无法连接！" %ip
                    request.websocket.send(msg.encode('utf-8'))
        request.websocket.send('over')
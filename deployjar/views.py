from django.shortcuts import render
import paramiko
from dwebsocket.decorators import accept_websocket
from .models import *
from django.core.paginator import Paginator
import json

def deploy(request):
    model_list = JarModel.objects.all()
    name = request.GET.get('name')
    env = request.GET.get('env')
    instances = Instance.objects.filter(name__name=name,host__env=env)

    return render(request, 'deploy.html', {'instances': instances, 'name':name, 'env': env, 'model_list':model_list})

@accept_websocket
def exec_deployment(request):
    for message in request.websocket:
        message = message.decode('utf-8')
        print(message)
        info = message.split('#')
        ips = info[0]
        jarurl = info[1]
        appname = info[2]

        # 获取包名
        jarapp = Jarapp.objects.get(name=appname)
        jarname = jarapp.jarname
        # 获取脚本路径
        script = Script.objects.get(name=jarapp.d_script)
        script_dir = script.script_dir
        # 获取用户名密码
        user = HostUser.objects.get(name=jarapp.user)
        username = user.name
        password = user.password
        # 端口号和路径
        port = '%d' % jarapp.port
        jar_dir = jarapp.jar_dir

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

                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                s.connect(hostname=ip, username=username, password=password, port=22)
                cmd = 'sh ' + script_dir + ' ' + type + ' ' + username + ' ' + jarname + ' '+ jar_dir + ' ' + port + ' 2>&1'
                stdin, stdout, stderr = s.exec_command(cmd)
                nullcount = 0
                msg = "### 开始在服务器 %s 上开始执行！" %ip
                request.websocket.send(msg.encode('utf-8'))
                print(cmd)
                while True:
                    outline = stdout.readline().strip().encode('utf-8')
                    request.websocket.send(outline)
                    if not outline:
                        nullcount = nullcount + 1
                        if nullcount == 100:
                            break
                s.close()
        request.websocket.send('over')
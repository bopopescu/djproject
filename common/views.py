from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from dwebsocket.decorators import accept_websocket
import paramiko
from deployjar.models import *
from django.core.paginator import Paginator
from .models import *
import socket
from django.http import JsonResponse
from django.views import View

from .form import FileForm
from .models import UploadFile
import json
# Create your views here.
def checkbackup(request):
    return render(request,'check_backup.html')

@accept_websocket
def execcheck(request):
    for message in request.websocket:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        s.connect(hostname='188.188.1.133', username='root', password='52R#jnFra%T1', port=22)
        cmd = 'sh /mntdisk/scripts/check_backup.sh 2>&1'
        stdin, stdout, stderr=s.exec_command(cmd)
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

def domain(request):
    porjects = Project.objects.all()
    paginator = Paginator(porjects, 3)
    page = request.GET.get('page')
    porject_list = paginator.get_page(page)
    return render(request,'domain.html',{'project_list':porject_list})

def host(request):
    type = request.GET.get('type')
    env = request.GET.get('env')
    if type == 'all' and env == 'all':
        host_list = Host.objects.all().order_by('-env','ip')
    elif type == 'all':
        host_list = Host.objects.filter(env=env).order_by('-type','ip')
    elif env == 'all':
        host_list = Host.objects.filter(type=type).order_by('-type','ip')
    else:
        host_list = Host.objects.filter(env=env, type=type)
    paginator = Paginator(host_list, 10)
    page = request.GET.get('page')
    hosts = paginator.get_page(page)
    return render(request,'host.html',{'hosts':hosts,'env':env,'type':type})

def instance(request):
    env = request.GET.get('env')
    if env == 'all':
        host_list = Host.objects.filter(type='java').order_by('-env')
    else:
        host_list = Host.objects.filter(env=env,type='java').order_by('-env')
    paginator = Paginator(host_list, 3)
    page = request.GET.get('page')
    hosts = paginator.get_page(page)
    return render(request, 'instance.html', {'hosts': hosts,'env':env})

def model(request):
    model_list = JarModel.objects.all()
    paginator = Paginator(model_list, 3)
    page = request.GET.get('page')
    models = paginator.get_page(page)
    return render(request, 'model.html', {'models': models})

def model_detail(request):
    name = request.GET.get('name')
    model = JarModel.objects.get(name=name)
    return render(request,'model_detail.html',{'model':model})

def project(request):
    project_list = Project.objects.all()
    return render(request,'project.html',{'project_list':project_list})

def project_detail(request,p_id):
    project = Project.objects.get(pk=p_id)
    return render(request,'project_detail.html',{'project':project})

def mysqldb(request):
    dbs = MySQLDB.objects.all()
    paginator = Paginator(dbs, 5)
    page = request.GET.get('page')
    db_list = paginator.get_page(page)
    return render(request,'mysqldb.html',{'db_list':db_list})

class UploadFilesView(View):
    def get(self, request):
        files_list = UploadFile.objects.all()
        return render(self.request, 'upload_files.html', {'files_list': files_list})

    def post(self, request):
        data = {'is_valid': True}
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            file.title = file.file.name
            file.save()
            update_files(file.file)
        else:
            data = {'is_valid': False}

        if data['is_valid']:
            s = paramiko.SSHClient()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            s.connect(hostname='188.188.1.141', username='tomcat', password='tomcat', port=22)
            cmd = 'sh /data/scripts/zip_baipao_template_files.sh 2>&1'
            s.exec_command(cmd)
        return JsonResponse(data)

def remove_file(request,f_id):
    file = UploadFile.objects.get(pk=f_id)
    name = file.file.name
    file.file.delete()
    file.delete()

    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    s.connect(hostname='188.188.1.141', username='tomcat', password='tomcat', port=22)
    s.exec_command('sh /data/scripts/zip_baipao_template_files.sh %s 2>&1' %name)
    return redirect('common:upload_files')

def update_files(name):
    host = '188.188.1.141'
    port = 22
    username = 'tomcat'
    password = 'tomcat'

    t = paramiko.Transport((host,port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.put('media/%s' %name,'/data/baipao/template/%s' %name)
    t.close()

def tasks(request):
    type = request.GET.get('type')
    env = request.GET.get('env')
    if type == 'all' and env == 'all':
        host_list = Host.objects.all().order_by('-env', 'ip')
    elif type == 'all':
        host_list = Host.objects.filter(env=env).order_by('-type', 'ip')
    elif env == 'all':
        host_list = Host.objects.filter(type=type).order_by('-type', 'ip')
    else:
        host_list = Host.objects.filter(env=env, type=type)
    paginator = Paginator(host_list, 10)
    page = request.GET.get('page')
    hosts = paginator.get_page(page)

    task_list = Task.objects.all()
    return render(request, 'tasks.html', {'hosts': hosts, 'env': env, 'type': type,'task_list':task_list})

@accept_websocket
def exec_tasks(request):
    for message in request.websocket:
        data = json.loads(s=message.decode('utf-8'))
        ips = data["ips"]
        tks = data["tks"]
        if len(ips) == 0 :
            request.websocket.send("请选择服务器！".encode('utf-8'))
        elif len(tks) == 0 :
            request.websocket.send("请选择任务！".encode('utf-8'))
        else:
            for ip in ips:
                host = Host.objects.get(ip=ip)
                stat = check_port(ip,22)
                if stat:
                    for t in tks:
                        task = Task.objects.get(pk=t)
                        script = task.script
                        user = str(task.user)

                        if user == 'root':
                            password = host.password
                        else:
                            password = task.user.password

                        s = paramiko.SSHClient()
                        s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                        try:
                            s.connect(hostname=ip, username=user, password=password, port=22)
                        except Exception as e:
                            msg = "服务器 %s 无法登陆！" %host.name
                            request.websocket.send(msg.encode('utf-8'))
                            continue
                        cmd = 'sh %s 2>&1' %script
                        stdin, stdout, stderr=s.exec_command(cmd)
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
                    msg = "服务器 %s 无法连接！" %host.name
                    request.websocket.send(msg.encode('utf-8'))
        request.websocket.send('over')

def check_port(ip,port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((ip, port))
        stat = True
    except Exception:
        stat = False
    sk.close()
    return stat

def config_file(request):
    project_list = Project.objects.all()
    return render(request,'config_file.html',{'project_list':project_list})
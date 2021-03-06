from django.shortcuts import render,redirect,HttpResponseRedirect,reverse
from django.views.decorators.csrf import csrf_exempt
from dwebsocket.decorators import accept_websocket
import paramiko
from deployjar.models import *
from django.core.paginator import Paginator
from .models import *
import socket
from django.http import JsonResponse
from django.views import View
import os
from .form import *
from .models import UploadFile
from djproject.settings import MEDIA_ROOT
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
    porjects = Project.objects.all().order_by('name')
    paginator = Paginator(porjects, 3)
    page = request.GET.get('page')
    porject_list = paginator.get_page(page)
    return render(request,'domain.html',{'project_list':porject_list})

def host(request,cmd,host_id):
    stat = 'success'
    object_type = '新增主机'
    form = HostForm()
    submit_uri = '/common/host/add/none/'
    back_uri = '/common/host/gets/none/'

    if request.method == 'POST':
        type_id = request.POST.get('type')
        type_name = HostType.objects.get(pk=type_id).name
        env = request.POST.get('env')
        if cmd == 'add':
            form = HostForm(request.POST)
            if form.is_valid():
                form.save()
                form = HostForm()
                stat = 'add'
            else:
                stat = 'error'
        elif cmd == 'save':
            stat = 'save'
            host = Host.objects.get(pk=host_id)
            form = HostForm(request.POST, instance=host)
            if form.is_valid():
                form.save()
                form = HostForm()
            else:
                object_type = '修改主机'
                stat = 'error'
                submit_uri = '/common/host/save/%s/' % host_id
    else:
        type_name = request.GET.get('type')
        env = request.GET.get('env')
        if cmd == 'gets':
            form = HostForm()
        elif cmd == 'get':
            stat = 'get'
            object_type = '修改主机'
            host = Host.objects.get(pk=host_id)
            form = HostForm(instance=host)
            submit_uri = '/common/host/save/%s/' % host_id

        elif cmd == 'del':
            stat = 'del'
            host = Host.objects.get(pk=host_id)
            host.delete()
            form = HostForm()

    if type_name == 'all' and env == 'all':
        host_list = Host.objects.all().order_by('-env','-created_at')
    elif type_name == 'all':
        host_list = Host.objects.filter(env=env).order_by('-created_at','ip')
    elif env == 'all':
        host_list = Host.objects.filter(type__name =type_name).order_by('-created_at','ip')
    else:
        host_list = Host.objects.filter(env=env, type__name=type_name)

    paginator = Paginator(host_list, 10)
    page = request.GET.get('page')
    hosts = paginator.get_page(page)

    type_list = HostType.objects.all()

    content = {'hosts':hosts,'env':env,'type':type_name,'type_list':type_list,'form': form,'object_type':object_type,'submit_uri':submit_uri,'stat':stat,'back_uri':back_uri}
    return render(request,'host.html',content)

def search_host(request):
    ip = request.GET.get('s_ip')
    type_name = 'all'
    env = 'all'
    stat = 'search'
    object_type = '新增主机'
    form = HostForm()
    submit_uri = '/common/host/add/none/'
    back_uri = '/common/host/gets/none/'

    host_list = Host.objects.filter(ip__contains=ip)

    paginator = Paginator(host_list, 10)
    page = request.GET.get('page')
    hosts = paginator.get_page(page)

    type_list = HostType.objects.all()

    content = {'hosts': hosts, 'env': env, 'type': type_name, 'type_list': type_list, 'form': form,
               'object_type': object_type, 'submit_uri': submit_uri, 'stat': stat, 'back_uri': back_uri,'ip':ip}
    return render(request, 'host.html', content)

def instance(request,cmd,instance_id):
    object_type = '新增 JAVA 实例'
    submit_uri = '/common/instance/add/none/'
    back_uri = '/common/instance/gets/none'
    stat = 'success'
    form = InstanceForm()
    host_list = ''

    if request.method == 'POST':
        host_id = request.POST.get('host')
        host = Host.objects.get(pk=host_id)
        env = host.env
        if cmd == 'add':
            stat = 'add'
            form = InstanceForm(request.POST)
            if form.is_valid():
                form.save()
                form = InstanceForm()
                host_list = Host.objects.filter(id = host_id)
            else:
                stat = 'error'
                host_list = Host.objects.filter(env=env, type__name='java').order_by('-env','ip')
        elif cmd == 'save':
            stat = 'save'
            inst = Instance.objects.get(pk=instance_id)
            form = InstanceForm(request.POST,instance=inst)
            if form.is_valid():
                form.save()
                form = InstanceForm()
                host_list = Host.objects.filter(id = host_id)
            else:
                stat = 'error'
                host_list = Host.objects.filter(env=env, type__name='java').order_by('-env','ip')
    else:
        env = request.GET.get('env')
        if cmd == 'gets':
            if env == 'all':
                host_list = Host.objects.filter(type__name='java').order_by('-env','ip')
            else:
                host_list = Host.objects.filter(env=env,type__name='java').order_by('-env','ip')
        else:
            if cmd == 'get':
                stat = 'get'
                object_type = '修改 JAVA 实例'
                ints = Instance.objects.get(pk=instance_id)
                form = InstanceForm(instance=ints)
                submit_uri = '/common/instance/save/%s/' % instance_id
            elif cmd == 'del':
                stat = 'del'
                ints = Instance.objects.get(pk=instance_id)
                ints.delete()
                form = InstanceForm()

            if env == 'all':
                host_list = Host.objects.filter(type__name='java').order_by('-env', 'ip')
            else:
                host_list = Host.objects.filter(env=env, type__name='java').order_by('-env', 'ip')

    paginator = Paginator(host_list, 3)
    page = request.GET.get('page')
    hosts = paginator.get_page(page)

    return render(request, 'instance.html', {'hosts': hosts,'env':env,'form':form,'object_type':object_type,'submit_uri':submit_uri,'stat':stat,'back_uri':back_uri})

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
    sftp.put('%s/%s' %(settings.MEDIA_ROOT,name),'/data/baipao/template/%s' %name)
    t.close()

def tasks(request):
    type = request.GET.get('type')
    env = request.GET.get('env')
    if type == 'all' and env == 'all':
        host_list = Host.objects.all().order_by('-env', 'ip')
    elif type == 'all':
        host_list = Host.objects.filter(env=env).order_by('-type', 'ip')
    elif env == 'all':
        host_list = Host.objects.filter(type__name=type).order_by('-type', 'ip')
    else:
        host_list = Host.objects.filter(env=env, type__name=type)
    paginator = Paginator(host_list, 10)
    page = request.GET.get('page')
    type_list = HostType.objects.all()
    hosts = paginator.get_page(page)

    task_list = Task.objects.all()
    return render(request, 'tasks.html', {'hosts': hosts, 'env': env, 'type': type,'task_list':task_list,'type_list':type_list})

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
                        type = task.type.cn_name

                        if user == 'root':
                            password = host.password
                        else:
                            password = task.user.password

                        # 传输脚本
                        t = paramiko.Transport((ip, 22))
                        try:
                            t.connect(username=user, password=password)
                            sftp = paramiko.SFTPClient.from_transport(t)
                            sftp.put('%s/scripts/' %settings.MEDIA_ROOT + type + '/' + script, '/tmp/%s' % script)
                        except Exception as e:
                            print(e)
                            msg = "在服务器 %s 上执行失败！" % host.name
                            request.websocket.send(msg.encode('utf-8'))
                            continue
                        t.close()

                        s = paramiko.SSHClient()
                        s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                        try:
                            s.connect(hostname=ip, username=user, password=password, port=22)
                        except Exception as e:
                            msg = "服务器 %s 无法登陆！" %host.name
                            request.websocket.send(msg.encode('utf-8'))
                            continue
                        cmd = 'sh /tmp/%s 2>&1' %script
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

@csrf_exempt
def open_file(request):
    project = request.POST.get("project")
    file_name = request.POST.get("file_name")

    path = '%s/%s/' %(MEDIA_ROOT,project)
    file_path = path + file_name
    p_stat = os.path.exists(path)
    f_stat = os.path.exists(file_path)
    content = ''

    if p_stat:
        if f_stat:
            with open(path + file_name, encoding='utf-8') as f:
                content = f.read()
        else:
            file = open(file_path, 'w',encoding='utf-8')
            file.close()
    else:
        os.makedirs(path)
        file = open(path + file_name,'w',encoding='utf-8')
        file.close()

    return JsonResponse({'content':content})

@csrf_exempt
def save_file(request):
    content = request.POST.get("content")
    project = request.POST.get("project")
    file_name = request.POST.get("file_name")

    path = '%s/%s/' %(MEDIA_ROOT,project)
    file_path = path + file_name
    p_stat = os.path.exists(path)

    if p_stat:
        file = open(file_path, 'w',encoding='utf-8')
        file.write(content)
        file.close()
    else:
        print('目录已经不存在')
        os.makedirs(path)
        file = open(path + file_name,'w',encoding='utf-8')
        file.write(content)
        file.close()

    return JsonResponse({'status':'success'})

@csrf_exempt
def del_file(request):
    project = request.POST.get("project")
    file_name = request.POST.get("file_name")
    c_file = ConfigFile.objects.get(project__name=project,file_name=file_name)
    c_file.delete()

    path = '%s/%s/' %(MEDIA_ROOT,project) + file_name
    stat = os.path.exists(path)

    if stat:
       os.remove(path)

    return JsonResponse({'status':'success'})

@csrf_exempt
def task_script(request):
    type_list = TaskType.objects.all()
    return render(request,'task_script.html',{'type_list':type_list})

@csrf_exempt
def open_script_file(request):
    type = request.POST.get("type")
    file_name = request.POST.get("file_name")

    path = '%s/scripts/%s/' % (settings.MEDIA_ROOT,type)
    file_path = path + file_name
    p_stat = os.path.exists(path)
    f_stat = os.path.exists(file_path)
    content = ''

    if p_stat:
        if f_stat:
            with open(path + file_name, encoding='utf-8') as f:
                content = f.read()
        else:
            file = open(file_path, 'w', encoding='utf-8')
            file.close()
    else:
        os.makedirs(path)
        file = open(path + file_name, 'w', encoding='utf-8')
        file.close()

    return JsonResponse({'content': content})

@csrf_exempt
def save_script_file(request):
    content = request.POST.get("content")
    type = request.POST.get("type")
    file_name = request.POST.get("file_name")

    path = '%s/scripts/%s/' %(settings.MEDIA_ROOT,type)
    file_path = path + file_name
    p_stat = os.path.exists(path)

    if p_stat:
        file = open(file_path, 'w',encoding='utf-8')
        file.write(content)
        file.close()
    else:
        print('目录已经不存在')
        os.makedirs(path)
        file = open(path + file_name,'w',encoding='utf-8')
        file.write(content)
        file.close()

    return JsonResponse({'status':'success'})

@csrf_exempt
def del_script_file(request):
    type = request.POST.get("type")
    file_name = request.POST.get("file_name")
    s_file = Task.objects.get(type__cn_name=type,script=file_name)
    s_file.delete()

    path = '%s/scripts/%s/' %(settings.MEDIA_ROOT,type) + file_name
    stat = os.path.exists(path)

    if stat:
       os.remove(path)

    return JsonResponse({'status':'success'})

def nginx_vhost(request):
    hostnames = NginxHostName.objects.all().order_by('hostname')

    paginator = Paginator(hostnames, 10)
    page = request.GET.get('page')
    host_name_list = paginator.get_page(page)

    return render(request,'nginx_vhost.html',{'host_name_list':host_name_list})

def mongodb(request):
    mongodbs = MongoDBDatabase.objects.all().order_by('name')

    paginator = Paginator(mongodbs, 5)
    page = request.GET.get('page')
    mongodb_list = paginator.get_page(page)

    return render(request, 'mongodb.html', {'mongodb_list': mongodb_list})

def redis(request):
    rds = RedisCluster.objects.all().order_by('name')

    paginator = Paginator(rds, 5)
    page = request.GET.get('page')
    redis_cluster_list = paginator.get_page(page)

    return render(request, 'redis.html', {'redis_cluster_list': redis_cluster_list})

def kafka(request):
    clusters = KafkaCluster.objects.all().order_by('name')

    paginator = Paginator(clusters, 5)
    page = request.GET.get('page')
    kafka_cluster_list = paginator.get_page(page)

    return render(request, 'kafka.html', {'kafka_cluster_list': kafka_cluster_list})

def zookeeper(request):
    clusters = ZookeeperCluster.objects.all().order_by('name')

    paginator = Paginator(clusters, 5)
    page = request.GET.get('page')
    zookeeper_cluster_list = paginator.get_page(page)

    return render(request, 'zookeeper.html', {'zookeeper_cluster_list': zookeeper_cluster_list})
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket
import paramiko
from deployjar.models import *
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *

# Create your views here.
def checkbackup(request):
    return render(request,'check_backup.html')

@accept_websocket
def execcheck(request):
    for message in request.websocket:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        s.connect(hostname='188.188.1.133', username='root', password='52R#jnFra%T1', port=22)
        cmd = 'sh /mntdisk/scripts/check_backup.sh'
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

def domain(request):
    return render(request,'domain.html')

def host(request):
    type = request.GET.get('type')
    env = request.GET.get('env')
    if type == 'all' and env == 'all':
        host_list = Host.objects.all().order_by('-env')
    elif type == 'all':
        host_list = Host.objects.filter(env=env).order_by('-type')
    elif env == 'all':
        host_list = Host.objects.filter(type=type).order_by('-type')
    else:
        host_list = Host.objects.filter(env=env, type=type)
    paginator = Paginator(host_list, 10)
    page = request.GET.get('page')
    hosts = paginator.get_page(page)
    return render(request,'host.html',{'hosts':hosts,'env':env,'type':type})

def instance(request):
    env = request.GET.get('env')
    if env == 'all':
        host_list = Host.objects.all().order_by('-env')
    else:
        host_list = Host.objects.filter(env=env).order_by('-env')
    paginator = Paginator(host_list, 3)
    page = request.GET.get('page')
    hosts = paginator.get_page(page)
    return render(request, 'instance.html', {'hosts': hosts,'env':env})

def model(request):
    model_list = JarModel.objects.all()
    paginator = Paginator(model_list, 5)
    page = request.GET.get('page')
    models = paginator.get_page(page)
    return render(request, 'model.html', {'models': models})

def project(request):
    project_list = Project.objects.all()
    return render(request,'project.html',{'project_list':project_list})

def project_detail(request,p_id):
    project = Project.objects.get(pk=p_id)
    return render(request,'project_detail.html',{'project':project})

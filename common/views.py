from django.shortcuts import render,redirect
from dwebsocket.decorators import accept_websocket
import paramiko
from deployjar.models import *
from django.core.paginator import Paginator
from .models import *

from django.http import JsonResponse
from django.views import View

from .form import FileForm
from .models import UploadFile

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
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            data = {'id':file.id,'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def remove_file(request,f_id):
    file = UploadFile.objects.get(pk=f_id)
    file.file.delete()
    file.delete()
    return redirect('common:upload_files')

@accept_websocket
def update_files(request):
    for message in request.websocket:
        file_list = UploadFile.objects.all()
        t = paramiko.Transport(('188.188.1.141', 22))
        t.connect(username='tomcat', password='tomcat')
        sftp = paramiko.SFTPClient.from_transport(t)
        for f in file_list:
            name = f.file
            sftp.put('media/%s' %name,'/tmp/upload/%s' %name)
        t.close()
        request.websocket.send('over')
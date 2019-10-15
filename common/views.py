from django.shortcuts import render
from dwebsocket.decorators import accept_websocket
import paramiko
from deployjar.models import *

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
    host_list = Host.objects.all()
    return render(request,'host.html',{'host_list':host_list})

def instance(request):
    host_list = Host.objects.all()
    return render(request, 'instance.html', {'host_list': host_list})

def model(request):
    model_list = JarModel.objects.all()
    return render(request,'model.html',{'model_list':model_list})

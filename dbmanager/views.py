from django.shortcuts import render
import paramiko
from dwebsocket.decorators import accept_websocket
from deployjar.models import *

# Create your views here.
def index(request):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    s.connect(hostname='188.188.1.133', username='root', password='52R#jnFra%T1', port=22)
    cmd = "ls -tl /backup/baipao/mysql/ | grep -v total | awk '{print $NF}' 2>&1"
    stdin, stdout, stderr = s.exec_command(cmd)
    content = stdout.readlines()
    s.close()
    return render(request, 'recovery.html', {'content':content})

@accept_websocket
def recovery(request):
    for message in request.websocket:
        message = message.decode('utf-8')
        filename = message
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        s.connect(hostname='188.188.1.133', username='root', password='52R#jnFra%T1', port=22)
        cmd = 'sh /mntdisk/scripts/recovery_mysql.sh %s 2>&1' %filename
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

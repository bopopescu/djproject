from django.shortcuts import render
import paramiko

# Create your views here.
def index(request):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    s.connect(hostname='188.188.1.133', username='root', password='52R#jnFra%T1', port=22)
    cmd = "ls -tl /backup/baipao/mysql/ | grep -v total | awk '{print $NF}' 2>&1"
    stdin, stdout, stderr = s.exec_command(cmd)
    content = stdout.readlines()
    s.close()
    return render(request,'recovery.html',{'content':content})
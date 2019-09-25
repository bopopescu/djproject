from django.db import models
from django.utils import timezone

# Create your models here.
class HostUser(models.Model):
    name = models.CharField('用户名', max_length=200, unique=True)
    password = models.CharField('密码', max_length=200)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '系统用户'
        verbose_name_plural = '系统用户'

    def __str__(self):
        return self.name

class Host(models.Model):
    version_list = [('CentOS 6','CentOS 6'),('CentOS 7','CentOS 7')]
    config_list = [('4C 8G 40G','4C 8G 40G'),('8C 16G 80G','8C 16G 80G'),('8C 32G 100G','8C 32G 100G')]
    position_list = [('阿里云','阿里云'),('电信机房','电信机房')]

    name = models.CharField('主机名',max_length=200,unique=True)
    ip = models.GenericIPAddressField('IP 地址',unique=True)
    version = models.CharField('版本',max_length=200,choices=version_list)
    config = models.CharField('配置',max_length=200,choices=config_list)
    position = models.CharField('位置',max_length=200,choices=position_list)
    hostuser = models.ForeignKey(HostUser,on_delete=models.CASCADE,verbose_name='系统管理员')
    created_at = models.DateTimeField('创建时间',default=timezone.now)

    class Meta:
        verbose_name = '主机'
        verbose_name_plural = '主机'

    def __str__(self):
        return self.ip

class Jarapp(models.Model):
    name = models.CharField('名称',max_length=200)
    host = models.ManyToManyField(Host,verbose_name='主机')
    port = models.IntegerField('端口号',default=8080)
    jar_dir = models.CharField('部署路径',max_length=200,default='/usr/local/jar8080')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '模块'
        verbose_name_plural = '模块'

    def __str__(self):
        return self.name

class Script(models.Model):
    name = models.CharField('名称',max_length=200)
    script_dir = models.CharField('路径',max_length=200,default='/data/scripts/deploy_jar.sh')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '脚本'
        verbose_name_plural = '脚本'

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone
from common.models import *

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

class HostType(models.Model):
    name = models.CharField('主机类别',max_length=200)

    class Meta:
        verbose_name = '主机类别'
        verbose_name_plural = '主机类别'

    def __str__(self):
        return self.name

class HostEnv(models.Model):
    en_name = models.CharField('英文名',max_length=200)
    cn_name = models.CharField('中文名',max_length=200)

    class Meta:
        verbose_name = '环境类型'
        verbose_name_plural = '环境类型'
    def __str__(self):
        return self.cn_name

class Host(models.Model):
    version_list = [('CentOS 6','CentOS 6'),('CentOS 7','CentOS 7'),('Windows 2008','Windows 2008')]
    config_list = [('4C 8G 40G','4C 8G 40G'),('8C 16G 80G','8C 16G 80G'),('8C 32G 100G','8C 32G 100G')]
    position_list = [('阿里云','阿里云'),('电信机房','电信机房'),('坪山机房','坪山机房')]
    env_list = [('test','测试环境'),('pro','生产环境')]
    type_list = [('nginx','nginx'),('java','java'),('mysql','mysql'),('redis','redis')]

    name = models.CharField('主机名',max_length=200,unique=True)
    ip = models.GenericIPAddressField('IP 地址',unique=True)
    version = models.CharField('版本',max_length=200,choices=version_list)
    config = models.CharField('配置',max_length=200,choices=config_list)
    position = models.CharField('位置',max_length=200,choices=position_list)
    hostuser = models.CharField('系统管理员',max_length=200,default='root')
    password = models.CharField('密码',max_length=200,default='bsbnet')
    type = models.CharField('类别',max_length=200,choices=type_list,default='java')
    env = models.CharField('环境',max_length=200,choices=env_list,default='test')
    created_at = models.DateTimeField('创建时间',default=timezone.now)

    class Meta:
        ordering = ['ip']
        verbose_name = '主机'
        verbose_name_plural = '主机'

    def __str__(self):
        return self.ip

class Script(models.Model):
    name = models.CharField('名称',max_length=200)
    script_dir = models.CharField('路径',max_length=200,default='/data/scripts/')
    user = models.ForeignKey(HostUser,on_delete=models.CASCADE,verbose_name='执行用户')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '脚本'
        verbose_name_plural = '脚本'

    def __str__(self):
        return self.name

class JarModel(models.Model):
    name = models.CharField('名称',max_length=200)
    manager = models.CharField('负责人',max_length=200)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='项目')
    created_at = models.DateTimeField('创建时间',default=timezone.now)

    class Meta:
        verbose_name = '模块'
        verbose_name_plural = '模块'

    def __str__(self):
        return self.name

class Instance(models.Model):
    name = models.ForeignKey(JarModel,on_delete=models.CASCADE,verbose_name='模块名')
    host = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='主机')
    port = models.IntegerField('端口号')
    package = models.CharField('包名',max_length=200)
    dir = models.CharField('部署路径',max_length=200,default='/usr/local/')
    created_at = models.DateTimeField('创建时间',default=timezone.now)

    class Meta:
        verbose_name = '实例'
        verbose_name_plural = '实例'

    def __str__(self):
        return self.host.ip + ':%s' %self.port

class MySQLInstance(models.Model):
    type_list = [('master','主节点'),('slave','从节点')]

    host = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='IP 地址')
    port = models.IntegerField('端口号',default=3306)
    dir = models.CharField('部署路径',max_length=200,default='/usr/local/mysql')
    version = models.CharField('版本',max_length=200,default='5.7')
    type = models.CharField('类型',max_length=200,choices=type_list)
    password = models.CharField('root 密码',max_length=200,default='111111')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'MySQL实例'
        verbose_name_plural = 'MySQL 实例'

    def __str__(self):
        return self.host.ip + ':%s' %self.port

class MySQLDB(models.Model):
    name = models.CharField('数据库名',max_length=200)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='项目')
    instance = models.ManyToManyField(MySQLInstance,verbose_name='MySQL 实例')
    dir = models.CharField('数据库路径',max_length=200,default='/usr/local/mysql/data')
    manager = models.CharField('管理员',max_length=200)
    user = models.CharField('用户名',max_length=200,default='dbuser')
    password = models.CharField('密码',max_length=200,default='111111')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'MySQL 数据库'
        verbose_name_plural = 'MySQL 数据库'

    def __str__(self):
        return self.name

class Domain(models.Model):
    project = models.ForeignKey(Project,verbose_name='项目',on_delete=models.CASCADE)
    name = models.CharField('名称',max_length=200)
    url = models.CharField('URL 地址',max_length=200)
    ip = models.CharField('外网 IP',max_length=200)
    nginx = models.ForeignKey(Host, verbose_name='Nginx 服务器', on_delete=models.CASCADE)
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    disc = models.CharField('备注',max_length=200,blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = '域名'
        verbose_name_plural = '域名'

    def __str__(self):
        return self.url

class Task(models.Model):
    name = models.CharField('名称',max_length=200)
    script = models.CharField('脚本',max_length=200,default='/data/scripts/')
    user = models.ForeignKey(HostUser,on_delete=models.CASCADE,verbose_name='执行用户')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'

    def __str__(self):
        return self.name

class ConfigFile(models.Model):
    file_name = models.CharField('文件名',max_length=200)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='项目')
    type = models.ForeignKey(HostType,on_delete=models.CASCADE,verbose_name='类别')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '配置文件'
        verbose_name_plural = '配置文件'
        ordering = ['file_name']
        unique_together = ['project', 'file_name']

    def __str__(self):
        return self.project.name +'-' + self.file_name
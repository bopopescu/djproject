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
        ordering = ['name']
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
    type = models.ForeignKey(HostType,verbose_name= '类别',on_delete=models.CASCADE)
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
    # host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机', limit_choices_to={'type__name': 'java'})
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

    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='IP 地址')
    # host = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='IP 地址',limit_choices_to={'type__name':'mysql'})
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
        verbose_name = '项目访问地址'
        verbose_name_plural = '项目访问地址'

    def __str__(self):
        return self.url

class TaskType(models.Model):
    en_name = models.CharField('英文名', max_length=200, unique=True)
    cn_name = models.CharField('中文名', max_length=200, unique=True)

    class Meta:
        verbose_name = '任务类别'
        verbose_name_plural = '任务类别'

    def __str__(self):
        return self.cn_name

class Task(models.Model):
    name = models.CharField('名称',max_length=200)
    script = models.CharField('脚本文件名',max_length=200)
    user = models.ForeignKey(HostUser,on_delete=models.CASCADE,verbose_name='执行用户')
    type = models.ForeignKey(TaskType,on_delete=models.CASCADE,verbose_name='类别')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务'
        ordering = ['-type__en_name']

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

class NginxHostName(models.Model):
    hostname = models.CharField('域名',max_length=200)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = '域名'
        verbose_name_plural = '域名'

    def __str__(self):
        return self.hostname

class NginxInstance(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机')
    # host = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='主机',limit_choices_to={'type__name':'nginx'})
    port = models.IntegerField('端口号',default=80)
    version = models.CharField('版本号',max_length=200,default='1.9')
    config_file = models.ForeignKey(ConfigFile,on_delete=models.CASCADE,verbose_name='主配置文件')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'NGINX 实例'
        verbose_name_plural = 'NGINX 实例'

    def __str__(self):
        return self.host.ip + ':' + str(self.port)

class NginxVhost(models.Model):
    protocol_list = [('http','http'),('https','https')]

    hostname = models.ForeignKey(NginxHostName,on_delete=models.CASCADE,verbose_name='Nginx 虚拟主机名')
    instance = models.ForeignKey(NginxInstance,on_delete=models.CASCADE,verbose_name='Nginx 实例')
    port = models.IntegerField('端口号',default=80)
    protocol = models.CharField('访问协议',max_length=200,choices=protocol_list,default='http')
    config_file = models.ForeignKey(ConfigFile,on_delete=models.CASCADE,verbose_name='配置文件')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'Nginx 虚拟主机'
        verbose_name_plural = 'Nginx 虚拟主机'

    def __str__(self):
        return self.hostname.hostname + ':' + str(self.instance.port)

class MongoDBCluster(models.Model):
    type_list = [('副本集','副本集'),('分片副本集','分片副本集')]
    name = models.CharField('集群名',max_length=200,unique=True)
    type = models.CharField('类型',max_length=200,choices=type_list)
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'MongoDB 集群'
        verbose_name_plural = 'MongoDB 集群'

    def __str__(self):
        return self.name

class MongoDBInstance(models.Model):
    role_list = [('primary','primary'),('secondary','secondary '),('arbiter','arbiter'),('route','route')]

    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机')
    # host = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='主机',limit_choices_to={'type__name':'mongodb'})
    port = models.IntegerField('端口号',default=27017)
    data_dir = models.CharField('数据目录',max_length=200,default='/usr/local/mongodb/data')
    config_file = models.ForeignKey(ConfigFile,on_delete=models.CASCADE,verbose_name='配置文件')
    shard = models.CharField('分片',max_length=200,blank=True)
    role = models.CharField('角色',max_length=200,choices=role_list)
    cluster = models.ForeignKey(MongoDBCluster,on_delete=models.CASCADE,verbose_name='集群')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'MongoDB 实例'
        verbose_name_plural = 'MongoDB 实例'

    def __str__(self):
        return self.host.ip + ':' + str(self.port)

class MongoDBDatabase(models.Model):
    name = models.CharField('数据库名',max_length=200,unique=True)
    user = models.CharField('用户',max_length=200,blank=True)
    password = models.CharField('密码',max_length=200,blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,verbose_name='项目')
    cluster = models.ForeignKey(MongoDBCluster,on_delete=models.CASCADE,verbose_name='集群')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'MongoDB 数据库'
        verbose_name_plural = 'MongoDB 数据库'

    def __str__(self):
        return self.name

class RedisCluster(models.Model):
    type_list = [('单实例','单实例'),('主从','主从'),('哨兵模式','哨兵模式')]

    name = models.CharField('集群名',max_length=200,unique=True)
    type = models.CharField('类别',max_length=200,choices=type_list)
    project = models.ManyToManyField(Project,verbose_name='项目使用')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'Redis 集群'
        verbose_name_plural = 'Redis 集群'

    def __str__(self):
        return self.name

class RedisInstance(models.Model):
    role_list = [('master','master'),('slave','slave')]

    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机')
    # host = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='主机',limit_choices_to={'type__name':'redis'})
    port = models.IntegerField('端口号',default=6379)
    role = models.CharField('角色',max_length=200,choices=role_list)
    cluster = models.ForeignKey(RedisCluster,on_delete=models.CASCADE,verbose_name='集群名')
    version = models.CharField('版本',max_length=200,default='4.0')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'Redis 实例'
        verbose_name_plural = 'Redis 实例'

    def __str__(self):
        return self.host.ip + ':' + str(self.port)

class KafkaCluster(models.Model):
    type_list = [('单实例','单实例'),('集群','集群')]

    name = models.CharField('集群名',max_length=200,unique=True)
    type = models.CharField('类别',max_length=200,choices=type_list)
    project = models.ManyToManyField(Project,verbose_name='项目使用')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'Kafka 集群'
        verbose_name_plural = 'Kafka 集群'

    def __str__(self):
        return self.name

class KafkaInstance(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机')
    # host = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='主机',limit_choices_to={'type__name':'kafka'})
    port = models.IntegerField('端口号',default=9092)
    cluster = models.ForeignKey(KafkaCluster,on_delete=models.CASCADE,verbose_name='集群名')
    version = models.CharField('版本',max_length=200,default='4.0')
    config_file = models.ForeignKey(ConfigFile,on_delete=models.CASCADE,verbose_name='配置文件')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'Kafka 实例'
        verbose_name_plural = 'Kafka 实例'

    def __str__(self):
        return self.host.ip + ':' + str(self.port)

class ZookeeperCluster(models.Model):
    type_list = [('单实例','单实例'),('集群','集群')]

    name = models.CharField('集群名',max_length=200,unique=True)
    type = models.CharField('类别',max_length=200,choices=type_list)
    project = models.ManyToManyField(Project,verbose_name='项目使用')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'Zookeeper 集群'
        verbose_name_plural = 'Zookeeper 集群'

    def __str__(self):
        return self.name

class ZookeeperInstance(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE, verbose_name='主机')
    # host = models.ForeignKey(Host,on_delete=models.CASCADE,verbose_name='主机',limit_choices_to={'type__name':'zookeeper'})
    port = models.IntegerField('端口号',default=2181)
    cluster = models.ForeignKey(ZookeeperCluster,on_delete=models.CASCADE,verbose_name='集群名')
    version = models.CharField('版本',max_length=200,default='4.0')
    config_file = models.ForeignKey(ConfigFile,on_delete=models.CASCADE,verbose_name='配置文件')
    created_at = models.DateTimeField('创建时间', default=timezone.now)

    class Meta:
        verbose_name = 'Zookeeper 实例'
        verbose_name_plural = 'Zookeeper 实例'

    def __str__(self):
        return self.host.ip + ':' + str(self.port)
# Generated by Django 2.2.5 on 2019-11-22 02:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20191022_1231'),
        ('deployjar', '0031_auto_20191121_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZookeeperInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField(default=6379, verbose_name='端口号')),
                ('version', models.CharField(default='4.0', max_length=200, verbose_name='版本')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.RedisCluster', verbose_name='集群名')),
                ('config_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.ConfigFile', verbose_name='配置文件')),
                ('host', models.ForeignKey(limit_choices_to={'type__name': 'zookeeper'}, on_delete=django.db.models.deletion.CASCADE, to='deployjar.Host', verbose_name='主机')),
            ],
            options={
                'verbose_name': 'Zookeeper 集群',
                'verbose_name_plural': 'Zookeeper 集群',
            },
        ),
        migrations.CreateModel(
            name='ZookeeperCluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='集群名')),
                ('type', models.CharField(choices=[('单实例', '单实例'), ('集群', '集群')], max_length=200, verbose_name='类别')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('project', models.ManyToManyField(to='common.Project', verbose_name='项目使用')),
            ],
            options={
                'verbose_name': 'Kafka 集群',
                'verbose_name_plural': 'Kafka 集群',
            },
        ),
        migrations.CreateModel(
            name='KafkaInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField(default=6379, verbose_name='端口号')),
                ('version', models.CharField(default='4.0', max_length=200, verbose_name='版本')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.RedisCluster', verbose_name='集群名')),
                ('config_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.ConfigFile', verbose_name='配置文件')),
                ('host', models.ForeignKey(limit_choices_to={'type__name': 'kafka'}, on_delete=django.db.models.deletion.CASCADE, to='deployjar.Host', verbose_name='主机')),
            ],
            options={
                'verbose_name': 'Kafka 实例',
                'verbose_name_plural': 'Kafka 实例',
            },
        ),
        migrations.CreateModel(
            name='KafkaCluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='集群名')),
                ('type', models.CharField(choices=[('单实例', '单实例'), ('集群', '集群')], max_length=200, verbose_name='类别')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('project', models.ManyToManyField(to='common.Project', verbose_name='项目使用')),
            ],
            options={
                'verbose_name': 'Kafka 集群',
                'verbose_name_plural': 'Kafka 集群',
            },
        ),
    ]

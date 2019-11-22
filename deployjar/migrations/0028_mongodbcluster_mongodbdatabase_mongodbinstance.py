# Generated by Django 2.2.5 on 2019-11-19 08:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20191022_1231'),
        ('deployjar', '0027_auto_20191118_1716'),
    ]

    operations = [
        migrations.CreateModel(
            name='MongoDBCluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='集群名')),
                ('type', models.CharField(choices=[('副本集', '副本集'), ('分片副本集', '分片副本集')], max_length=200, verbose_name='类型')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'MongoDB 集群',
                'verbose_name_plural': 'MongoDB 集群',
            },
        ),
        migrations.CreateModel(
            name='MongoDBInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField(default=27017, verbose_name='端口号')),
                ('data_dir', models.CharField(default='/usr/local/mongodb/data', max_length=200, verbose_name='数据目录')),
                ('shard', models.CharField(blank=True, max_length=200, verbose_name='分片')),
                ('role', models.CharField(choices=[('primary', 'primary'), ('secondary', 'secondary '), ('arbiter', 'arbiter')], max_length=200, verbose_name='角色')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.MongoDBCluster', verbose_name='集群')),
                ('config_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.ConfigFile', verbose_name='配置文件')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.Host', verbose_name='主机')),
            ],
            options={
                'verbose_name': 'MongoDB 实例',
                'verbose_name_plural': 'MongoDB 实例',
            },
        ),
        migrations.CreateModel(
            name='MongoDBDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='数据库名')),
                ('user', models.CharField(max_length=200, null=True, verbose_name='用户')),
                ('password', models.CharField(max_length=200, null=True, verbose_name='密码')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('cluster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.MongoDBCluster', verbose_name='集群')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Project', verbose_name='项目')),
            ],
            options={
                'verbose_name': 'MongoDB 数据库',
                'verbose_name_plural': 'MongoDB 数据库',
            },
        ),
    ]
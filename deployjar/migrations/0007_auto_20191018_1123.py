# Generated by Django 2.2.5 on 2019-10-18 03:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('deployjar', '0006_auto_20191017_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='MySQLDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='数据库名')),
            ],
        ),
        migrations.AlterModelOptions(
            name='host',
            options={'ordering': ['ip'], 'verbose_name': '主机', 'verbose_name_plural': '主机'},
        ),
        migrations.CreateModel(
            name='MySQLInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port', models.IntegerField(default=3306, verbose_name='端口号')),
                ('dir', models.CharField(default='/usr/local/mysql', max_length=200, verbose_name='部署路径')),
                ('version', models.CharField(default='5.7', max_length=200, verbose_name='版本')),
                ('type', models.CharField(choices=[('主节点', 'primary'), ('从节点', 'slave')], max_length=200, verbose_name='类型')),
                ('password', models.CharField(default='111111', max_length=200, verbose_name='root 密码')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='deployjar.Host', verbose_name='IP 地址')),
            ],
            options={
                'verbose_name': 'MySQL实例',
                'verbose_name_plural': 'MySQL 实例',
            },
        ),
    ]

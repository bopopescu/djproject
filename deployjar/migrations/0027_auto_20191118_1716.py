# Generated by Django 2.2.5 on 2019-11-18 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployjar', '0026_auto_20191118_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nginxvhost',
            options={'verbose_name': 'Nginx 虚拟主机', 'verbose_name_plural': 'Nginx 虚拟主机'},
        ),
        migrations.AddField(
            model_name='nginxvhost',
            name='protocol',
            field=models.CharField(choices=[('http', 'http'), ('https', 'https')], default='http', max_length=200, verbose_name='访问协议'),
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-26 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deployjar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jarapp',
            name='c_script',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='c_script', to='deployjar.Script', verbose_name='控制脚本'),
        ),
        migrations.AddField(
            model_name='jarapp',
            name='d_script',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='d_script', to='deployjar.Script', verbose_name='发布脚本'),
        ),
        migrations.AddField(
            model_name='jarapp',
            name='jarname',
            field=models.CharField(default=1, max_length=200, verbose_name='包名'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jarapp',
            name='jar_dir',
            field=models.CharField(default='/usr/local/jars', max_length=200, verbose_name='部署路径'),
        ),
    ]

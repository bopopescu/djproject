# Generated by Django 2.2.5 on 2019-10-31 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deployjar', '0013_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='deployjar.HostUser', verbose_name='执行用户'),
            preserve_default=False,
        ),
    ]

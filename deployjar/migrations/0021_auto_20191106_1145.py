# Generated by Django 2.2.5 on 2019-11-06 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deployjar', '0020_auto_20191106_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='deployjar.TaskType', verbose_name='类别'),
            preserve_default=False,
        ),
    ]
# Generated by Django 2.2.5 on 2019-10-22 03:53

import common.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20191021_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(storage=common.models.OverwriteStorage(), upload_to=''),
        ),
    ]

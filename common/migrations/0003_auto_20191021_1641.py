# Generated by Django 2.2.5 on 2019-10-21 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_uploadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfile',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]

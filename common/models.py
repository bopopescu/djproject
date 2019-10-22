from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

# Create your models here.
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            f = UploadFile.objects.get(title=name)
            f.delete()
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class Project(models.Model):
    name = models.CharField('名称',max_length=200)
    manager = models.CharField('负责人',max_length=200)
    created_at = models.DateTimeField('创建时间',default=timezone.now)
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'

    def __str__(self):
        return self.name

class UploadFile(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='',storage=OverwriteStorage())
    uploaded_at = models.DateTimeField(auto_now_add=True)
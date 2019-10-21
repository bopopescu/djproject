from django.db import models
from django.utils import timezone

# Create your models here.
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
    file = models.FileField(upload_to='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
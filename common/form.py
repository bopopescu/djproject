from .models import UploadFile
from django import forms
from deployjar.models import *

class FileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('file','title')

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = '__all__'

class InstanceForm(forms.ModelForm):
    class Meta:
        model = Instance
        fields = '__all__'

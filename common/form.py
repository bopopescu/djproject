from .models import UploadFile
from django import forms

class FileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('file','title')
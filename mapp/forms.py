

#https://coderwall.com/p/bz0sng/simple-django-image-upload-to-model-imagefield
from django import forms
from .models import Datos
class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Datos
        fields = ['imagen']
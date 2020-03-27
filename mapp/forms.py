

#https://coderwall.com/p/bz0sng/simple-django-image-upload-to-model-imagefield
from django import forms

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
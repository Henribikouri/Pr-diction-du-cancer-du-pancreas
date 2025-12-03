# image_processing/forms.py
# from django import forms
from .models import ProcessedImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = ProcessedImage
        fields = ['patient', 'image_file', 'result']
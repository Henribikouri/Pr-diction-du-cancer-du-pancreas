from django import forms
from .models import Patient, Image, Report

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'date_of_birth', 'diagnosis']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['patient', 'image_file']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['patient', 'summary', 'report_file']

from django.db import models
from patient_records.models import Patient

class AnalysisReport(models.Model):
    patient = models.ForeignKey(Patient, related_name='analysis_reports', on_delete=models.CASCADE)
    summary = models.TextField()
    report_file = models.FileField(upload_to='analysis_reports/')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis Report for {self.patient.name}"

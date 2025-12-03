from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    diagnosis = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    patient = models.ForeignKey(Patient, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='patient_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.patient.name}"

class Report(models.Model):
    patient = models.ForeignKey(Patient, related_name='reports', on_delete=models.CASCADE)
    summary = models.TextField()
    report_file = models.FileField(upload_to='reports/')
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.patient.name}"

from django.db import models
from patient_records.models import Patient

class ProcessedImage(models.Model):
    patient = models.ForeignKey(Patient, related_name='processed_images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='processed_images/')
    result = models.CharField(max_length=255)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Processed Image for {self.patient.name}"

"""from django.db import models

class ProcessedImage(models.Model):
    patient_id = models.IntegerField()  # ID du patient
    image_file = models.ImageField(upload_to='processed_images/')  # L'image téléchargée
    result = models.CharField(max_length=255)  # Résultat du traitement, par exemple : "Cancer détecté"

    def __str__(self):
        return f"Image traitée pour le patient {self.patient_id} - Résultat: {self.result}" """

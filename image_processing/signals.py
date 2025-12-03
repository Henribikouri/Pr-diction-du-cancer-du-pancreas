from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProcessedImage
import requests

@receiver(post_save, sender=ProcessedImage)
def generate_report_on_image_processing(sender, instance, created, **kwargs):
    if created:
        # Appel à l'API de `data_analysis` pour générer un rapport après traitement de l'image
        response = requests.post(f'http://localhost:8000/api/reports/{instance.patient_id}/', data={'result': instance.result})
        if response.status_code == 200:
            print("Rapport généré avec succès")
        else:
            print("Erreur dans la génération du rapport")

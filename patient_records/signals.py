from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Patient
from data_analysis.models import AnalysisReport

@receiver(post_save, sender=Patient)
def create_initial_report(sender, instance, created, **kwargs):
    if created:
        AnalysisReport.objects.create(
            patient=instance,
            summary="Rapport initial créé automatiquement pour le patient."
        )

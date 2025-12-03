from .models import ProcessedImage
from patient_records.models import Patient

def analyze_image(patient_id, image_file):
    patient = Patient.objects.get(id=patient_id)
    # Exemple d'analyse (dummy processing)
    result = f"L'image pour {patient.name} a été analysée avec succès."
    processed_image = ProcessedImage.objects.create(
        patient=patient,
        image_file=image_file,
        result=result
    )
    return processed_image

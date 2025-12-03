from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from rest_framework.response import Response
import requests
import logging
from PIL import Image, ImageEnhance
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import numpy as np
import os
from patient_records.models import Patient  # Import du modèle Patient
from .models import ProcessedImage, Patient
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageForm


# Charger le modèle une seule fois
model_path = "cancer_detection_model.h5"
if os.path.exists(model_path):
    model = load_model(model_path)
else:
    raise FileNotFoundError(f"Le fichier de modèle {model_path} est introuvable. Veuillez vérifier son emplacement.")


# Fonction de prétraitement de l'image
def preprocess_image(image_file):
    """
    Fonction de prétraitement d'image avec des améliorations.
    1. Redimensionne l'image.
    2. Améliore la luminosité.
    3. Applique une normalisation.
    """
    try:
        # Charger l'image
        image = load_img(image_file, target_size=(224, 224))

        # Amélioration de la luminosité (optionnelle)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)  # Augmenter la luminosité de 20%

        # Convertir en tableau numpy
        image_array = img_to_array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        # Normaliser pour correspondre à l'entrée du modèle
        image_array = preprocess_input(image_array)

        return image_array
    except Exception as e:
        raise ValueError(f"Erreur lors du prétraitement de l'image : {e}")


# API de prédiction d'image
def predict_image(request):
    """
    Fonction qui prédit le résultat de l'image uploadée.
    """
    if request.method == "POST" and request.FILES.get("image"):
        try:
            # Récupérer l'image uploadée
            image_file = request.FILES["image"]

            # Prétraiter l'image avant de la passer au modèle
            image_array = preprocess_image(image_file)

            # Prédire avec le modèle
            prediction = model.predict(image_array)
            label = "Cancer" if np.argmax(prediction) == 1 else "Non Cancer"

            return JsonResponse({"prediction": label})

        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Une erreur est survenue lors de la prédiction."}, status=500)

    return JsonResponse({"error": "Veuillez fournir une image."}, status=400)


# API pour obtenir les images d'un patient
@api_view(['GET'])
def get_images_for_patient(request, patient_id):
    """
    Retourne toutes les images traitées pour un patient donné.
    """
    try:
        images = ProcessedImage.objects.filter(patient_id=patient_id)
        if not images:
            return JsonResponse({"error": "Aucune image trouvée pour ce patient."}, status=404)

        data = [{'id': img.id, 'result': img.result, 'file_url': img.image_file.url} for img in images]
        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"error": f"Erreur lors de la récupération des images : {e}"}, status=500)


# Configuration du logger
logger = logging.getLogger(__name__)

# Traitement d'image et génération de rapport
@csrf_exempt
def process_image(request, patient_id):
    """
    Fonction qui permet de traiter l'image et de générer un rapport pour un patient.
    """
    try:
        # Vérifier la présence de l'image dans la requête
        image_file = request.FILES.get('image')
        if not image_file:
            return JsonResponse({'status': 'error', 'message': 'Aucune image fournie'}, status=400)

        # Vérifier si le patient existe
        patient = get_object_or_404(Patient, id=patient_id)

        # Vérifier si le fichier est une image valide
        try:
            image = Image.open(image_file)
            image.verify()  # Vérifie si l'image est valide
        except (IOError, SyntaxError):
            return JsonResponse({'status': 'error', 'message': 'Fichier non valide. Veuillez télécharger une image.'}, status=400)

        # Vérifier si le type de fichier est valide (par exemple, seulement jpg, png, jpeg)
        if not image_file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            return JsonResponse({'status': 'error', 'message': 'Format de fichier non pris en charge'}, status=400)

        # Sauvegarder temporairement l'image
        image_path = default_storage.save(f'uploads/{image_file.name}', image_file)

        # Traitement de l'image (exemple fictif de résultat)
        result = "Cancer du pancréas détecté"  # Exemple pour le test

        # Enregistrer l'image traitée dans la base de données
        processed_image = ProcessedImage.objects.create(
            patient=patient,
            image_file=image_path,
            result=result
        )

        # Journalisation du téléchargement réussi de l'image
        logger.info(f"Image {image_file.name} téléchargée avec succès pour le patient {patient_id}")

        # Appeler une API pour générer un rapport
        response = requests.post(
            f'http://localhost:8000/api/reports/{patient_id}/',
            data={'result': result},
            files={'report_file': image_file}
        )

        # Vérifier la réponse de l'API
        if response.status_code == 200:
            return JsonResponse({'status': 'success', 'result': processed_image.result})
        else:
            logger.error(f"Erreur dans la génération du rapport : {response.text}")
            return JsonResponse({'status': 'error', 'message': f"Erreur dans la génération du rapport : {response.text}"}, status=500)

    except Exception as e:
        logger.error(f"Erreur lors du traitement de l'image pour le patient {patient_id}: {e}")
        return JsonResponse({'status': 'error', 'message': f"Erreur lors du traitement de l'image : {e}"}, status=500)



def image_processing(request):
    """
    Vue qui rend le template image_processing.html et traite la soumission de l'image.
    """
    patients = Patient.objects.all()  # Récupérer tous les patients de la base de données
    selected_patient_id = request.GET.get('patient_id', None)

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        image_file = request.FILES.get('image')

        # Vérifier si l'image est fournie et que le patient est sélectionné
        if not patient_id or not image_file:
            return JsonResponse({'status': 'error', 'message': 'Veuillez sélectionner un patient et télécharger une image.'}, status=400)

        # Récupérer le patient sélectionné
        patient = Patient.objects.get(id=patient_id)

        # Sauvegarder l'image téléchargée
        image_path = default_storage.save(f'uploads/{image_file.name}', image_file)

        # Ici, vous pouvez ajouter le traitement de l'image comme vous le souhaitez
        # Par exemple, vous pouvez passer l'image à votre modèle pour faire des prédictions

        # Rediriger vers la page de traitement de l'image avec le patient et l'image sauvegardés
        return redirect('process_image', patient_id=patient.id)

    return render(request, 'image_processing/image_processing.html', {
        'patients': patients,
        'selected_patient_id': selected_patient_id
    })




def add_processed_image(request, patient_id):
    """
    Vue pour ajouter une image traitée pour un patient.
    """
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES)
        
        if image_form.is_valid():
            # Sauvegarder l'image
            new_image = image_form.save(commit=False)
            new_image.patient = patient  # Associer l'image au patient
            new_image.save()
            return redirect('patient_details', patient_id=patient.id)
    else:
        image_form = ImageForm()

    return render(request, 'add_image.html', {'image_form': image_form, 'patient': patient})

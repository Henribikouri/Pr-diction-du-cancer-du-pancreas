from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Patient
from .forms import PatientForm
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientSerializer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def patient_details(request, patient_id):
    """
    Vue pour afficher les détails d'un patient, les images traitées et les rapports d'analyse.
    """
    # Récupérer le patient ou renvoyer une 404
    patient = get_object_or_404(Patient, id=patient_id)

    # Appel API pour récupérer les images traitées
    try:
        response = requests.get(f'http://localhost:8000/api/images/{patient_id}/')
        response.raise_for_status()
        images = response.json() if response.text else []
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Erreur lors de la récupération des images : {e}")
        images = []

    # Appel API pour récupérer les rapports d'analyse
    try:
        response_reports = requests.get(f'http://localhost:8000/api/reports/{patient_id}/')
        response_reports.raise_for_status()
        reports = response_reports.json() if response_reports.text else []
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Erreur lors de la récupération des rapports : {e}")
        reports = []

    return render(request, 'patient_details.html', {
        'patient': patient,
        'images': images,
        'reports': reports
    })


def patient_list(request):
    """
    Vue pour afficher la liste des patients.
    """
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


def create_patient(request):
    """
    Vue pour créer un nouveau patient.
    """
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()  # Sauvegarder les données dans la base
            messages.success(request, "Le patient a été créé avec succès.")
            return redirect('patient_list')  # Rediriger vers la liste des patients
        else:
            messages.error(request, "Une erreur est survenue lors de la création du patient.")
    else:
        form = PatientForm()

    return render(request, 'create_patient.html', {'form': form})


@api_view(['POST'])
def create_patient_api(request):
    """
    API pour créer un nouveau patient (format JSON).
    """
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Enregistrer le patient
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


def patient_records(request):
    """
    Vue pour afficher les dossiers des patients.
    """
    return render(request, 'patient_records.html')



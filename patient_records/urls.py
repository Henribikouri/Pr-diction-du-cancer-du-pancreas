from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.create_patient, name='create_patient'),
    path('patients/api/create/', views.create_patient_api, name='create_patient_api'),  # API pour créer un patient
    path('patients/<int:patient_id>/', views.patient_details, name='patient_details'),
    path('patient_records/', views.patient_records, name='patient_records'),  # Nouvelle route
]

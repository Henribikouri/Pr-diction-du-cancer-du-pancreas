# data_analysis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/reports/<int:patient_id>/', views.get_reports_for_patient, name='get_reports_for_patient'),
    path('api/reports/generate/<int:patient_id>/', views.generate_report, name='generate_report'),
]

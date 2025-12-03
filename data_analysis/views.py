from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import AnalysisReport

@api_view(['GET'])
def get_reports_for_patient(request, patient_id):
    reports = AnalysisReport.objects.filter(patient_id=patient_id)
    data = [{'id': report.id, 'summary': report.summary, 'file_url': report.report_file.url} for report in reports]
    return JsonResponse(data, safe=False)

@api_view(['POST'])
def generate_report(request, patient_id):
    # Exemple de création de rapport
    result = request.data.get('result', 'Cancer du pancréas détecté')  # Résultat d'analyse d'image
    summary = f"Analyse du patient {patient_id}: {result}"
    report_file = request.FILES['report_file']

    # Créer le rapport
    analysis_report = AnalysisReport.objects.create(
        patient_id=patient_id,
        summary=summary,
        report_file=report_file
    )

    return JsonResponse({'status': 'success', 'summary': analysis_report.summary})

from django.urls import path
from . import views
from .views import predict_image

"""urlpatterns = [
    path('api/images/<int:patient_id>/', views.get_images_for_patient, name='get_images_for_patient'),
    path('api/process_image/<int:patient_id>/', views.process_image, name='process_image'),  # Cette ligne suffit
    path("predict/", predict_image, name="predict_image"),
    path('image_processing/', views.image_processing, name='image_processing'),
]"""



urlpatterns = [
    path('api/images/<int:patient_id>/', views.get_images_for_patient, name='get_images_for_patient'),
    path('api/process_image/<int:patient_id>/', views.process_image, name='process_image'),  # Cette ligne suffit
    path("predict/", views.predict_image, name="predict_image"),  # Correction ici
    path('image_processing/', views.image_processing, name='image_processing'),
]







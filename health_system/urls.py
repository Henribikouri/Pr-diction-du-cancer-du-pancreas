"""
URL configuration for health_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# health_system/urls.py
"""from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Route pour la page d'accueil du projet
    path('admin/', admin.site.urls),
    path('patient-records/', include('patient_records.urls')),
    path('image-processing/', include('image_processing.urls')),
    path('data-analysis/', include('data_analysis.urls')),
]"""

from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),  # Route pour la page d'accueil du projet
    path('admin/', admin.site.urls),
    path('', include('patient_records.urls')),
    path('image_processing/', include('image_processing.urls')),
    path('data_analysis/', include('data_analysis.urls')),
    #path('image_processing/', views.image_processing, name='image_processing'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


""""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs des différentes applications
    path('patients/', include('patient_records.urls')),  # Inclure les URLs de patient_records
    path('images/', include('image_processing.urls')),  # Inclure les URLs de image_processing
    path('analysis/', include('data_analysis.urls')),   # Inclure les URLs de data_analysis
]
"""

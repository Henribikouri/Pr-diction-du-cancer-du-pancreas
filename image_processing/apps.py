# image_processing/apps.py
from django.apps import AppConfig

class ImageProcessingConfig(AppConfig):
    name = 'image_processing'

    def ready(self):
        import image_processing.signals

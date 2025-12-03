from django.test import TestCase
from patient_records.models import Patient

# Create your tests here.

class PatientModelTest(TestCase):
    def test_create_patient(self):
        patient = Patient.objects.create(name="John Doe", age=30, gender="Male")
        self.assertEqual(str(patient), "John Doe")

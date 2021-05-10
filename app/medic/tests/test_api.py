from core import models
from core.tests.helpers import MEDIC_URL, SAMPLE_MEDIC_RESPONSE, SAMPLE_SPECIALTY_LIST, sample_user
from django.test import TestCase
from medic.serializers import MedicSerializer
from rest_framework import status
from rest_framework.test import APIClient


class PublicApiTests(TestCase):
    """Test unauthenticated medic API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(MEDIC_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
    """Test unauthenticated medic API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    @classmethod
    def setUpTestData(cls):
        """Sets up sample testing data using provided examples"""
        for s in SAMPLE_SPECIALTY_LIST:
            models.Specialty.objects.create(nome=s)
        sp = models.Specialty.objects.all()
        for m in SAMPLE_MEDIC_RESPONSE:
            models.Medic.objects.create(nome=m['nome'], crm=m['crm'],
                                        especialidade=sp.get(nome=m['especialidade']["nome"]))

    def test_search_medic(self):
        """Users should be able to search for medics by name"""
        sp = models.Specialty.objects.all()
        s1 = sp.get(nome='Pediatria')
        s2 = sp.get(nome='Cardiologia')
        models.Medic.objects.create(nome='Maria', crm=222222,
                                    especialidade=s1)  # 2
        res = self.client.get('/medicos/?search=maria')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
        self.assertContains(res, text='Maria')

        res = self.client.get(f'/medicos/?search=maria&especialidade={s1.id}'
                              f'&especialidade={s2.id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)
        queryset = MedicSerializer(models.Medic.objects.filter(especialidade__in=[s1.id, s2.id],
                                                               nome__icontains='maria'),
                                   many=True)
        self.assertQuerysetEqual(queryset.data, res.data)

    def test_filter_medic_by_specialty(self):
        """Users should be able to filter medics by specialties"""
        res = self.client.get('/medicos/?especialidade=3')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        queryset = MedicSerializer(models.Medic.objects.filter(especialidade=3), many=True)
        self.assertQuerysetEqual(queryset.data, res.data)

    def test_search_invalid_medic(self):
        """Invalid search should not return results"""
        print('/medicos/?search=gregory&especialidade=1&especialidade=2')
        res = self.client.get('/medicos/?search=gregory&especialidade=1&especialidade=2')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

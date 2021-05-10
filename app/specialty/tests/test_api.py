from core import models
from core.tests.helpers import SAMPLE_SPECIALTY_RESPONSE, SPECIALTY_URL
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from specialty.serializers import SpecialtySerializer


def sample_user(username='test', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


class PublicApiTests(TestCase):
    """Test unauthenticated specialty API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(SPECIALTY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
    """Test unauthenticated specialty API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    @classmethod
    def setUpTestData(cls):
        """Sets up sample testing data using provided examples"""
        for s in SAMPLE_SPECIALTY_RESPONSE:
            models.Specialty.objects.create(nome=s['nome'])

    def test_specialties_serializes_and_gets_successfully(self):
        """Users should be able to get specialties without errors"""
        res = self.client.get(SPECIALTY_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_specialties_match_sample_format(self):
        """Specialty data format should match the provided sample data"""
        res = self.client.get(SPECIALTY_URL)
        serializer = SpecialtySerializer(res.data, many=True)
        self.assertQuerysetEqual(serializer.data, [n['nome'] for n in SAMPLE_SPECIALTY_RESPONSE],
                                 transform=lambda x: x['nome'], ordered=False)

    def test_search_specialty(self):
        """Users should be able to search for specialties by name"""
        queryset = models.Specialty.objects.filter(nome__icontains='ginecologia')
        res = self.client.get(f'{SPECIALTY_URL}?search=ginecologi')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset.values()[0]['nome'], 'Ginecologia')

from core import models
from core.tests.helpers import SPECIALTY_URL, SAMPLE_SPECIALTY_LIST, SAMPLE_SPECIALTY_RESPONSE
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from specialty.serializers import SpecialtySerializer

def sample_user(username='test', password='testpass'):
	"""Create a sample user"""
	return get_user_model().objects.create_user(username, password)


class PublicApiTests(TestCase):
	"""Test unauthenticated recipe API access"""

	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test that authentication is required"""
		res = self.client.get(SPECIALTY_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
	"""Test unauthenticated recipe API access"""

	def setUp(self):
		self.client = APIClient()
		self.user = sample_user()
		self.client.force_authenticate(self.user)

	@classmethod
	def setUpTestData(cls):
		for s in SAMPLE_SPECIALTY_LIST:
			models.Specialty.objects.create(nome=s)

	def test_get_specialty_list(self):
		"""Test Requirement: Nome da especialidade (termo de pesquisa)"""
		res = self.client.get(SPECIALTY_URL)
		serializer = SpecialtySerializer(res.data, many=True)
		self.assertQuerysetEqual(serializer.data, SAMPLE_SPECIALTY_RESPONSE)

	def test_create_specialty(self):
		"""T"""
		# specialty = models.Specialty.objects.create(
		# 	name="Gine"
		#

		specialty_name = 'Gine'
		res = self.client.post(SPECIALTY_URL, {'nome': specialty_name})

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		specialty = models.Specialty.objects.get(id=res.data['id'])
		self.assertEqual(specialty.nome, specialty_name)

	def test_search_specialty(self):
		"""T"""
		# specialty = models.Specialty.objects.create(
		# 	name="Gine"
		#

		queryset = models.Specialty.objects.filter(nome__icontains='gine')
		self.assertQuerysetEqual(queryset, [SAMPLE_SPECIALTY_RESPONSE[1]['nome']],
		                         transform=lambda x: x.nome)
		self.assertEqual(queryset.count(), 1)

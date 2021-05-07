from core import models
from core.tests.helpers import MEDIC_URL, SAMPLE_SPECIALTY_LIST, SAMPLE_MEDIC_RESPONSE, sample_user
from django.test import TestCase
from medic.serializers import MedicSerializer
from rest_framework import status
from rest_framework.test import APIClient


class PublicApiTests(TestCase):
	"""Test unauthenticated recipe API access"""

	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test that authentication is required"""
		res = self.client.get(MEDIC_URL)

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
		sp = models.Specialty.objects.all()
		for m in SAMPLE_MEDIC_RESPONSE:
			models.Medic.objects.create(nome=m['nome'], crm=m['crm'],
			                            especialidade=sp.get(nome=m['especialidade']["nome"]))

	def test_get_medic_list(self):
		"""Test Requirement: Nome da especialidade (termo de pesquisa)"""
		res = self.client.get(MEDIC_URL)
		print(res.content)
		serializer = MedicSerializer(res.data, many=True)
		self.assertQuerysetEqual(serializer.data, SAMPLE_MEDIC_RESPONSE)

	def test_create_medic(self):
		"""T"""
		medic_name = 'Gine'
		res = self.client.post(MEDIC_URL, {'nome': medic_name, 'crm': 222222})

		self.assertEqual(res.status_code, status.HTTP_201_CREATED)
		medic = models.Medic.objects.get(id=res.data['id'])
		self.assertEqual(medic.nome, medic_name)

	# Identificador de uma ou mais especialidades
	# Nome do médico (termo de pesquisa)
	# GET /medicos/?search=maria&especialidade=1&especialidade=3
	def test_search_medic(self):
		"""T"""
		sp = models.Specialty.objects.all()
		medic = models.Medic.objects.create(nome='Maria', crm=222222,
		                                    especialidade=sp.get(nome='Pediatria'))  # 2
		res = self.client.get('/medicos/?search=maria')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)

		res = self.client.get('/medicos/?search=maria&especialidade=2&especialidade=3')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)
		queryset1 = MedicSerializer(res.data, many=True)
		queryset2 = MedicSerializer([medic], many=True)
		self.assertQuerysetEqual(queryset1.data, queryset2.data)

	def test_filter_medic_by_specialty(self):
		"""T"""
		res = self.client.get('/medicos/?especialidade=3')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)

	def test_search_invalid_medic(self):
		"""T"""
		print('/medicos/?search=gregory&especialidade=1&especialidade=2')
		res = self.client.get('/medicos/?search=gregory&especialidade=1&especialidade=2')
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 0)

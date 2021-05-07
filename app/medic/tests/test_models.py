from unittest.mock import patch
import unittest

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from django.urls import reverse
from rest_framework import status
from medic.serializers import MedicSerializer

MEDIC_URL = reverse('medic:medic-list')
SAMPLE_MEDIC_RESPONSE = [
	{
		"id": 1,
		"crm": 3711,
		"nome": "Drauzio Varella",
		"especialidade": {
			"id": 2,
			"nome": "Pediatria"
		}
	},
	{
		"id": 2,
		"crm": 2544,
		"nome": "Gregory House",
		"especialidade": {
			"id": 3,
			"nome": "Cardiologia"
		}
	},
	{
		"id": 3,
		"crm": 3087,
		"nome": "Tony Tony Chopper",
		"especialidade": {
			"id": 2,
			"nome": "Pediatria"
		}
	}
]
SAMPLE_SPECIALTY_LIST = [
	"Ginecologia",
	"Pediatria",
	"Cardiologia",
	"Clínico Geral",
]


def sample_user(username='test', password='testpass'):
	"""Create a sample user"""
	return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):
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

	@unittest.skip('just an test sample')
	def test_create_medic(self):
		"""T"""
		MEDIC_URL = reverse('medic-list')
		# medic = models.Medic.objects.create(
		# 	name="Gine"
		#

		medic_name = 'Gine'
		res = self.client.post(MEDIC_URL, {'nome': medic_name})

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
					                            especialidade=sp.get(nome='Pediatria')) # 2
		res = self.client.get('/medicos/?search=maria')
		self.assertEqual(len(res.data), 1)

		res = self.client.get('/medicos/?search=maria&especialidade=2&especialidade=3')
		self.assertEqual(len(res.data), 1)
		queryset1 = MedicSerializer(res.data, many=True)
		queryset2 = MedicSerializer([medic], many=True)
		self.assertQuerysetEqual(queryset1.data, queryset2.data)

	def test_filter_medic_by_specialty(self):
				"""T"""
				res = self.client.get('/medicos/?especialidade=3')
				self.assertEqual(len(res.data), 1)

	def test_search_invalid_medic(self):
			"""T"""
			print('/medicos/?search=gregory&especialidade=1&especialidade=2')
			res = self.client.get('/medicos/?search=gregory&especialidade=1&especialidade=2')
			self.assertEqual(len(res.data), 0)

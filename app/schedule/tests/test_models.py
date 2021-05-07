from core import models
from core.tests.helpers import sample_user, SAMPLE_SPECIALTY_LIST, SAMPLE_MEDIC_RESPONSE, \
	SCHEDULE_URL
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class PublicApiTests(TestCase):
	"""Test unauthenticated recipe API access"""

	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test that authentication is required"""
		res = self.client.get(SCHEDULE_URL)

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

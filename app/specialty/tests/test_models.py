from unittest.mock import patch
import unittest

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from django.urls import reverse
from rest_framework import status
from specialty.serializers import SpecialtySerializer

SPECIALTY_URL = reverse('specialty:specialty-list')
SAMPLE_SPECIALTY_LIST = [
	"Pediatria",
	"Ginecologia",
	"Cardiologia",
	"Clínico Geral",
]
SAMPLE_SPECIALTY_RESPONSE = [
	{
		"id": 1,
		"nome": "Pediatria"
	},
	{
		"id": 2,
		"nome": "Ginecologia"
	},
	{
		"id": 3,
		"nome": "Cardiologia"
	},
	{
		"id": 4,
		"nome": "Clínico Geral"
	}
]


def sample_user(username='test', password='testpass'):
	"""Create a sample user"""
	return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):
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

	@unittest.skip('just an test sample')
	def test_tag_str(self):
		"""Test the tag string representation"""
		tag = models.Tag.objects.create(
			user=sample_user(),
			name='Vegan'
		)

		self.assertEqual(str(tag), tag.name)

	@unittest.skip('just an test sample')
	def test_ingredient_str(self):
		"""Test the ingredient string respresentation"""
		ingredient = models.Ingredient.objects.create(
			user=sample_user(),
			name='Cucumber'
		)

		self.assertEqual(str(ingredient), ingredient.name)

	@unittest.skip('just an test sample')
	def test_recipe_str(self):
		"""Test the recipe string representation"""
		recipe = models.Recipe.objects.create(
			user=sample_user(),
			title='Steak and mushroom sauce',
			time_minutes=5,
			price=5.00
		)

		self.assertEqual(str(recipe), recipe.title)

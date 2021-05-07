from django.contrib.auth import get_user_model
from django.test import TestCase


def sample_user(username='test', password='testpass'):
	"""Create a sample user"""
	return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):
	pass

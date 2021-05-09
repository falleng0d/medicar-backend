from unittest.mock import patch
import unittest

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models
from django.urls import reverse
from rest_framework import status


def sample_user(username='test', password='testpass'):
	"""Create a sample user"""
	return get_user_model().objects.create_user(username, password)


class ModelTests(TestCase):

	def test_create_user_with_username_successful(self):
		"""Test creating a new user with an username is successful"""
		username = 'test'
		password = 'Testpass123'
		user = get_user_model().objects.create_user(
			username=username,
			password=password
		)

		self.assertEqual(user.username, username)
		self.assertTrue(user.check_password(password))

	def test_new_user_username_normalized(self):
		"""Test the username for a new user is normalized"""
		username = 'test'
		user = get_user_model().objects.create_user(username, 'test123')

		self.assertEqual(user.username, username.lower())

	def test_new_user_invalid_username(self):
		"""Test creating user with no username raises error"""
		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(None, 'test123')

	def test_create_new_superuser(self):
		"""Test creating a new superuser"""
		user = get_user_model().objects.create_superuser(
			'test',
			'test123'
		)

		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)

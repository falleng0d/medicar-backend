import json
from datetime import datetime, date

from core import models
from core.models import Appointment, Schedule
from core.tests.helpers import sample_user, SCHEDULE_URL, APPOINTMENT_URL
from django.core import management
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from schedule.serializers import ScheduleSerializer


class PublicApiTests(TestCase):
	"""Test unauthenticated appointment API access"""

	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test that authentication is required"""
		res = self.client.get(APPOINTMENT_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
	"""Test unauthenticated appointment API access"""

	def setUp(self):
		self.client = APIClient()
		self.user = sample_user()
		self.user2 = sample_user(username='user2')
		self.client.force_authenticate(self.user)

	@classmethod
	def setUpTestData(cls):
		management.call_command('setup_test_data')
		user = sample_user()
		user2 = sample_user(username='user2')

		# Get some future times
		schedule_dataset = Schedule.objects.order_by('-dia').filter(horarios__isnull=False)
		future_schedules = schedule_dataset.filter(dia__gte=datetime.now().date())

		# Schedule some future appointments
		Appointment(user=user, horario=future_schedules.first().horarios.first(),
		            data_agendamento=datetime.now()).save()
		Appointment(user=user2, horario=future_schedules.last().horarios.first(),
		            data_agendamento=datetime.now()).save()

		# Get some past times
		past_schedules = schedule_dataset.filter(dia__lt=datetime.now().date())

		# Schedule some past appointments
		Appointment(user=user, horario=past_schedules.first().horarios.first(),
		            data_agendamento=datetime.now()).save()
		Appointment(user=user2, horario=past_schedules.last().horarios.first(),
		            data_agendamento=datetime.now()).save()

	def test_only_one_appointment_allowed_per_schedule_time(self):
		appointment = Appointment.objects.last()
		time = appointment.horario

		self.client.post(APPOINTMENT_URL, {'agenda_id': time.agenda_id,
		                                   'horario': time.horario})
		self.client.force_authenticate(self.user2)
		res = self.client.post(APPOINTMENT_URL, {'agenda_id': time.agenda_id,
		                                         'horario': time.horario})
		print(res.status_code)
		self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_user_can_see_only_future_appointments(self):
		res = self.client.get(APPOINTMENT_URL)
		self.assertEqual(res.status_code, status.HTTP_200_OK)

		for d in res.data:
			self.assertTrue(d.get('dia') >= datetime.now().date())

	def test_user_cannot_see_others_appointments(self):
		res = self.client.get(APPOINTMENT_URL)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		self.assertEqual(len(res.data), 1)

	def test_user_can_delete_appointments(self):
		appointment = Appointment.objects.get(user=self.user,
		                              horario__agenda__dia__gte=datetime.now().date())
		res = self.client.delete(f'{APPOINTMENT_URL}{appointment.id}')
		self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

	def test_user_cannot_delete_past_appointments(self):
		appointment = Appointment.objects.get(user=self.user,
		                                      horario__agenda__dia__lt=datetime.now().date())
		res = self.client.delete(f'{APPOINTMENT_URL}{appointment.id}')
		self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


import json
from datetime import datetime, date

from core import models
from core.models import Appointment, Schedule
from core.tests.helpers import sample_user, SCHEDULE_URL
from django.core import management
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from schedule.serializers import ScheduleSerializer


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

		self.debug_data_dump()

	def debug_data_dump(self):
		res = self.client.get(SCHEDULE_URL)
		data = res.data
		with open("res.json", "w") as writer:
			dump = json.dumps(data)
			writer.write(dump)

	@classmethod
	def setUpTestData(cls):
		management.call_command('setup_test_data')

	def test_schedules_format(self):
		schedule = models.Schedule.objects.get(pk=1)

		dataset = ScheduleSerializer(schedule)

		res = self.client.get(SCHEDULE_URL)
		print(res.content)

	def test_no_empty_times(self):
		res = self.client.get(SCHEDULE_URL)
		for d in res.data:
			if d.get('horarios') is not None:
				self.assertTrue(len(d['horarios']) > 0)

	def test_after_times(self):
		res = self.client.get(SCHEDULE_URL)
		data = res.data
		for d in data:
			dia = date.fromisoformat(d['dia'])
			self.assertTrue(dia >= datetime.today().date())
			if dia == datetime.today().date():
				horarios = d['horarios']
				for h in horarios:
					horario = datetime.strptime(h, '%H:%M').time()
					self.assertTrue(datetime.now().time() <= horario)

	def test_hide_appointment(self):
		schedule = Schedule.objects.order_by('-dia').filter(horarios__isnull=False)
		time = schedule.first().horarios.first()

		Appointment(user=self.user, horario=time,
		            data_agendamento=datetime.now()).save()

		res = self.client.get(SCHEDULE_URL)
		data = res.data

		# objs = ScheduleTime.objects.filter(agendamento__isnull=False).all()

		for d in data:
			if d.get('dia') != time.agenda.dia.isoformat():
				continue
			if d.get('medico').get('id') != time.agenda.medico.id:
				continue
			for h in d.get('horarios'):
				horario = datetime.strptime(h, '%H:%M').time()
				self.assertTrue(time.horario != horario)

import json
from datetime import datetime, date, timedelta

from core import models
from core.models import Appointment, Schedule
from core.tests.helpers import sample_user, SCHEDULE_URL
from django.core import management
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from schedule.serializers import ScheduleSerializer


class PublicApiTests(TestCase):
	"""Test unauthenticated schedule API access"""

	def setUp(self):
		self.client = APIClient()

	def test_auth_required(self):
		"""Test that authentication is required"""
		res = self.client.get(SCHEDULE_URL)

		self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateApiTests(TestCase):
	"""Test unauthenticated schedule API access"""

	def setUp(self):
		self.client = APIClient()
		self.user = sample_user()
		self.client.force_authenticate(self.user)

		self.debug_data_dump()

	def debug_data_dump(self):
		res = self.client.get(SCHEDULE_URL)
		data = res.data
		with open("schedule_sample.json", "w") as writer:
			dump = json.dumps(data)
			writer.write(dump)

	@classmethod
	def setUpTestData(cls):
		management.call_command('setup_test_data')

	def test_schedules_serializes_and_gets_successfully(self):
		schedule = models.Schedule.objects.first()
		ScheduleSerializer(schedule)
		self.client.get(SCHEDULE_URL)

	def test_schedule_filters_successfuly(self):
		"""Users should be able to filter the schedule data"""
		today_str = datetime.now().date().isoformat()
		nextweek_str = (datetime.now() + timedelta(days=7)).date().isoformat()
		filtered_url = f'/agendas/?medico=4&especialidade=6&' \
		         f'data_inicio={today_str}&data_final={nextweek_str}'
		res=self.client.get(filtered_url)
		self.assertEqual(res.status_code, status.HTTP_200_OK)
		print(res.data)

	def test_user_can_see_free_schedules(self):
		"""Users should not be able to see schedule on dates/times that have already
		passed"""
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

	def test_user_can_see_free_schedule_times(self):
		"""Users should not be able to see schedule times that have appointments"""
		schedule = Schedule.objects.order_by('-dia').filter(horarios__isnull=False)
		time = schedule.first().horarios.first()

		Appointment(user=self.user, horario=time,
		            data_agendamento=datetime.now()).save()

		res = self.client.get(SCHEDULE_URL)

		for d in res.data:
			if d.get('dia') != time.agenda.dia.isoformat():
				continue
			if d.get('medico').get('id') != time.agenda.medico.id:
				continue
			for h in d.get('horarios'):
				horario = datetime.strptime(h, '%H:%M').time()
				self.assertTrue(time.horario != horario)

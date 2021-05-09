from core.models import Specialty, Medic, ScheduleTime, Schedule
from core.tests.factories import (
	ScheduleFactory,
	SpecialtyFactory,
	MedicFactory,
	ScheduleTimeFactory
)
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

faker = Faker(locale='pt_BR')

SCHEDULE_NUMBER = 30
SPECIALTY_NUMBER = 6
MEDIC_NUMBER = 20
SCHEDULE_TIME_NUMBER = 50

class Command(BaseCommand):
	help = "Generates test data"

	@transaction.atomic
	def handle(self, *args, **kwargs):
		self.stdout.write("Deleting old data...")
		models = [Specialty, Medic, Schedule, ScheduleTime]
		for m in models:
			m.objects.all().delete()

		self.stdout.write("Creating new data...")

		specialtys = []
		for _ in range(SPECIALTY_NUMBER):
			specialty = SpecialtyFactory()
			specialtys.append(specialty)

		# Create all the users
		medics = []
		for _ in range(MEDIC_NUMBER):
			medic = MedicFactory(especialidade=faker.random.choice(specialtys))
			medics.append(medic)

		schedules = []
		for _ in range(SCHEDULE_NUMBER):
			schedule = ScheduleFactory(medico=faker.random.choice(medics))
			schedules.append(schedule)

		print(len(schedules))

		for _ in range(SCHEDULE_TIME_NUMBER):
			schedule = faker.random.choice(schedules)
			ScheduleTimeFactory(agenda=schedule)

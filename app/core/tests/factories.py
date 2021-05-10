from datetime import date, timedelta

import factory.random
from core import models
from factory.django import DjangoModelFactory
from faker import Faker

factory.random.reseed_random('miglo')
faker = Faker(locale='pt_BR')


def ramdom_date(date_range: int):
    return date.today() + timedelta(days=faker.pyint(min_value=-date_range, max_value=date_range))


def random_time():
    return faker.time('%H') + ':' + ('%02d' % (faker.pyint(min_value=0, max_value=30, step=30)))


class SpecialtyFactory(DjangoModelFactory):
    class Meta:
        model = models.Specialty

    nome = factory.Faker("job")


class MedicFactory(DjangoModelFactory):
    class Meta:
        model = models.Medic
        django_get_or_create = ('especialidade',)

    nome = factory.Faker("first_name")
    crm = factory.Faker("ean", length=8)
    telefone = factory.Faker("phone_number", locale='pt_BR')
    email = factory.Faker("ascii_email")


class ScheduleFactory(DjangoModelFactory):
    class Meta:
        model = models.Schedule
        django_get_or_create = ('medico', 'dia')

    dia = factory.LazyFunction(lambda: ramdom_date(5))


class ScheduleTimeFactory(DjangoModelFactory):
    class Meta:
        model = models.ScheduleTime
        django_get_or_create = ('agenda', 'horario')

    horario = factory.LazyFunction(random_time)

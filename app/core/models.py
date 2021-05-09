from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q

# Create your models here.
from rest_framework.exceptions import ValidationError


class Specialty(models.Model):
	nome = models.CharField(max_length=60)


# Deve ser possível cadastrar os médicos que podem atender na clínica fornecendo as seguintes
# informações:
#
# Nome: Nome do médico (obrigatório)
# CRM: Número do médico no conselho regional de medicina (obrigatório)
# E-mail: Endereço de e-mail do médico
# Telefone: Telefone do médico
# Especialidade: Especialidade na qual o médico atende
class Medic(models.Model):
	nome = models.CharField(max_length=255)
	crm = models.IntegerField(unique=True)
	email = models.EmailField(blank=True)
	telefone = PhoneNumberField(region='BR', blank=True)
	especialidade = models.ForeignKey(Specialty,
	                                  on_delete=models.deletion.SET_NULL,
	                                  null=True)


def limit_pub_date_choices():
	return {'pub_date__lte': datetime.utcnow()}


def validate_gte_today(value: datetime.date):
	print(value)
	if value < datetime.today().date():
		raise ValidationError(
			detail=f'{value} is less than today',
			code='invalid'
		)


# Deve ser possível criar uma agenda para um médico em um dia específico
# fornecendo as seguintes informações:
#
# Médico: Médico que será alocado (obrigatório) Dia: Data de alocação do médico (obrigatório)
# Horários: Lista de horários na qual o médico deverá ser alocado para o dia especificado (
# obrigatório)
class Schedule(models.Model):
	dia = models.DateField(auto_created=True, validators=[validate_gte_today])
	medico = models.ForeignKey(Medic, on_delete=CASCADE, unique_for_date="dia")
	ordering = ['dia']


# TODO: Não deve ser possível criar uma agenda para um médico em um dia passado
class ScheduleTimeManager(models.Manager):
	def get_queryset(self):
		q = super().get_queryset().filter(Q(agenda__dia__exact=datetime.now().date()))
		print(q.query)
		return q
	# Q(creator=owner) | Q(moderated=False)
	# return super().get_queryset().filter(Q(agenda__dia__gt=datetime.now().date()) |
	#                                      Q(Q(agenda__dia__exact=datetime.now().date()) &
	#                                        Q(horario__gte=datetime.now().time())))


# Horários: Lista de horários na qual o médico deverá ser alocado para o
# dia especificado (obrigatório)
class ScheduleTime(models.Model):
	agenda = models.ForeignKey(Schedule, on_delete=CASCADE,
	                           related_name='horarios')
	horario = models.TimeField()

	class Meta:
		unique_together = (("agenda", "horario"),)

	objects = models.Manager()  # The default manager.
	after_today = ScheduleTimeManager()


class Appointment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	horario = models.OneToOneField(ScheduleTime, on_delete=models.CASCADE,
	                               null=True, related_name='agendamento')
	data_agendamento = models.DateTimeField()

# class Passenger(models.Model):
#     firstName = models.CharField(max_length=20)
#     lastName = models.CharField(max_length=20)
#     middleName = models.CharField(max_length=20)
#     email = models.CharField(max_length=20)
#     phone = models.CharField(max_length=10)
#
# class Reservation(models.Model):
#     flight = models.OneToOneField(Flight,on_delete=models.CASCADE)
#     passenger = models.OneToOneField(Passenger,on_delete=models.CASCADE)

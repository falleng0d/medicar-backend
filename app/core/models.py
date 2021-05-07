from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
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


# Deve ser possível criar uma agenda para um médico em um dia específico
# fornecendo as seguintes informações:
#
# Médico: Médico que será alocado (obrigatório) Dia: Data de alocação do médico (obrigatório)
# Horários: Lista de horários na qual o médico deverá ser alocado para o dia especificado (
# obrigatório)
class Schedule(models.Model):
    dia = models.DateField(auto_created=True)
    medico = models.ForeignKey(Medic, on_delete=CASCADE, unique_for_date=dia)


# TODO: Não deve ser possível criar uma agenda para um médico em um dia passado

# Horários: Lista de horários na qual o médico deverá ser alocado para o
# dia especificado (obrigatório)
class DayScheduleTime(models.Model):
    agenda = models.ForeignKey(Schedule, on_delete=CASCADE)
    horario = models.CharField(max_length=5)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    agendamento = models.ForeignKey(DayScheduleTime, on_delete=models.CASCADE)

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

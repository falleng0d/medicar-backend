from core.utilities import validate_gte_today
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, SET_NULL
from phonenumber_field.modelfields import PhoneNumberField


# Nota sobre a implementação:
# - Os modelos foram projetados para serem "limpos", quer dizer,
#   não possuem funções com Side Effects.
# - Isso delega essas atribuições para a View que fica totalmente responsável por controlar
#   como a informação é apresentada, em que ordem e de que maneira
# - Isso facilita a reutilização do código do modelo e dos serializadores e da funcionalidade
#   em outros projetos

class Specialty(models.Model):
    nome = models.ChaField(max_length=60)

    class Meta:
        verbose_name = 'Especialidade'


# Deve ser possível cadastrar os médicos que podem atender na clínica
class Medic(models.Model):
    nome = models.CharField(max_length=255)
    crm = models.IntegerField(unique=True)
    email = models.EmailField(blank=True)
    telefone = PhoneNumberField(region='BR', blank=True)
    especialidade = models.ForeignKey(Specialty,
                                      on_delete=SET_NULL,
                                      null=True)

    class Meta:
        verbose_name = 'Medico'


# Deve ser possível criar uma agenda para um médico em um dia específico
class Schedule(models.Model):
    dia = models.DateField(auto_created=True, validators=[validate_gte_today])
    medico = models.ForeignKey(Medic, on_delete=CASCADE, unique_for_date="dia")
    ordering = ['dia']

    class Meta:
        verbose_name = 'Agenda'


# Horários: Lista de horários na qual o médico deverá ser alocado para o
# dia especificado (obrigatório)
class ScheduleTime(models.Model):
    agenda = models.ForeignKey(Schedule, on_delete=CASCADE,
                               related_name='horarios')
    horario = models.TimeField()

    class Meta:
        unique_together = (("agenda", "horario"),)
        verbose_name = 'Horário'


# Consultas
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    horario = models.OneToOneField(ScheduleTime, on_delete=CASCADE,
                                   null=True, related_name='agendamento')
    data_agendamento = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Consulta'

from datetime import time

from core.models import Appointment, ScheduleTime
from medic.serializers import MedicSerializer
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField


class ScheduleTimeField(serializers.RelatedField):
	def to_internal_value(self, obj):
		return self.queryset.objects.get(agenda=self.parent.initial_data['agenda_id'],
		                                 horario=obj)

	def to_representation(self, obj):
		if type(obj) in [str, time]:
			return obj
		return obj.horario.strftime('%H:%M')

class AppointmentSerializer(serializers.ModelSerializer):
	medico = MedicSerializer(read_only=True, source='horario.agenda.medico')
	# horario = ScheduleTimeField(queryset=ScheduleTime)
	horario = ScheduleTimeField(queryset=ScheduleTime)
	dia = serializers.ReadOnlyField(source='horario.agenda.dia')

	class Meta:
		model = Appointment
		fields = ['id', 'dia', 'horario', 'data_agendamento', 'medico']

class AppointmentPOSTSerializer(serializers.ModelSerializer):
	horario = ScheduleTimeField(queryset=ScheduleTime)
	agenda_id = ReadOnlyField(source='horario.agenda.id')

	class Meta:
		model = Appointment
		fields = ['agenda_id', 'horario']

from datetime import time

from core.models import Schedule, ScheduleTime
from medic.serializers import MedicSerializer
from rest_framework import serializers


class ScheduleTimeField(serializers.RelatedField):
	def to_internal_value(self, obj):
		return self.queryset.objects.get(agenda=obj.agenda, horario=obj)

	def to_representation(self, obj):
		if type(obj) in [str, time]:
			return obj
		return obj.horario.strftime('%H:%M')


class ScheduleSerializer(serializers.ModelSerializer):
	medico = MedicSerializer(read_only=True)
	horarios = ScheduleTimeField(many=True, queryset=ScheduleTime)

	class Meta:
		model = Schedule
		fields = ['medico', 'dia', 'horarios']

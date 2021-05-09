from datetime import datetime, time

from core.models import Schedule, ScheduleTime
from django.db import models
from django.db.models.functions import Coalesce
from medic.serializers import MedicSerializer
from rest_framework import serializers
from django.db.models import Q


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


class ScheduleTimeField2(serializers.RelatedField):
	def to_internal_value(self, obj):
		return self.queryset.objects.get(agenda=obj.agenda, horario=obj)

	def to_representation(self, obj):
		if type(obj) in [str, time]:
			return obj
		return obj.horario.strftime('%H:%M')

	def get_queryset(self):
		return ScheduleTime.after_today.all()


class ScheduleTimeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScheduleTime
		fields = ['horario']

	def to_representation(self, obj):
		if type(obj) in [str, time]:
			return obj
		return obj.horario.strftime('%H:%M')


class ScheduleSerializer2(serializers.ModelSerializer):
	medico = MedicSerializer(read_only=True)
	horarios = ScheduleTimeField(many=True, queryset=ScheduleTime)

	class Meta:
		model = Schedule
		fields = ['medico', 'dia', 'horarios']

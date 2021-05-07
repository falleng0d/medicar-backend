from core.models import Medic
from rest_framework import serializers
from specialty.serializers import SpecialtySerializer


class MedicSerializer(serializers.ModelSerializer):
	especialidade = SpecialtySerializer(read_only=True)
	class Meta:
		model = Medic
		fields = ['id', 'nome', 'crm', 'especialidade']

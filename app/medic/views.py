from core.models import Medic
from medic.serializers import MedicSerializer
from rest_framework import filters, viewsets


# from django_filters import rest_framework as filters
class MedicViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = Medic.objects.all()
	serializer_class = MedicSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['nome']

	def get_queryset(self):
		queryset = super().get_queryset()
		params = self.request.query_params.getlist('especialidade', default=None)
		if params:
			queryset = queryset.filter(especialidade__in=params)
		return queryset

from core.models import Medic
from medic.serializers import MedicSerializer
from rest_framework import filters, viewsets

# from django_filters import rest_framework as django_filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class MedicViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = Medic.objects.all()

	serializer_class = MedicSerializer
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	filter_backends = [filters.SearchFilter]
	search_fields = ['nome']

	def get_queryset(self):
		queryset = super().get_queryset()
		params = self.request.query_params.getlist('especialidade', default=None)
		if params:
			queryset = queryset.filter(especialidade__in=params)
		return queryset

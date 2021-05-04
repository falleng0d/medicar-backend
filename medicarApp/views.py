# Create your views here.
from medicarApp.serializer import SpecialtySerializer
from rest_framework import generics, viewsets

from .models import Specialty


class SpecialtyListView(generics.ListCreateAPIView):
	queryset = Specialty.objects.all()
	serializer_class = SpecialtySerializer


class SpecialtyViewSet(viewsets.ModelViewSet):
	"""
		API endpoint that allows users to be viewed or edited.
		"""
	queryset = Specialty.objects.all()
	serializer_class = SpecialtySerializer



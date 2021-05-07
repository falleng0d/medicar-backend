# Create your views here.
from core.models import Specialty
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from specialty.serializers import SpecialtySerializer


class SpecialtyViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	queryset = Specialty.objects.all()
	serializer_class = SpecialtySerializer
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

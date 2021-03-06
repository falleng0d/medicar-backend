from core.models import Specialty
from rest_framework import filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from specialty.serializers import SpecialtySerializer


class SpecialtyViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    """
    API endpoint that allows specialtys to be viewed and searched by the API.
    """
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

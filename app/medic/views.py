from core.models import Medic
from medic.serializers import MedicSerializer
from rest_framework import filters, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


class MedicViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    API endpoint that allows medics to be viewed and searched by the API.
    """
    queryset = Medic.objects.all()

    serializer_class = MedicSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params.getlist('especialidade', default=None)
        if params:
            queryset = queryset.filter(especialidade__in=params)
        return queryset

from datetime import datetime

from core.models import Schedule, ScheduleTime
from django.db.models import Prefetch
from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from schedule.serializers import ScheduleSerializer


class ScheduleList(APIView):
    """
    API endpoint that allows the schedule(agenda) to be viewed by the API.
    As per required, users can only view delete and add to its owned data
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        schedule = self.queryset.order_by('dia')
        serializer = ScheduleSerializer(schedule, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @property
    def queryset(self):
        """Users should not be able to see schedule on dates that have already
        passed or that don't have any filter times"""
        base_queryset = Schedule.objects.filter(dia__gte=datetime.today().date())

        # Prefetch valid ScheduleTime objects
        queryset = base_queryset.prefetch_related(Prefetch(
            'horarios',
            ScheduleTime.objects.filter(Q(agendamento__isnull=True)
                                        & (Q(agenda__dia__gt=datetime.now().date())
                                           | Q(Q(agenda__dia__exact=datetime.now().date())
                                               & Q(horario__gte=datetime.now().time()))))
        ))

        specialty_ids = self.request.query_params.getlist('especialidade', default=None)
        if specialty_ids:
            queryset = queryset.filter(medico__especialidade__id__in=specialty_ids)

        medic_ids = self.request.query_params.getlist('medico', default=None)
        if medic_ids:
            queryset = queryset.filter(medico__id__in=medic_ids)

        initial_date = self.request.query_params.get('data_inicio', default=None)
        final_date = self.request.query_params.get('data_final', default=None)

        if initial_date:
            queryset = queryset.filter(dia__gte=initial_date)
        if final_date:
            queryset = queryset.filter(dia__lte=final_date)

        return queryset

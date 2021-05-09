from datetime import datetime

from core.models import Schedule, ScheduleTime

# Create your views here.
from django.db.models import Q
from django.db.models import Prefetch
from rest_framework import viewsets, filters, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from schedule.serializers import ScheduleSerializer, ScheduleSerializer2


# Create your views here.
class ScheduleList(APIView):
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		schedule = self.get_queryset.order_by('dia')
		serializer = ScheduleSerializer2(schedule, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = ScheduleSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	@property
	def get_queryset(self):
		base_queryset = Schedule.objects.filter(dia__gte=datetime.today().date())
		queryset = base_queryset.prefetch_related(Prefetch(
			'horarios',
			ScheduleTime.objects.filter(Q(agendamento__isnull=True) &
			                            (Q(agenda__dia__gt=datetime.now().date()) |
			       Q(Q(agenda__dia__exact=datetime.now().date()) &
			         Q(horario__gte=datetime.now().time()))))
		))

		# horario = datetime.now().time()
		# datetime.strptime('x', '%H:%M').time()

		specialty_ids = self.request.query_params.getlist('especialidade', default=None)
		if specialty_ids:
			queryset = queryset.filter(medico__especialidade__id__in=specialty_ids)
		medic_ids = self.request.query_params.getlist('medico', default=None)

		if medic_ids:
			queryset = queryset.filter(medico__id__in=medic_ids)

		initial_date = self.request.query_params.get('data_inicio', default=None)
		final_date = self.request.query_params.get('data_final', default=None)

		if initial_date:
			queryset = queryset.filter(agenda__dia__gte=initial_date)
		if final_date:
			queryset = queryset.filter(agenda__dia__lte=final_date)

		return queryset

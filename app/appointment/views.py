from datetime import datetime

from appointment.serializers import AppointmentSerializer, AppointmentPOSTSerializer
from core.models import Appointment
from django import db
from django.db import transaction
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AppointmentList(APIView):
	"""
	API endpoint that allows appointments to be viewed, added, and deleted by the API.
	As per required, users can only view delete and add to its owned data
	"""
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def get_object(self, pk):
		try:
			return self.queryset.get(pk=pk)
		except Appointment.DoesNotExist:
			raise status.HTTP_404_NOT_FOUND

	def get(self, request):
		data = self.queryset.order_by('data_agendamento')
		serializer = AppointmentSerializer(data, many=True)
		return Response(serializer.data)

	def post(self, request):
		serializer = AppointmentPOSTSerializer(data=request.data)
		if serializer.is_valid():
			try:
				with transaction.atomic():
					serializer.save(data_agendamento=datetime.now(), user=request.user)
			except db.utils.IntegrityError:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		try:
			appointment = self.queryset.get(pk=pk)
		except Appointment.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		appointment.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	@property
	def queryset(self):
		"""Retrieve the future appointments for the authenticated user"""
		queryset = Appointment.objects.filter(horario__agenda__dia__gte=datetime.today().date())
		return queryset.filter(user=self.request.user)

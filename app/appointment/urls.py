from django.conf.urls import url
from appointment import views

app_name = 'appointment'

urlpatterns = [
	url('consultas/$', views.AppointmentList.as_view()),
	url('consultas/(?P<pk>[0-9]+)$', views.AppointmentList.as_view()),
]

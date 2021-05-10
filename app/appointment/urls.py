from appointment import views
from django.conf.urls import url

app_name = 'appointment'

urlpatterns = [
    url('consultas/$', views.AppointmentList.as_view()),
    url('consultas/(?P<pk>[0-9]+)$', views.AppointmentList.as_view()),
]

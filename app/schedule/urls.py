from django.urls import path
from schedule import views

app_name = 'schedule'

urlpatterns = [
	path('agendas/', views.ScheduleList.as_view())
]

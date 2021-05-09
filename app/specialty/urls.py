from django.urls import path, include
from specialty import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('especialidades', views.SpecialtyViewSet)

app_name = 'specialty'

urlpatterns = [
	path('', include(router.urls))
]

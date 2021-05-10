from django.urls import include, path
from rest_framework import routers
from specialty import views

router = routers.DefaultRouter()
router.register('especialidades', views.SpecialtyViewSet)

app_name = 'specialty'

urlpatterns = [
    path('', include(router.urls))
]

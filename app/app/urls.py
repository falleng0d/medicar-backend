from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('', include('specialty.urls')),
    path('', include('medic.urls')),
    path('', include('schedule.urls')),
    path('', include('appointment.urls')),
    path('', include('user.urls')),
]

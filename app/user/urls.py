from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('user/', views.RetrieveUserView.as_view(), name='user')
]

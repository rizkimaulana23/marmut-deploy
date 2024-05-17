from django.urls import path
from .views import register, register_user, register_label

app_name = 'register'

urlpatterns = [
    path('', register, name='register'),
    path('user/', register_user, name='register_user'),
    path('label/', register_label, name='register_label'),
]
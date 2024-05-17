from django.urls import path
from login.views import *
from .views import login2, logout_view, register 

app_name = 'login'

urlpatterns = [
    path('', login2, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
]
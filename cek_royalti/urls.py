from django.urls import path
from .views import calculate_royalties

app_name = 'cek_royalti'

urlpatterns = [
    path('royalties/<uuid:user_id>/<str:user_type>/', calculate_royalties, name='calculate_royalties'),
]

from django.urls import path
from downloaded_song.views import *

app_name = 'main'

urlpatterns = [
    path('', show_downloaded_song, name='show_downloaded_song'),
]
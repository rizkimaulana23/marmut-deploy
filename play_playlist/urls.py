from django.urls import path
from play_playlist.views import *
from kelola_playlist.views import *

app_name = 'play_playlist'

urlpatterns = [
    path('<str:playlist_id>', play_playlist, name='play_playlist'),
]
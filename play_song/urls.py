from django.urls import path
from play_song.views import *

app_name = 'play_song'

urlpatterns = [
    path('<str:id_song>/', play_song, name='play_song'),
    path('ajax/download_song/', download_song, name='download_song_ajax'),
    path('func/add_to_playlist/', add_song_to_playlist, name='add_song_to_playlist'),
]
from django.urls import path
from kelola_playlist.views import *

app_name = 'kelola_playlist'

urlpatterns = [
    path('', kelola_playlist, name='kelola_playlist'),
    path('<str:playlist_id>', playlist_detail, name='playlist_detail'),
    path('ajax/play_song/', play_song, name='play_song_ajax'),
    path('delete_playlist/', delete_playlist, name='delete_playlist'),
    path('update_playlist/', update_playlist, name='update_playlist'),
    path('delete_song/', delete_song, name='delete_song'),
    path('ajax/shuffle_playlist/', shuffle_playlist, name='shuffle_playlist_ajax'),
    path('enter/add_song_to_playlist', add_song_to_playlist, name='add_song_to_playlist'),
]
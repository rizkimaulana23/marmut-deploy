from django.urls import path
from .views import (
    create_album_artist, detail_song, list_album_crud, add_song_to_album_artist,
    delete_album_artist, list_songs_in_album_crud, delete_song_from_album_artist,
    list_album_rd, list_songs_in_album_rd
)

app_name = 'kelola_album_song'

urlpatterns = [
    # CRUD KELOLA ALBUM & SONG untuk Artist/Songwriter
    path('artist/albums/', list_album_crud, name='list_album'),
    path('artist/albums/create/', create_album_artist, name='create_album_artist'),
    path('artist/albums/<uuid:album_id>/', list_songs_in_album_crud, name='list_songs_in_album'),
    path('artist/albums/<uuid:album_id>/add-song/', add_song_to_album_artist, name='add_song_to_album'),
    path('artist/albums/<uuid:album_id>/delete/', delete_album_artist, name='delete_album'),
    path('artist/albums/<uuid:album_id>/songs/<uuid:song_id>/delete/', delete_song_from_album_artist, name='delete_song_from_album'),
    path('albums/songs/<uuid:song_id>/detail/', detail_song, name='detail_song'),
    
    # RD KELOLA ALBUM & SONG untuk Label
    path('label/albums/', list_album_rd, name='list_album_rd'),
    path('label/albums/<uuid:album_id>/', list_songs_in_album_rd, name='list_songs_in_album_rd'),
]

from django.shortcuts import render
from django.shortcuts import redirect
from datetime import date
import uuid
import marmut_function.general as sql

# Create your views here.

def play_playlist(request, playlist_id):

    context = {
        'playlist':{
            'judul':'', 
            'jumlah_lagu':'', 
            'total_durasi':'', 
            'tanggal_dibuat':'', 
            'deskripsi':'', 
            'email_pembuat':'',
            'nama_pembuat':'',
            'playlist_id': playlist_id,
            },
        'songs':[],
        'all_songs':[],
    }
    # Mendapatkan semua lagu
    sql_all_songs = sql.query_result(
        f"""
        SELECT K.judul, AK.nama, K.id
        FROM SONG S
        JOIN KONTEN K ON K.id = S.id_konten
        JOIN ARTIST A ON A.id = S.id_artist
        JOIN AKUN AK ON AK.email = A.email_akun;
        """
    )

    for song in sql_all_songs:
        context['all_songs'].append({
            'judul': song[0],
            'nama_artist': song[1],
            'id_konten': song[2],
        })

    # Mendapatkan metadata playlist
    metadata_playlist = sql.query_result(
        f"""
        SELECT judul, jumlah_lagu, total_durasi, tanggal_dibuat, deskripsi, email_pembuat
        FROM USER_PLAYLIST
        WHERE id_playlist = '{playlist_id}';
        """
    )

    context['playlist']['judul'] = metadata_playlist[0][0]
    context['playlist']['jumlah_lagu'] = metadata_playlist[0][1]
    context['playlist']['total_durasi'] = metadata_playlist[0][2]
    context['playlist']['tanggal_dibuat'] = metadata_playlist[0][3]
    context['playlist']['deskripsi'] = metadata_playlist[0][4]
    context['playlist']['email_pembuat'] = metadata_playlist[0][5]
    
    email_pembuat = metadata_playlist[0][5]

    # Mendapatkan nama pembuat playlist
    nama_pembuat = sql.query_result(
        f"""
        SELECT nama
        FROM AKUN
        WHERE email = '{email_pembuat}';
        """
    )
    context['playlist']['nama_pembuat'] = nama_pembuat[0][0]

    # Mendapatkan lagu-lagu dalam playlist
    songs = sql.query_result(
        f"""
        SELECT K.judul, K.durasi, AK.nama, S.id_konten
        FROM PLAYLIST_SONG P
        JOIN SONG S ON S.id_konten = P.id_song
        JOIN KONTEN K ON S.id_konten = K.id
        JOIN ARTIST A ON A.id = S.id_artist
        JOIN AKUN AK ON AK.email = A.email_akun
        WHERE p.id_playlist = '{playlist_id}';
        """
    )

    for song in songs:
        context['songs'].append({
            'judul': song[0],
            'durasi': song[1],
            'nama_artist': song[2],
            'id_konten': song[3],
        })

    return render(request, 'play_playlist.html', context)

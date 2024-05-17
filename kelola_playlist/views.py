from django.shortcuts import render, redirect
from django.http import HttpResponse
from marmut_function.general import *
import marmut_function.general as sql
import json
import uuid
from datetime import date, datetime
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib import messages

# Create your views here.
def kelola_playlist(request):
    # test = {
    #     'email': data['email'],
    #     'premium_status': data['premium_status'],
    #     'role': data['role'],
    # }

    if request.method == 'POST':
        if request.POST['submit'] == 'create_new_playlist':
            new_playlist_uuid = uuid.uuid4()
            new_user_playlist_uuid = uuid.uuid4()
            today = date.today()
            formatted_date = today.strftime('%Y-%m-%d')

            sql.query_add(
                f"""
                INSERT INTO PLAYLIST(id) VALUES('{str(new_playlist_uuid)}');

                INSERT INTO USER_PLAYLIST(email_pembuat, id_user_playlist, judul, deskripsi, tanggal_dibuat, id_playlist, jumlah_lagu) VALUES
                ('{request.session.get('email')}', 
                '{str(new_user_playlist_uuid)}',
                '{request.POST['judul']}', 
                '{request.POST['deskripsi']}',
                '{formatted_date}',
                '{str(new_playlist_uuid)}',
                0
                );
                """
            )
            return redirect('kelola_playlist:kelola_playlist')

    html_data = {
        'playlist':[]
    }

    sql_data = sql.query_result(
        f"""
        SELECT id_playlist, id_user_playlist, judul, deskripsi, jumlah_lagu, total_durasi
        FROM USER_PLAYLIST
        WHERE email_pembuat = '{request.session.get('email')}'
        """
    )

    if len(sql_data) == 0:
        return render(request, 'user_playlist_kosong.html', html_data)
    else:
        for row in sql_data:
            html_data['playlist'].append({
                'id_playlist': row[0],
                'id_user_playlist': row[1],
                'judul': row[2],
                'deskripsi': row[3],
                'jumlah_lagu': row[4],
                'total_durasi': row[5],
            })

        return render(request, 'user_playlist_isi.html', html_data)

def playlist_detail(request, playlist_id):

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

    return render(request, 'user_playlist_detail.html', context)

def play_song(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "POST":
        song_id = request.POST.get('song_id')

        sql.query_add(
            f"""
            INSERT INTO AKUN_PLAY_SONG(email_pemain, id_song, waktu)
            VAlUES ('{request.session.get('email')}', '{song_id}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}');
            """
        )
        return JsonResponse({"success": True, "message": "Song played successfully!"})
    else:
        return JsonResponse({"success": False, "message": "Invalid request"}, status=400)

# def delete_playlist(request):
#     if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "POST":
#         playlist_id = request.POST.get('playlist_id')

#         # Perform your SQL operation here
#         try:
#             sql.query_add(
#                 f"""
#                 DELETE FROM AKUN_PLAY_USER_PLAYLIST
#                 WHERE id_user_playlist = 
#                 (
#                     SELECT id_user_playlist
#                     FROM USER_PLAYLIST
#                     WHERE id_playlist = '{playlist_id}'
#                 ) AND 
#                 email_pembuat = 
#                 (
#                     SELECT email_pembuat
#                     FROM USER_PLAYLIST
#                     WHERE id_playlist = '{playlist_id}'
#                 );

#                 DELETE FROM USER_PLAYLIST
#                 WHERE id_playlist = '{playlist_id}';

#                 DELETE FROM PLAYLIST
#                 WHERE id = '{playlist_id}';
#                 """
#             )
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})
        
#         return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
def delete_playlist(request):
    playlist_id = request.POST.get('playlist_id')
    sql.query_add(
        f"""
        DELETE FROM AKUN_PLAY_USER_PLAYLIST
        WHERE id_user_playlist = 
        (
            SELECT id_user_playlist
            FROM USER_PLAYLIST
            WHERE id_playlist = '{playlist_id}'
        ) AND 
        email_pembuat = 
        (
            SELECT email_pembuat
            FROM USER_PLAYLIST
            WHERE id_playlist = '{playlist_id}'
        );

        DELETE FROM USER_PLAYLIST
        WHERE id_playlist = '{playlist_id}';

        DELETE FROM PLAYLIST
        WHERE id = '{playlist_id}';
        """
    )   
    return redirect('kelola_playlist:kelola_playlist')

def update_playlist(request):
    playlist_id = request.POST.get('playlist_id')
    new_title = request.POST.get('title')
    new_description = request.POST.get('description')

    sql.query_add(
        f"""
        UPDATE USER_PLAYLIST
        SET judul = '{new_title}', deskripsi = '{new_description}'
        WHERE id_playlist = '{playlist_id}';
        """
    )

    return redirect('kelola_playlist:kelola_playlist')

def delete_song(request):
    song_id = request.POST.get('song_id')
    playlist_id = request.POST.get('playlist_id')

    sql.query_add(
        f"""
        DELETE FROM PLAYLIST_SONG
        WHERE id_playlist = '{playlist_id}' AND id_song = '{song_id}';
        """
    )

    return redirect('kelola_playlist:playlist_detail', playlist_id=playlist_id)

def shuffle_playlist(request):
    playlist_id = request.POST.get('playlist_id')
    email_pembuat = request.POST.get('email_pembuat')
    email_pemain = request.session.get('email')
    waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    songs = sql.query_add(
        f"""
        INSERT INTO AKUN_PLAY_USER_PLAYLIST(email_pemain, id_user_playlist, email_pembuat, waktu)
        VALUES ('{email_pemain}', 
        (
            SELECT id_user_playlist FROM USER_PLAYLIST
            WHERE id_playlist = '{playlist_id}'
        ),
        '{email_pembuat}', 
        '{waktu}');

        INSERT INTO akun_play_song(email_pemain, id_song, waktu)
        SELECT 
            '{email_pemain}',
            ps.id_song, 
            '{waktu}'
        FROM 
            playlist_song ps
        JOIN 
            user_playlist up ON ps.id_playlist = up.id_playlist
        WHERE 
            up.id_user_playlist = 
            (
                SELECT id_user_playlist FROM USER_PLAYLIST
                WHERE id_playlist = '{playlist_id}'
            );  
        """
    )

    return JsonResponse({"success": True, "message": "Playlist shuffle played successfully!"})

# def add_song_to_playlist(request):
#     if request.method == 'POST':
#         playlist_id = request.POST.get('playlist_id')
#         song_id = request.POST.get('song_id')

#         sql.query_add(
#             f"""
#             INSERT INTO PLAYLIST_SONG(id_playlist, id_song)
#             VALUES ('{playlist_id}', '{song_id}');
#             """
#         )

#         return redirect('kelola_playlist:playlist_detail', playlist_id=playlist_id)

#     return redirect('kelola_playlist:kelola_playlist')

def add_song_to_playlist(request):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')
        song_id = request.POST.get('song_id')

        try:
            sql.query_add(
                f"""
                INSERT INTO PLAYLIST_SONG(id_playlist, id_song)
                VALUES ('{playlist_id}', '{song_id}');
                """
            )
        except Exception as e:  # Catching database errors
            messages.error(request, f'Error adding song to playlist: {str(e)}')
            return redirect('kelola_playlist:playlist_detail', playlist_id=playlist_id)

        messages.success(request, 'Song added to playlist successfully!')
        return redirect('kelola_playlist:playlist_detail', playlist_id=playlist_id)

    return redirect('kelola_playlist:kelola_playlist')
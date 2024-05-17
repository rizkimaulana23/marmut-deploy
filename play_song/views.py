from django.shortcuts import render
from marmut_function.general import *
import marmut_function.general as sql
import json
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.
def play_song(request, id_song):

    data = {
        "judul" : "",
        "artist": "",
        "tanggal_rilis" : "",
        "tahun" : "",
        "durasi" : "",
        "total_play" : "",
        "total_download" : "",
        "album" : "",
        "genre" : "",
        "songwriter" : "",
        "id_song" : "",
        "playlists": [],
    }

    # Mendapatkan daftar playlist yang dimiliki oleh user
    sql_playlists = sql.query_result(
        f'''
        SELECT id_playlist, judul
        FROM USER_PLAYLIST
        WHERE email_pembuat = '{request.session.get('email')}';
        '''
    )
    print('KONTOLLL')
    print(sql_playlists)

    for playlist in sql_playlists:
        data['playlists'].append({
            "id_playlist": playlist[0],
            "judul_playlist": playlist[1]
        })

    # Mendapatkan data untuk lagu
    uuid_lagu_sementara = id_song

    lagu = query_result(
        f'''
        SELECT K.judul, K.tanggal_rilis, K.tahun, K.durasi, S.total_play, S.total_download, A.judul, AK.nama
        FROM KONTEN K
        JOIN SONG S on K.id  = S.id_konten
        JOIN ALBUM A on A.id = S.id_album
        JOIN ARTIST AR on AR.id = S.id_artist
        JOIN AKUN AK on AK.email = AR.email_akun
        WHERE K.id = '{uuid_lagu_sementara}'
        ''')
    
    data['judul'] = lagu[0][0]
    data['tanggal_rilis'] = lagu[0][1]
    data['tahun'] = lagu[0][2]
    data['durasi'] = lagu[0][3]
    data['total_play'] = lagu[0][4]
    data['total_download'] = lagu[0][5]
    data['album'] = lagu[0][6]
    data['artist'] = lagu[0][7]
    data['id_song'] = uuid_lagu_sementara

    # Mendapatkan data untuk genre
    genre = query_result(
        f'''
        SELECT G.genre
        FROM KONTEN K
        JOIN GENRE G on K.id = G.id_konten
        WHERE K.id = '{uuid_lagu_sementara}'
        ''')

    list_genre = []
    for row in genre:
        list_genre.append(row[0])

    string_genre = ""
    for j in range(len(list_genre)-1):
        string_genre += list_genre[j] + ", "

    
    string_genre += list_genre[-1]
    
    data['genre'] = string_genre

    # Mendapatkan data untuk songwriter
    songwriter = query_result(
        f'''
        SELECT A.nama 
        FROM SONG S
        JOIN SONGWRITER_WRITE_SONG SWS on S.id_konten = SWS.id_song
        JOIN SONGWRITER SW on SWS.id_songwriter = SW.id
        JOIN AKUN A on SW.email_akun = A.email
        WHERE S.id_konten = '{uuid_lagu_sementara}'
        '''
    )

    list_songwriter = []
    for row in songwriter:
        list_songwriter.append(row[0])

    string_songwriter = ""
    for j in range(len(list_songwriter)-1):
        string_songwriter += list_songwriter[j] + ", "

    string_songwriter += list_songwriter[-1]
    
    data['songwriter'] = string_songwriter
    
    return render(request, 'play_song.html', {'data':data, "navbar": get_navbar(request)})

def download_song(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "POST":
        try:
            song_id = request.POST.get('song_id')

            email = request.session.get('email')

            sql.query_add(
                f"""
                INSERT INTO DOWNLOADED_SONG(id_song, email_downloader)
                VALUES ('{song_id}', '{email}')
                """
            )

            # Return a response indicating success
            return JsonResponse({'status': 'success', 'message': 'Song successfully added to playlist.'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to add song to playlist: {str(e)}'}, status=400)
    
# def add_song_to_playlist(request):
#     if request.method == "POST":
#         song_id = request.POST.get('song_id')
#         playlist_id = request.POST.get('playlist_id')

#         sql.query_add(
#             f"""
#             INSERT INTO PLAYLIST__SONG(id_playlist, id_song)
#             VALUES ('{playlist_id}', '{song_id}')
#             """
#         )

#         return redirect('play_song:play_song', id_song=song_id)
    
def add_song_to_playlist(request):
    if request.method == "POST":
        song_id = request.POST.get('song_id')
        playlist_id = request.POST.get('playlist_id')

        try:
            # Assuming your SQL function handles exceptions and raises them on failure
            sql.query_add(
                f"INSERT INTO PLAYLIST_SONG(id_playlist, id_song) VALUES ('{playlist_id}', '{song_id}');"
            )
            return JsonResponse({'status': 'success', 'message': 'Song successfully added to playlist.'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Failed to add song to playlist: {str(e)}'}, status=400)
        
def get_navbar(request):
    data = {
        "email": request.session.get('email'),
        "role": request.session.get('role'),
        "premium_status": request.session.get('premium_status')
    }

    return data
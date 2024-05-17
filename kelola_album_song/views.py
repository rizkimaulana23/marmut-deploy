from django.shortcuts import render, redirect
from marmut_function.general import *
import marmut_function.general as sql
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

# CRUD KELOLA ALBUM & SONG untuk Artist/Songwriter
# View untuk menampilkan halaman pembuatan album untuk artist
def create_album_artist(request):
    if request.method == "GET":
        # Mendapatkan daftar label yang terdaftar pada Marmut
        labels = query_result("SELECT id, nama FROM LABEL")
        label_list = [{'id': label[0], 'nama': label[1]} for label in labels]

        # Mendapatkan daftar genre yang terdaftar pada Marmut
        genres = query_result("SELECT DISTINCT genre FROM GENRE")
        genre_list = [{'genre': genre[0]} for genre in genres]

        return render(request, 'create_album.html', {'labels': label_list, 'genres': genre_list})

    if request.method == "POST":
        judul_album = request.POST.get('judul_album')
        label_id = request.POST.get('label')
        judul_lagu = request.POST.get('judul_lagu')
        durasi = request.POST.get('durasi')
        genre_ids = request.POST.getlist('genre')
        songwriter_ids = request.POST.getlist('songwriter')

        # Asumsi user logged in sebagai artist atau songwriter
        user_email = request.session.get('email')
        user = query_result(f"SELECT id, role FROM AKUN WHERE email = '{user_email}'")[0]

        if user['role'] == 'artist':
            artist_id = user['id']
        else:
            artist_id = request.POST.get('artist')

        try:
            # Buat album
            album_id = query_add_returning(
                f"""
                INSERT INTO ALBUM (judul, id_label)
                VALUES ('{judul_album}', '{label_id}')
                RETURNING id
                """
            )[0][0]

            # Buat konten lagu
            song_id = query_add_returning(
                f"""
                INSERT INTO KONTEN (judul, tanggal_rilis, tahun, durasi)
                VALUES ('{judul_lagu}', CURRENT_DATE, EXTRACT(YEAR FROM CURRENT_DATE), '{durasi}')
                RETURNING id
                """
            )[0][0]

            # Tambahkan lagu ke album
            query_add(
                f"""
                INSERT INTO SONG (id_konten, id_album, id_artist)
                VALUES ('{song_id}', '{album_id}', '{artist_id}')
                """
            )

            # Tambahkan genre
            for genre_id in genre_ids:
                query_add(
                    f"""
                    INSERT INTO GENRE (id_konten, genre)
                    VALUES ('{song_id}', '{genre_id}')
                    """
                )

            # Tambahkan songwriter
            for songwriter_id in songwriter_ids:
                query_add(
                    f"""
                    INSERT INTO SONGWRITER_WRITE_SONG (id_song, id_songwriter)
                    VALUES ('{song_id}', '{songwriter_id}')
                    """
                )

            return redirect('kelola_album_song:list_album_crud')

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

def list_album_crud(request):
    user_email = request.session.get('email')
    user = query_result(f"SELECT id, role FROM AKUN WHERE email = '{user_email}'")[0]

    albums = query_result(
        f"""
        SELECT A.id, A.judul, COUNT(S.id_konten), SUM(K.durasi)
        FROM ALBUM A
        LEFT JOIN SONG S on A.id = S.id_album
        LEFT JOIN KONTEN K on S.id_konten = K.id
        WHERE A.artist_id = '{user['id']}'
        GROUP BY A.id, A.judul
        """
    )

    album_list = [{'id': album[0], 'judul': album[1], 'jumlah_lagu': album[2], 'total_durasi': album[3]} for album in albums]

    return render(request, 'list_album_crud.html', {'albums': album_list})

def list_songs_in_album_crud(request, album_id):
    songs = query_result(
        f"""
        SELECT K.judul, K.durasi, S.total_play, S.total_download
        FROM SONG S
        JOIN KONTEN K on S.id_konten = K.id
        WHERE S.id_album = '{album_id}'
        """
    )

    song_list = [{'judul': song[0], 'durasi': song[1], 'total_play': song[2], 'total_download': song[3]} for song in songs]

    return render(request, 'list_song_crud.html', {'songs': song_list, 'album_id': album_id})

def delete_album_artist(request, album_id):
    try:
        query_add(f"DELETE FROM ALBUM WHERE id = '{album_id}'")
        return redirect('kelola_album_song:list_album_crud')
    except Exception as e:
        return HttpResponseBadRequest(f"Error: {str(e)}")

def delete_song_from_album_artist(request, song_id):
    try:
        query_add(f"DELETE FROM SONG WHERE id_konten = '{song_id}'")
        query_add(f"DELETE FROM KONTEN WHERE id = '{song_id}'")
        return redirect('kelola_album_song:list_album_crud')
    except Exception as e:
        return HttpResponseBadRequest(f"Error: {str(e)}")

def add_song_to_album_artist(request, album_id):
    if request.method == "GET":
        # Mendapatkan data yang diperlukan
        artists = query_result("SELECT id, nama FROM ARTIST")
        genres = query_result("SELECT DISTINCT genre FROM GENRE")
        songwriters = query_result("SELECT id, nama FROM SONGWRITER")

        artist_list = [{'id': artist[0], 'nama': artist[1]} for artist in artists]
        genre_list = [{'genre': genre[0]} for genre in genres]
        songwriter_list = [{'id': songwriter[0], 'nama': songwriter[1]} for songwriter in songwriters]

        return render(request, 'add_song_to_album.html', {
            'artists': artist_list,
            'genres': genre_list,
            'songwriters': songwriter_list,
            'album_id': album_id
        })

    if request.method == "POST":
        judul_lagu = request.POST.get('judul_lagu')
        durasi = request.POST.get('durasi')
        genre_ids = request.POST.getlist('genre')
        songwriter_ids = request.POST.getlist('songwriter')

        user_email = request.session.get('email')
        user = query_result(f"SELECT id, role FROM AKUN WHERE email = '{user_email}'")[0]

        if user['role'] == 'artist':
            artist_id = user['id']
        else:
            artist_id = request.POST.get('artist')

        try:
            # Buat konten lagu
            song_id = query_add_returning(
                f"""
                INSERT INTO KONTEN (judul, tanggal_rilis, tahun, durasi)
                VALUES ('{judul_lagu}', CURRENT_DATE, EXTRACT(YEAR FROM CURRENT_DATE), '{durasi}')
                RETURNING id
                """
            )[0][0]

            # Tambahkan lagu ke album
            query_add(
                f"""
                INSERT INTO SONG (id_konten, id_album, id_artist)
                VALUES ('{song_id}', '{album_id}', '{artist_id}')
                """
            )

            # Tambahkan genre
            for genre_id in genre_ids:
                query_add(
                    f"""
                    INSERT INTO GENRE (id_konten, genre)
                    VALUES ('{song_id}', '{genre_id}')
                    """
                )

            # Tambahkan songwriter
            for songwriter_id in songwriter_ids:
                query_add(
                    f"""
                    INSERT INTO SONGWRITER_WRITE_SONG (id_song, id_songwriter)
                    VALUES ('{song_id}', '{songwriter_id}')
                    """
                )

            return redirect('kelola_album_song:list_album_crud')

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

# View untuk menampilkan detail lagu
def detail_song(request, song_id):
    song = query_result(f"""
        SELECT K.judul, K.durasi, S.total_play, S.total_download
        FROM SONG S
        JOIN KONTEN K on S.id_konten = K.id
        WHERE S.id_konten = '{song_id}'
    """)[0]

    song_details = {
        'judul': song[0],
        'durasi': song[1],
        'total_play': song[2],
        'total_download': song[3]
    }

    return render(request, 'detail_song.html', {'song': song_details})

# RD KELOLA ALBUM & SONG untuk Label
def list_album_rd(request):
    user_email = request.session.get('email')
    user = query_result(f"SELECT id, role FROM AKUN WHERE email = '{user_email}'")[0]

    albums = query_result(
        f"""
        SELECT A.id, A.judul, L.nama, COUNT(S.id_konten), SUM(K.durasi)
        FROM ALBUM A
        JOIN LABEL L on A.id_label = L.id
        LEFT JOIN SONG S on A.id = S.id_album
        LEFT JOIN KONTEN K on S.id_konten = K.id
        WHERE L.id = '{user['id']}'
        GROUP BY A.id, A.judul, L.nama
        """
    )

    album_list = [{'id': album[0], 'judul': album[1], 'label': album[2], 'jumlah_lagu': album[3], 'total_durasi': album[4]} for album in albums]

    return render(request, 'list_album_rd.html', {'albums': album_list})

def list_songs_in_album_rd(request, album_id):
    songs = query_result(
        f"""
        SELECT K.judul, K.durasi, S.total_play, S.total_download
        FROM SONG S
        JOIN KONTEN K on S.id_konten = K.id
        WHERE S.id_album = '{album_id}'
        """
    )

    song_list = [{'judul': song[0], 'durasi': song[1], 'total_play': song[2], 'total_download': song[3]} for song in songs]

    return render(request, 'list_song_rd.html', {'songs': song_list, 'album_id': album_id})

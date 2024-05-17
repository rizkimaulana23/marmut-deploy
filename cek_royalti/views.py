from django.shortcuts import render
from django.http import HttpResponse
from marmut_function.general import query_result

def calculate_royalties(request, user_id, user_type):
    # Tentukan tabel berdasarkan jenis pengguna
    if user_type == 'artist':
        user_table = 'artist'
        user_column = 'id_artist'
    elif user_type == 'songwriter':
        user_table = 'songwriter'
        user_column = 'id_songwriter'
    elif user_type == 'label':
        user_table = 'label'
        user_column = 'id_label'
    else:
        return HttpResponse('Invalid user type', status=400)

    # Ambil informasi pengguna
    user_info = query_result(f"SELECT * FROM {user_table} WHERE id = '{user_id}'")
    if not user_info:
        return HttpResponse('User not found', status=404)

    # Ambil data lagu dan hitung royalti
    songs = query_result(f"""
        SELECT 
            k.judul AS title,
            a.judul AS album_title,
            s.total_play AS plays,
            s.total_download AS downloads,
            phc.rate_royalti AS royalty_rate,
            (s.total_play * phc.rate_royalti) AS total_royalty
        FROM 
            SONG s
        JOIN 
            KONTEN k ON s.id_konten = k.id
        JOIN 
            ALBUM a ON s.id_album = a.id
        JOIN 
            ROYALTI r ON r.id_song = s.id_konten
        JOIN 
            PEMILIK_HAK_CIPTA phc ON r.id_pemilik_hak_cipta = phc.id
        WHERE 
            s.{user_column} = '{user_id}'
    """)

    total_royalty = sum(song[5] for song in songs)  # Menjumlahkan kolom total_royalty

    context = {
        'user': user_info[0],
        'songs': songs,
        'total_royalty': total_royalty
    }
    return render(request, 'cek_royalti/royalty.html', context)

import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from marmut_function.general import query_add, query_result
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        # Add other fields as needed

        try:
            sql.query_add(  # type: ignore
                f"""
                INSERT INTO AKUN (email, password, nama)
                VALUES ('{email}', '{password}', '{name}')
                """
            )
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login:login')
        except Exception as e:
            messages.error(request, f'Registration failed: {e}')

    return render(request, 'register.html')

def register_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        name = request.POST.get("nama")
        place_of_birth = request.POST.get("tempat_lahir")
        date_of_birth = request.POST.get("tanggal_lahir")
        hometown = request.POST.get("kota_asal")
        gender = request.POST.get("gender")
        role = request.POST.get("role")  # Role could be 'podcaster', 'artist', 'songwriter'
        is_verified = False  # Assuming default is_verified status

        # Mapping gender to integers
        gender_map = {'male': 1, 'female': 0}
        gender_value = gender_map.get(gender.lower(), 0)  # Default to 0 if undefined

        try:
            # Insert into AKUN table
            query_add(
                f"""
                INSERT INTO AKUN (email, password, nama, tempat_lahir, tanggal_lahir, kota_asal, gender, is_verified)
                VALUES ('{email}', '{password}', '{name}', '{place_of_birth}', '{date_of_birth}', '{hometown}', {gender_value}, {is_verified});
                """
            )

            if role == 'podcaster':
                # Insert into PODCASTER table
                query_add(
                    f"""
                    INSERT INTO PODCASTER (email)
                    VALUES ('{email}')
                    """
                )
            else:
                # Generate UUID for pemilik_hak_cipta
                pemilik_hak_cipta_id = str(uuid.uuid4())
                # Insert into PEMILIK_HAK_CIPTA table
                query_add(
                    f"""
                    INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti)
                    VALUES ('{pemilik_hak_cipta_id}', 0.1)
                    """
                )

                if role == 'artist':
                    # Generate UUID for artist
                    artist_id = str(uuid.uuid4())
                    # Insert into ARTIST table
                    query_add(
                        f"""
                        INSERT INTO ARTIST (id, email_akun, id_pemilik_hak_cipta)
                        VALUES ('{artist_id}', '{email}', '{pemilik_hak_cipta_id}')
                        """
                    )
                elif role == 'songwriter':
                    # Generate UUID for songwriter
                    songwriter_id = str(uuid.uuid4())
                    # Insert into SONGWRITER table
                    query_add(
                        f"""
                        INSERT INTO SONGWRITER (id, email_akun, id_pemilik_hak_cipta)
                        VALUES ('{songwriter_id}', '{email}', '{pemilik_hak_cipta_id}')
                        """
                    )

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login:login')
        except Exception as e:
            print(e)
            messages.error(request, f'Registration failed: {e}')
            return render(request, 'register_user.html', {'error': 'An error occurred during registration. Please check your input and try again.'})

    return render(request, 'register_user.html')

@csrf_exempt
def register_label(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        nama = request.POST['nama']
        kontak = request.POST['kontak']

        # Cek apakah email sudah digunakan untuk label lain
        existing_label = query_result(f"SELECT * FROM LABEL WHERE email = '{email}'")
        if existing_label:
            messages.error(request, 'Email sudah digunakan untuk label lain.')
            return render(request, 'register_label.html')

        try:
            # Generate UUID untuk id label dan id pemilik hak cipta
            label_id = str(uuid.uuid4())
            pemilik_hak_cipta_id = str(uuid.uuid4())

            # Buat entri baru di PEMILIK_HAK_CIPTA dengan rate royalti tetap, misalnya 0.1
            query_add(f"""
                INSERT INTO PEMILIK_HAK_CIPTA (id, rate_royalti)
                VALUES ('{pemilik_hak_cipta_id}', 0.1)
            """)

            # Tambahkan label baru ke database
            query_add(f"""
                INSERT INTO LABEL (id, nama, email, password, kontak, id_pemilik_hak_cipta)
                VALUES ('{label_id}', '{nama}', '{email}', '{password}', '{kontak}', '{pemilik_hak_cipta_id}')
            """)

            messages.success(request, 'Label berhasil didaftarkan.')
            return redirect('login:login')

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

    else:
        return render(request, 'register_label.html')

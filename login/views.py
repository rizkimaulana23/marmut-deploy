from django.shortcuts import redirect, render
import marmut_function.general as sql
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def login_or_register(request):
    return render(request, 'login_or_register.html')

def login2(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Validate email and password using SQL
        data = sql.query_result(
            f"""
            SELECT email, password, is_verified FROM AKUN
            WHERE email = '{email}'
            """
        )

        if len(data) == 0:
            messages.info(request, 'Email is not found. Please try again.')
        elif data[0][1] != password:
            messages.info(request, 'The password is incorrect. Please try again.')
        else:
            # Login the user
            user = authenticate(request, email=email, password=password)
            login(request, user)
            
            # Determining premium status
            is_premium = sql.query_result(
                f"""
                SELECT EXISTS(
                    SELECT * FROM PREMIUM
                    WHERE email = '{email}'
                )
                """
            )

            is_verified = data[0][2]

            if is_verified:
                # Determining the role
                is_artist = sql.query_result(
                    f"""
                    SELECT EXISTS(
                        SELECT * FROM ARTIST
                        WHERE email = '{email}'
                    )
                    """
                )
                if (is_artist[0][0] == "true"):
                    role = "artist"
                else:
                    is_label = sql.query_result(
                        f"""
                        SELECT EXISTS(
                            SELECT * FROM LABEL
                            WHERE email = '{email}'
                        )
                        """
                    )
                    if (is_label[0][0] == "true"):
                        role = "label"
                    else:
                        role = "songwriter"
            else: 
                role = "pengguna_biasa"
            
            response = HttpResponseRedirect(reverse("kelola_playlist:kelola_playlist"))

            # Set the session data
            print("LOGINNNN", is_premium[0][0])
            request.session['email'] = email
            request.session['premium_status'] = 'premium' if is_premium[0][0] == True else 'nonpremium'
            request.session['role'] = role
            return response
        
        return render(request, 'login.html')
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    logout(request)
    return HttpResponseRedirect(reverse("main:show_main"))

def register(request):
    if request.method == 'POST':
        # Handle registration form submission
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        # Add other fields as needed

        try:
            # Save the new user to the database
            sql.query_add(
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
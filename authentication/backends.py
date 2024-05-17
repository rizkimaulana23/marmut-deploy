# accounts/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db import connection
import marmut_function.general as sql

class CustomBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):

        user_password = sql.query_result(
            f"""
            SELECT password
            FROM AKUN
            WHERE email = '{email}'
            """
        )
        if len(user_password) == 0:
            return None
        elif user_password[0][0] == password:
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                # Optionally create a user in Django's system
                user = User(username=email)
                user.set_unusable_password()  # Important if you're not managing passwords through Django
                user.save()
            return user
        
        return None

    def get_user(self, user_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username FROM my_user_table WHERE id = %s", [user_id])
            result = cursor.fetchone()
            if result:
                user = User(username=result[1])
                user.pk = result[0]
                return user
        return None

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from users.models import CustomUser

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Busca al usuario por su email
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None

        # Verifica la contraseña y que el usuario esté activo
        if user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

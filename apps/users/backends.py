# users/backends.py
from django.contrib.auth.backends import ModelBackend
from users.models import User


class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        if username is None or password is None:
            return None

        try:
            # avval email orqali
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                # topilmasa phone orqali
                user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                return None

        if user and user.check_password(password):
            return user
        return None

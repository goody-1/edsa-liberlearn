from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        # Check if the input is an email address
        if "@" in username:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        else:
            # If not an email, try to find the user by username
            try:
                user = User.objects.get(Q(username=username) | Q(email=username))
            except User.DoesNotExist:
                return None

        # Check the user's password
        if user.check_password(password):
            return user

        return None

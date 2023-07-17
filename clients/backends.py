from django.core.exceptions import ObjectDoesNotExist

from .models import Client


class AuthBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return Client.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

    def authenticate(self, request, email, password):
        try:
            client = Client.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

        if client.check_password(password):
            return client
        else:
            return None

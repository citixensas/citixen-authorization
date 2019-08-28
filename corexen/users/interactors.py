import requests

from django.conf import settings
from corexen.users.models import AppUser

URL_SIGNUP = 'authentication/signup/'


class UserInteractor(object):

    @classmethod
    def create_user(cls, first_name, last_name, email, username, password, password_confirmation):
        created = False
        user = None
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': password,
            'password_confirmation': password_confirmation
        }
        r = requests.post(f'{settings.BASE_AUTHENTICATION_URL_API}{URL_SIGNUP}', data=data)
        if r.status_code == 201:
            response = r.json()
            uuid = response['uuid']
            user = AppUser.objects.create(uuid=uuid)
            created = True
        return created, user

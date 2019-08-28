import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from django.conf import settings

from corexen.users.models import AppUser


class UserInteractor(object):

    @classmethod
    def create_user(cls, first_name, last_name, email, username, password, password_confirmation):
        created = False
        user = None
        remote_response = None
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': password,
            'password_confirmation': password_confirmation
        }
        try:
            r = requests.post(f'{settings.BASE_AUTHENTICATION_URL_API}{settings.URL_SIGNUP}', data=data)
            if not r.status_code == 404:
                remote_response = r.json()
            if r.status_code == 201:
                uuid = remote_response['uuid']
                user = AppUser.objects.create(uuid=uuid)
                created = True
        except (ConnectionError, ConnectTimeout) as e:
            pass
        return created, user, remote_response

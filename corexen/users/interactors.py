from django.conf import settings

from corexen.users.models import AppUser
from corexen.utils.http import HTTPRequest


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
        status_code, response = HTTPRequest.post(url=f'{settings.BASE_AUTHENTICATION_URL_API}{settings.URL_SIGNUP}', data=data)
        if status_code == 201:
            uuid = response['uuid']
            user = AppUser.objects.create(uuid=uuid)
            created = True
        return created, user, response

    def retrive_user_info(self, user):
        pass

    def retrive_users_list(self, queryset, uuid_list):
        pass

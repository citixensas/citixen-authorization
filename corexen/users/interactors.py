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
        status_code, response = HTTPRequest.post(url=f'{settings.BASE_AUTHENTICATION_URL_API}{settings.URL_SIGNUP}',
                                                 data=data)
        if status_code == 201:
            uuid = response['uuid']
            user = AppUser.objects.create(uuid=uuid)
            created = True
        return created, user, response

    @classmethod
    def retrive_user_info(cls, user):
        uuid = str(user.uuid)
        found, response = HTTPRequest.get(url=f'{settings.BASE_AUTHENTICATION_URL_API}{settings.URL_USER_INFO}{uuid}')
        return found, response

    @classmethod
    def retrive_users_list(cls, queryset, uuid_list):
        pass

    @classmethod
    def convert_user_queryset_to_list_uuid(cls, queryset):
        #   list(queryset.annotate(str=Cast('uuid', output_field=CharField())).values_list('str', flat=True))
        list_uuid = list(queryset.values_list('uuid', flat=True))
        return [str(uuid) for uuid in list_uuid]

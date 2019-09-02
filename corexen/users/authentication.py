from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from corexen.users.models import User, AppUser


class CitixenAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            data = validated_token.payload
            user = User(
                first_name=data.get('first_name', ''), last_name=data.get('last_name', ''),
                email=data.get('email', ''), username=data.get('username', ''),
                uuid=data.get('uuid', None)
            )
            app_user, created = AppUser.objects.get_or_create(uuid=data['uuid'])
            user.app_user = app_user
            user.save()
            return user
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

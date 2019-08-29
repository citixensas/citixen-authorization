from corexen.users.models import User, AppUser
from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CitixenAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            data = validated_token.payload
            user = User(first_name=data['first_name'],  last_name=data['last_name'],
                        email=data['email'], username=data['username'], uuid=data['uuid'])
            app_user, created = AppUser.objects.get_or_create(uuid=data['uuid'])
            user.app_user = app_user
            return user
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

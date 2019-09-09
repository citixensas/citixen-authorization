from django.utils.translation import ugettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from corexen.users.models import User


class CitixenAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            data = validated_token.payload

            # Get or create user
            user, created = User.objects.get_or_create(uuid=data.get('uuid', None))
            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.email = data.get('email', user.email)
            user.username = data.get('username', user.username)
            user.is_superuser = data.get('is_superuser', user.is_superuser)
            user.save()

            return user
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

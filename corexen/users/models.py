import unicodedata
from uuid import uuid4

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.contrib.auth.models import UserManager, \
    _user_has_module_perms, _user_has_perm, _user_get_all_permissions, Permission, Group, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _

from corexen.companies.models import Headquarter
from corexen.utils.models import CitixenModel


class AbstractBaseUser(models.Model):
    password = models.CharField(_('password'), max_length=128)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    is_active = True

    REQUIRED_FIELDS = []

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return self.get_username(),

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """

        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])

        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username


class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class AppPermissionsMixin(PermissionsMixin):
    """
    Abstract permissions mixin class.
    Fix clashed related name with groups and permissions.
    """
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
        through='users.UserPermission',
    )

    class Meta(PermissionsMixin.Meta):
        abstract = True


class RemoteUserModelMixin(models.Model):
    """
    This mixin expose unique idenfier.
    """
    uuid = models.UUIDField(default=uuid4, unique=True)

    class Meta:
        abstract = True

    @property
    def get_app_user(self):
        """Extract user from this instance or return this current instance if is a AppUser."""
        if hasattr(self, 'app_user') and isinstance(self.app_user, AppUser):
            return self.app_user
        return self if isinstance(self, AppUser) else None


class _OldProfileSystemCapability:
    """This funcionality was deprecated."""

    _user_types = getattr(settings, 'APP_PROFILES', [])

    @property
    def profile(self):
        """Return user profile."""
        for user_type in self._user_types:
            user_profile = getattr(self, user_type, None)
            if user_profile is not None:
                return user_profile
        return None

    def has_headquarter(self):
        """Verify if user is associated to headquarter."""
        return hasattr(self.profile, 'headquarter')

    def has_company(self):
        """Verify if user is associated to company."""
        return hasattr(self.profile, 'company')


class AppUser(CitixenModel):
    pass


class User(AbstractUser,
           RemoteUserModelMixin,
           AppPermissionsMixin):
    """
    This model contains user data in auth app and each citixen project.
    """
    objects = UserManager()


class UserPermission(CitixenModel):
    """
    This model contains each permission for user in specific headquarter.
    """
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.DO_NOTHING)

    headquarter = models.ForeignKey(Headquarter, on_delete=models.DO_NOTHING)

    def __str__(self):
        """Return friendly description."""
        return f'{self.user.uuid} can {self.permission} in {self.headquarter}'

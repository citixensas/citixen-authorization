import unicodedata
from distutils.version import LooseVersion
from uuid import uuid4

from django.contrib import auth
from django.contrib.auth.models import (
    UserManager,
    _user_has_module_perms,
    _user_has_perm,
    Permission,
    Group,
    AbstractBaseUser
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import CICharField, CIEmailField
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone, version
from django.utils.translation import gettext_lazy as _

from corexen.companies.models import Headquarter
from corexen.utils.models import CitixenModel

version_Django = version.get_main_version()

if LooseVersion(version_Django) >= LooseVersion('3.0'):
    # noinspection PyUnresolvedReferences
    from django.contrib.auth.models import _user_get_permissions
else:
    from django.contrib.auth.models import _user_get_all_permissions


class AbstractUser(AbstractBaseUser):
    """
        An abstract base class implementing a fully featured User model with
        admin-compliant permissions.

        Username and password are required. Other fields are optional.
        """
    username_validator = UnicodeUsernameValidator()

    username = CICharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = CIEmailField(_('email address'), blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_banned = models.BooleanField(
        _('banned'),
        default=False,
        help_text=_(
            'Designate if this user should be treated as banned'
        ),
    )
    is_enabled = models.BooleanField(
        _('enabled'),
        default=True,
        help_text=_(
            'Designate if this user should be treated as enabled'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    @classmethod
    def normalize_username(cls, username):
        """Normalize email and lowercase during normalizing."""
        return super(AbstractUser, cls).normalize_username(username).lower()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


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
        if LooseVersion(version_Django) >= LooseVersion('3.0'):
            return _user_get_permissions(self, obj, 'all')
        else:
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
        if getattr(self, 'is_active', None) and self.is_superuser:
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
        if getattr(self, 'is_active', None) and self.is_superuser:
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
    uuid = models.UUIDField(default=uuid4, primary_key=True)

    class Meta:
        abstract = True


class User(AbstractUser,
           RemoteUserModelMixin,
           AppPermissionsMixin):
    """
    This model contains user data in auth app and each citixen project.
    """
    objects = UserManager()

    phone_number = models.CharField(
        _('phone number'),
        max_length=26,
        null=True,
        blank=True,
        help_text=_('Verified phone number. 26 digits or fewer.')
    )
    non_verified_phone_number = models.CharField(
        _('non verified phone number'),
        max_length=26,
        null=True,
        blank=True,
        help_text=_('Non verified phone number. 26 digits or fewer.')
    )
    phone_number_verified_at = models.DateTimeField(
        _('phone number verified at'),
        null=True,
        blank=True,
        help_text=_('Date time on which the phone number was verified.')
    )

    non_verified_email = models.EmailField(
        _('non email address'),
        null=True,
        blank=True,
        help_text=_('Verified email. This field is not used by all user profiles.')
    )
    email_verified_at = models.DateTimeField(
        _('email verified at'),
        null=True,
        blank=True,
        help_text=_('Date time on which the email was verified.')
    )

    class Meta:
        """Meta options."""
        ordering = ('first_name', 'last_name')


class UserPermission(CitixenModel):
    """
    This model contains each permission for user in specific headquarter.
    """
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.DO_NOTHING)

    headquarter = models.ForeignKey(Headquarter, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ('user', 'headquarter')

    def __str__(self):
        """Return friendly description."""
        return f'{self.user.uuid} can {self.permission} in {self.headquarter}'

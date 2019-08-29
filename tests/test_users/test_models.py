import uuid

from django.contrib.auth.models import Permission
from faker import Faker
from test_plus import TestCase

from corexen.users.models import UserPermission, AppUser
from tests.test_companies.factories import CompanyFactory, HeadquarterFactory

fake = Faker()


class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.appUser = AppUser.objects.create()
        self.company = CompanyFactory(created_by=self.appUser)
        self.headquarter = HeadquarterFactory(company=self.company, created_by=self.appUser)

    def _add_user_permissions(self, permissions):
        for perm in permissions:
            UserPermission.objects.create(user=self.user, permission=perm,
                                          headquarter=self.headquarter)

    def test_should_add_permissions_to_user(self):
        self.assertEquals(self.user.user_permissions.count(), 0)
        perms_amount = Permission.objects.count()
        self.assertTrue(perms_amount > 0)
        self._add_user_permissions(permissions=Permission.objects.all())
        self.assertEquals(perms_amount, self.user.user_permissions.count())

    def test_should_verify_if_user_has_a_given_permission(self):
        self.assertEquals(self.user.user_permissions.count(), 0)
        perm = Permission.objects.first()
        UserPermission.objects.create(user=self.user, permission=perm,
                                      headquarter=self.headquarter)
        self.assertEquals(self.user.user_permissions.count(), 1)
        perm_codename = '%s.%s.%s' % (perm.content_type.app_label, perm.codename,
                                      self.headquarter.pk)
        self.assertTrue(self.user.has_perm(perm_codename))

    def test_should_user_has_not_permission_in_another_headquarter_in_same_company(self):
        headquarter = HeadquarterFactory(company=self.company, created_by=self.appUser)
        self.assertEquals(self.user.user_permissions.count(), 0)
        self._add_user_permissions(permissions=Permission.objects.all())
        perm = Permission.objects.first()
        perm_codename = '%s.%s.%s' % (perm.content_type.app_label, perm.codename,
                                      headquarter.pk)
        self.assertFalse(self.user.has_perm(perm_codename))

    def test_should_user_has_not_permission_in_another_headquarter_in_other_company(self):
        company = CompanyFactory(created_by=self.appUser)
        headquarter = HeadquarterFactory(company=company, created_by=self.appUser)
        self.assertEquals(self.user.user_permissions.count(), 0)
        self._add_user_permissions(permissions=Permission.objects.all())
        perm = Permission.objects.first()
        perm_codename = '%s.%s.%s' % (perm.content_type.app_label, perm.codename,
                                      headquarter.pk)
        self.assertFalse(self.user.has_perm(perm_codename))


class AppUserModelTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.uuid = uuid.uuid1()
        self.appUser = AppUser.objects.create(uuid=self.uuid)

    def test_string_representation(self):
        self.assertEquals(str(self.appUser), 'Remote User: {}'.format(str(self.uuid)))

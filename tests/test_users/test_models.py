import uuid

from django.contrib.auth.models import Permission
from faker import Faker

from corexen.internationalization.models import Country, City, LanguageCode
from corexen.users.models import UserPermission
from corexen.utils.testing import CitixenTestCase
from tests.test_companies.factories import CompanyFactory, HeadquarterFactory

fake = Faker()


class UserModelTestCase(CitixenTestCase):

    def setUp(self):
        self.user = self.make_user()
        self.country = Country.objects.create(name='Colombia')
        self.city = City.objects.create(name='Colombia', country=self.country)
        self.language_code = LanguageCode.objects.create(name='Español', code='Es_co')
        self.company = CompanyFactory(country=self.country, created_by=self.user)
        self.headquarter = HeadquarterFactory(
            company=self.company,
            city=self.city,
            language_code=self.language_code,
            created_by=self.user,
        )

    def test_should_add_permissions_to_user(self):
        self.assertEquals(self.user.user_permissions.count(), 0)
        perms_amount = Permission.objects.count()
        self.assertTrue(perms_amount > 0)
        perm_pks = Permission.objects.all().values_list('codename', flat=True)
        self._add_user_permissions(perms=perm_pks, user=self.user,
                                   headquarter=self.headquarter)
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
        headquarter = HeadquarterFactory(
            name='headquarter1',
            company=self.company,
            city=self.city,
            language_code=self.language_code,
            created_by=self.user,
        )
        self.assertEquals(self.user.user_permissions.count(), 0)
        perm_pks = Permission.objects.all().values_list('codename', flat=True)
        self._add_user_permissions(perms=perm_pks, user=self.user,
                                   headquarter=self.headquarter)
        perm = Permission.objects.first()
        perm_codename = '%s.%s.%s' % (perm.content_type.app_label, perm.codename,
                                      headquarter.pk)
        self.assertFalse(self.user.has_perm(perm_codename))

    def test_should_user_has_not_permission_in_another_headquarter_in_other_company(self):
        headquarter = HeadquarterFactory(
            company=self.company,
            city=self.city,
            language_code=self.language_code,
            created_by=self.user,
        )
        self.assertEquals(self.user.user_permissions.count(), 0)
        perm_pks = Permission.objects.all().values_list('codename', flat=True)
        self._add_user_permissions(perms=perm_pks, user=self.user, headquarter=self.headquarter)
        perm = Permission.objects.first()
        perm_codename = '%s.%s.%s' % (perm.content_type.app_label, perm.codename, headquarter.pk)
        self.assertFalse(self.user.has_perm(perm_codename))

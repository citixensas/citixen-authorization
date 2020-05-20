import uuid

from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from faker import Faker

from corexen.internationalization.models import Country, City, LanguageCode
from corexen.users.models import UserPermission, User
from corexen.utils.testing import CitixenTestCase
from tests.test_companies.factories import CompanyFactory, HeadquarterFactory

fake = Faker()


class UserModelTestCase(CitixenTestCase):

    def setUp(self):
        self.user = self.make_user()
        self.country = Country.objects.create(name='Colombia')
        self.city = City.objects.create(
            name='Valledupar',
            country=self.country,
            code=5001,
            type=City.Types.locality
        )
        self.language_code = LanguageCode.objects.create(name='Español', code='Es_co')
        self.company = CompanyFactory(country=self.country, created_by=self.user)
        self.headquarter = HeadquarterFactory(
            company=self.company,
            city=self.city,
            created_by=self.user,
        )

    def test_should_add_permissions_to_user(self):
        self.assertEqual(self.user.user_permissions.count(), 0)
        perms_amount = Permission.objects.count()
        self.assertTrue(perms_amount > 0)
        perm_pks = Permission.objects.all().values_list('codename', flat=True)
        self._add_user_permissions(perms=perm_pks, user=self.user,
                                   headquarter=self.headquarter)
        self.assertEqual(perms_amount, self.user.user_permissions.count())

    def test_should_verify_if_user_has_a_given_permission(self):
        self.assertEqual(self.user.user_permissions.count(), 0)
        perm = Permission.objects.first()
        UserPermission.objects.create(user=self.user, permission=perm,
                                      headquarter=self.headquarter)
        self.assertEqual(self.user.user_permissions.count(), 1)
        perm_codename = '%s.%s.%s' % (perm.content_type.app_label, perm.codename,
                                      self.headquarter.pk)
        self.assertTrue(self.user.has_perm(perm_codename))

    def test_should_user_has_not_permission_in_another_headquarter_in_same_company(self):
        headquarter = HeadquarterFactory(
            name='headquarter1',
            company=self.company,
            city=self.city,
            created_by=self.user,
        )
        self.assertEqual(self.user.user_permissions.count(), 0)
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
            created_by=self.user,
        )
        self.assertEqual(self.user.user_permissions.count(), 0)
        perm_pks = Permission.objects.all().values_list('codename', flat=True)
        self._add_user_permissions(perms=perm_pks, user=self.user, headquarter=self.headquarter)
        perm = Permission.objects.first()
        perm_codename = '%s.%s.%s' % (perm.content_type.app_label, perm.codename, headquarter.pk)
        self.assertFalse(self.user.has_perm(perm_codename))


class UsernameValidationTestCase(CitixenTestCase):
    def setUp(self) -> None:
        self.username = 'abcEiou'
        self.password = fake.password()
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_should_authenticate_user_with_case_insensitive(self):
        credential_list = [
            {'username': 'abceiou', 'password': self.password},
            {'username': self.username, 'password': self.password},
            {'username': 'AbCeIOu', 'password': self.password},
        ]
        for credentials in credential_list:
            self.assertEqual(authenticate(**credentials), self.user)

    def test_should_not_authenticate_with_dots_or_with_(self):
        credential_list = [
            {'username': 'abce.iou', 'password': self.password},
            {'username': 'ábceíoú', 'password': self.password},
        ]
        for credentials in credential_list:
            self.assertIsNone(authenticate(**credentials), self.user)

    def test_should_save_messenger_username_in_lowercase_on_db(self):
        user = User.objects.create_user(username='MYUSERNAMEINUPPERCASE')
        user.refresh_from_db()
        self.assertEqual(user.username, 'myusernameinuppercase')


class VerificationEmailTestCase(CitixenTestCase):

    def test_no_verified_two_diffs_emails_and_verification_date(self):
        # Arrange
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'email': fake.email(),
            'non_verified_email': fake.email(),
            'email_verified_at': timezone.now(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_email

        # Assert
        self.assertFalse(is_verified)

    def test_same_emails_and_verification_date(self):
        # Arrange
        email = fake.email()
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'email': email,
            'non_verified_email': email,
            'email_verified_at': timezone.now(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_email

        # Assert
        self.assertTrue(is_verified)

    def test_email_without_verification_date(self):
        # Arrange
        email = fake.email()
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'email': email,
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_email

        # Assert
        self.assertTrue(is_verified)

    def test_non_verified_email_without_verification_date(self):
        # Arrange
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'non_verified_email': fake.email(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_email

        # Assert
        self.assertFalse(is_verified)

    def test_non_verified_email_with_verification_date(self):
        # Arrange
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'non_verified_email': fake.email(),
            'email_verified_at': timezone.now(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_email

        # Assert
        self.assertFalse(is_verified)

    def test_email_with_verification_date(self):
        # Arrange
        email = fake.email()
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'email': email,
            'email_verified_at': timezone.now(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_email

        # Assert
        self.assertTrue(is_verified)

    def test_two_diffs_emails_without_verification_date(self):
        # Arrange
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'email': fake.email(),
            'non_verified_email': fake.email(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_email

        # Assert
        self.assertFalse(is_verified)


class VerificationPhoneNumberTestCase(CitixenTestCase):

    def test_no_verified_two_diffs_phones_with_verification_date(self):
        # Arrange
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'phone_number': fake.numerify('+5731########'),
            'non_verified_phone_number': fake.numerify('+5731########'),
            'phone_number_verified_at': timezone.now(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_phone_number

        # Assert
        self.assertFalse(is_verified)

    def test_non_verified_phone_without_verification_date(self):
        # Arrange
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'non_verified_phone_number': fake.numerify('+5731########'),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_phone_number

        # Assert
        self.assertFalse(is_verified)

    def test_non_verified_phone_with_verification_date(self):
        # Arrange
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'non_verified_phone_number': fake.numerify('+5731########'),
            'email_verified_at': timezone.now(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_phone_number

        # Assert
        self.assertFalse(is_verified)

    def test_two_diffs_phones_without_verification_date(self):
        # Arrange
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'phone_number': fake.numerify('+5731########'),
            'non_verified_phone_number': fake.numerify('+5731########'),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_phone_number

        # Assert
        self.assertFalse(is_verified)

    def test_same_phones_with_verification_date(self):
        # Arrange
        phone_number = fake.numerify('+5731########')
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'phone_number': phone_number,
            'non_verified_phone_number': phone_number,
            'email_verified_at': timezone.now(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_phone_number

        # Assert
        self.assertTrue(is_verified)

    def test_phone_without_verification_date(self):
        # Arrange
        phone_number = fake.numerify('+5731########')
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'phone_number': phone_number,
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_phone_number

        # Assert
        self.assertTrue(is_verified)

    def test_phone_with_verification_date(self):
        # Arrange
        phone_number = fake.numerify('+5731########')
        user_data = {
            'username': fake.user_name(),
            'password': fake.password(),
            'phone_number': phone_number,
            'email_verified_at': timezone.now(),
        }
        user = User.objects.create(**user_data)

        # Act
        is_verified = user.is_verified_phone_number

        # Assert
        self.assertTrue(is_verified)



# Python
from uuid import uuid4

# Citixen
from django.contrib.auth.models import Permission
from faker import Factory
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from corexen.permissions.models import GroupTemplate
from corexen.permissions.serializers import GroupTemplateModelSerializer
from corexen.users.models import AppUser
from corexen.utils.testing import CitixenAPITestCase
# Companies
from tests.constants import EXAMPLE_TOKEN_VALID
from tests.test_companies.factories import CompanyFactory, HeadquarterFactory
from tests.test_permission.factories import GroupTemplateFactory

fake = Factory.create()


class GroupTemplateTestCase(CitixenAPITestCase):
    def setUp(self):
        self._credentials = {'username': fake.user_name(), 'password': fake.password()}
        self.user = self.make_superuser(**self._credentials)
        self.set_client_token(self.user)
        self.company = CompanyFactory(created_by=uuid4())
        self.headquarter = HeadquarterFactory(company=self.company, created_by=uuid4())
        self.client.credentials(HTTP_AUTHORIZATION='Bearer %s' % EXAMPLE_TOKEN_VALID)


class GetSingleGroupTemplateTestCase(GroupTemplateTestCase):

    def setUp(self):
        super().setUp()
        self.app_user = AppUser.objects.create(uuid=self.user.uuid)
        self._add_user_permissions(['view_grouptemplate'], user=self.app_user,
                                   headquarter=self.headquarter)
        self.groupTemplate = GroupTemplate.objects.create(
            name='TestGroupTemplate', headquarter=self.headquarter, parent=None)

    def test_should_should_get_valid_single_group_template(self):
        response = (self.get(reverse_lazy('permissions:grouptemplate-detail', kwargs={'pk': self.groupTemplate.pk})))
        group = GroupTemplate.objects.get(pk=self.groupTemplate.pk)
        serializer = GroupTemplateModelSerializer(group)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_should_should_get_invalid_single_group_template(self):
        response = (self.get(reverse_lazy('permissions:grouptemplate-detail', kwargs={'pk': 30})))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_should_get_valid_single_group_template_with_subgroup(self):
        self.subgroupTemplate = GroupTemplate.objects.create(
            name='TestSubGroupTemplate', headquarter=self.headquarter, parent=self.groupTemplate)
        response = (self.get(
            reverse_lazy('permissions:grouptemplate-detail', kwargs={'pk': self.groupTemplate.pk})))
        group = GroupTemplate.objects.get(pk=self.groupTemplate.pk)
        serializer = GroupTemplateModelSerializer(group)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllGroupTemplateTestCase(GroupTemplateTestCase):

    def setUp(self):
        super().setUp()
        self.app_user = AppUser.objects.create(uuid=self.user.uuid)
        self._add_user_permissions(['view_grouptemplate'], user=self.app_user,
                                   headquarter=self.headquarter)
        self.groupTemplate1 = GroupTemplate.objects.create(
            name='TestGroupTemplate1', headquarter=self.headquarter, parent=None)
        self.groupTemplate2 = GroupTemplate.objects.create(
            name='TestGroupTemplate2', headquarter=self.headquarter, parent=None)

    @staticmethod
    def _generate_groups(headquarter, parent, amount):
        return [
            GroupTemplateFactory(
                name=fake.name(),
                headquarter=headquarter,
                parent=parent
            )
            for _ in range(amount)
        ]

    def test_should_get_all_valid_group_template_not_parent(self):
        groups1 = self._generate_groups(self.headquarter, self.groupTemplate1, 5)
        groups2 = self._generate_groups(self.headquarter, self.groupTemplate2, 3)

        response = (self.get(reverse_lazy('permissions:grouptemplate-list')))
        # El Queryset debe estar basado en el que tenga la vista para la accion list
        groups = GroupTemplate.objects.filter(parent=None, headquarter=self.headquarter)
        serializer = GroupTemplateModelSerializer(groups, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(len(response.data['results']), 2)
        group_template_1 = [result for result in response.data['results'] if result['id'] == self.groupTemplate1.pk][0]
        group_template_2 = [result for result in response.data['results'] if result['id'] == self.groupTemplate2.pk][0]
        self.assertEqual(len(group_template_1['groups']), len(groups1))
        self.assertEqual(len(group_template_2['groups']), len(groups2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateGroupTemplateTestCase(GroupTemplateTestCase):

    def setUp(self):
        super().setUp()
        self.app_user = AppUser.objects.create(uuid=self.user.uuid)
        self._add_user_permissions(['add_grouptemplate'], user=self.app_user,
                                   headquarter=self.headquarter)

    def test_should_can_create_an_group_with_valid_payload_in_the_headquarter(self):
        valid_payload = {
            'name': 'clientes',
            'headquarter': self.headquarter.pk,
            'parent': '',
            'group_permissions': []
        }
        response = self.post(reverse_lazy('permissions:grouptemplate-list'), data=valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_can_not_create_an_group_with_invalid_payload__in_the_headquarter(self):
        invalid_payload = {
            'name': '',
            'headquarter': self.headquarter.pk,
            'parent': '',
            'group_permissions': []
        }
        response = self.post(reverse_lazy('permissions:grouptemplate-list'), data=invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_can_not_create_an_group_with_invalid_headquarter(self):
        payload = {
            'name': 'clientes',
            'headquarter': 20,
            'parent': '',
            'group_permissions': []
        }
        response = self.post(reverse_lazy('permissions:grouptemplate-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_can_not_create_an_group_with_invalid_parent(self):
        payload = {
            'name': 'clientes',
            'headquarter': self.headquarter.pk,
            'parent': 100,
            'group_permissions': []
        }
        response = self.post(reverse_lazy('permissions:grouptemplate-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_can_not_create_an_group_with_invalid_permission(self):
        payload = {
            'name': 'clientes',
            'headquarter': self.headquarter.pk,
            'parent': '',
            'group_permissions': [100]
        }
        response = self.post(reverse_lazy('permissions:grouptemplate-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_can_create_an_group_without_parent_without_group_permission_in_the_headquarter(self):
        payload = {
            'name': 'clientes',
            'headquarter': self.headquarter.pk,
            'parent': '',
            'group_permissions': []
        }
        response = self.post(reverse_lazy('permissions:grouptemplate-list'), data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_can_create_an_group_with_parent_without_group_permission_in_the_headquarter(self):
        group_parent = GroupTemplate.objects.create(name="terceros", headquarter=self.headquarter, parent=None)
        payload = {
            'name': 'clientes',
            'headquarter': self.headquarter.pk,
            'parent': group_parent.pk,
            'group_permissions': []
        }
        response = self.post(reverse_lazy('permissions:grouptemplate-list'), data=payload)
        self.assertEqual(response.data['parent'], group_parent.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_can_create_an_group_with_parent_with_group_permission_in_the_headquarter(self):
        group_parent = GroupTemplate.objects.create(name="terceros", headquarter=self.headquarter, parent=None)
        permissions = Permission.objects.first()
        payload = {
            'name': 'clientes',
            'headquarter': self.headquarter.pk,
            'parent': group_parent.pk,
            'group_permissions': [permissions.pk]
        }
        response = self.post(reverse_lazy('permissions:grouptemplate-list'), data=payload)
        self.assertEqual(response.data['parent'], group_parent.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

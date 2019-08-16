"""Company tests."""

from faker import Faker
from rest_framework.reverse import reverse_lazy, reverse

from ..factories import CompanyFactory, HeadquarterFactory
from companies.models import Company
#from citixen.users.tests.factories import ManagerFactory, AdminFactory

from utils.testing import CitixenAPITestCase

fake = Faker()


class CompanyViewTestCase(CitixenAPITestCase):
    def setUp(self):
        self._credentials = {'username': fake.user_name(), 'password': fake.password()}
        self.superuser = self.make_superuser(**self._credentials)

    def test_should_return_headquarters_list_if_user_is_superuser(self):
        self.set_client_token(self.superuser)
        response = self.client.get(reverse('companies:headquarter-list'))
        self.response_200(response)

    def test_should_return_company_headquarters_list_if_user_is_manager(self):
        company = CompanyFactory(created_by=self.superuser)
        #manager_user = ManagerFactory(company=company)
        #self.set_client_token(user=manager_user)
        response = self.client.get(reverse('companies:headquarter-list'))
        self.response_200(response)

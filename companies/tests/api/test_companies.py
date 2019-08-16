"""Company tests."""

from faker import Faker
from rest_framework.reverse import reverse

from companies.tests.factories import CompanyFactory
from citixen.users.tests.factories import ManagerFactory

from citixen.utils.testing import CitixenAPITestCase

fake = Faker()


class CompanyViewTestCase(CitixenAPITestCase):
    def setUp(self):
        self._credentials = {'username': fake.user_name(), 'password': fake.password()}
        self.superuser = self.make_superuser(**self._credentials)

    def test_should_not_return_list_companies_without_access(self):
        response = self.get(reverse('companies:company-list'))
        self.response_401(response)

    def test_should_return_list_companies_if_user_is_superuser(self):
        self.set_client_token(user=self.superuser)
        response = self.client.get(reverse('companies:company-list'))
        self.response_200(response)

    def test_should_not_return_list_companies_if_user_does_not_superuser(self):
        user = self.make_user({'username': fake.user_name(), 'password': fake.password()})
        self.set_client_token(user=user)
        response = self.client.get(reverse('companies:company-list'))
        self.response_403(response)

    def test_should_return_company_if_user_is_your_manager(self):
        company = CompanyFactory(created_by=self.superuser)
        manager = ManagerFactory(company=company)
        self.set_client_token(user=manager)
        response = self.client.get(reverse('companies:company-detail', kwargs={'pk': company.pk}))
        self.response_200(response)

    def test_should_not_return_company_if_user_is_not_your_manager(self):
        company = CompanyFactory(created_by=self.superuser)
        other_company = CompanyFactory(created_by=self.superuser)
        manager = ManagerFactory(company=company)
        self.set_client_token(user=manager)
        response = self.client.get(reverse('companies:company-detail', kwargs={'pk': other_company.pk}))
        self.response_403(response)

    def test_should_not_return_company_if_user_has_not_a_company(self):
        company = CompanyFactory(created_by=self.superuser)
        user = self.make_user({'username': fake.user_name(), 'password': fake.password()})
        self.set_client_token(user=user)
        response = self.client.get(reverse('companies:company-detail', kwargs={'pk': company.pk}))
        self.response_403(response)

    def test_should_return_list_of_company_headquarters_if_user_is_your_manager(self):
        company = CompanyFactory(created_by=self.superuser)
        manager = ManagerFactory(company=company)
        self.set_client_token(user=manager)
        response = self.client.get(reverse('companies:company-headquarters', kwargs={'pk': company.pk}))
        self.response_200(response)

from django.test import TestCase

from employer.models import employer
from accounts.models import User


class employerTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user('test@test.com', 'test_user', 'test_pass')
        employer.objects.create(user=test_user, company='test_company', industry='test_industry',
                                phone_number='+964780000000', )

    def test_employers_have_jobs(self):
        """Employer identified"""
        test_employer = employer.objects.get(company='test_company')
        self.assertEqual(str(test_employer), 'test_company')
        print('Employer Test Done.')

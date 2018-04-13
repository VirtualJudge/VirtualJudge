from django.test import TestCase

# Create your tests here.
from account.serializers import LoginSerializer


class TestSerializer(TestCase):
    def test_login(self):
        self.assertTrue(LoginSerializer.validate_password('password'))
        self.assertTrue(LoginSerializer.validate_username('username'))

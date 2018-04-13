from django.test import TestCase
import unittest
# Create your tests here.
from account.serializers import LoginSerializer


class SerializerTests(TestCase):
    def test_login(self):
        self.assertTrue(LoginSerializer.validate_password('password'))
        self.assertTrue(LoginSerializer.validate_username('username'))

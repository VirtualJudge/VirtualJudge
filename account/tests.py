from django.test import TestCase
import random
import string
# Create your tests here.
from account.serializers import LoginSerializer, RegisterSerializer

random_string = lambda length: ''.join(str(random.choice(string.ascii_lowercase)) for x in range(length))


class SerializerTests(TestCase):
    def test_login_1(self):
        request_data = {'username': 'username', 'password': 'password'}
        serializer = LoginSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_login_2(self):
        request_data = {'username': 'username', 'password-123': 'password'}
        serializer = LoginSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_login_3(self):
        request_data = {'username': 'err', 'password-123': 'password'}
        serializer = LoginSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_login_4(self):
        request_data = {'username': 'username', 'password': 'password', 'aaa': 'aaa'}
        serializer = LoginSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_register_1(self):
        request_data = {'username': 'username', 'password': 'password', 'email': 'email@email.com'}
        serializer = RegisterSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_register_2(self):
        request_data = {'username': 'username', 'password1': 'password', 'email': 'email@email.com'}
        serializer = RegisterSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_register_3(self):
        request_data = {'username': 'username', 'password': 'password', 'email': 'email-email.com'}
        serializer = RegisterSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_register_4(self):
        request_data = {'password': 'password', 'email': 'email-email.com'}
        serializer = RegisterSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_register_5(self):
        request_data = {'username': 'username', 'password': 'password', 'email': random_string(255) + 'email@email.com'}
        serializer = RegisterSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

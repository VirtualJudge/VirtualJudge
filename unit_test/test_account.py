import random
import string

from django.test import TestCase

# Create your tests here.
from account.serializers import LoginSerializer, RegisterSerializer, ChangePasswordSerializer
from account.models import UserProfile


def random_string(length):
    return ''.join(str(random.choice(string.ascii_lowercase)) for x in range(length))


class SerializerTests(TestCase):
    def setUp(self):
        UserProfile.objects.create_user('unit_test_user', 'email@unit_test.com', 'unit_test_password').save()

    def tearDown(self):
        UserProfile.objects.filter(username='unit_test_user').delete()

    def test_login_1(self):
        request_data = {'username': 'username', 'password': 'password'}
        serializer = LoginSerializer(data=request_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

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
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_register_1(self):
        request_data = {'username': 'username', 'password': 'password', 'email': 'email@email.com'}
        serializer = RegisterSerializer(data=request_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

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

    def test_change_password_1(self):
        request_data = {'old_password': 'unit_test_password',
                        'new_password': '111',
                        'username': 'unit_test_user'}

        serializer = ChangePasswordSerializer(data=request_data)
        self.assertFalse(serializer.is_valid())

    def test_change_password_2(self):
        request_data = {'old_password': 'unit_test_password',
                        'new_password': 'unit_test_password1',
                        'username': 'unit_test_user'}
        login_data_1 = {'username': 'unit_test_user', 'password': 'unit_test_password'}
        login_data_2 = {'username': 'unit_test_user', 'password': 'unit_test_password1'}
        serializer = ChangePasswordSerializer(data=request_data)
        login_serializer_1 = LoginSerializer(data=login_data_1)
        login_serializer_2 = LoginSerializer(data=login_data_2)
        self.assertTrue(login_serializer_1.is_valid(), login_serializer_1.errors)
        self.assertTrue(login_serializer_2.is_valid(), login_serializer_2.errors)

        self.assertIsNotNone(login_serializer_1.login(None))
        self.assertIsNone(login_serializer_2.login(None))

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertIsNotNone(serializer.save())

        self.assertIsNone(login_serializer_1.login(None))
        self.assertIsNotNone(login_serializer_2.login(None))

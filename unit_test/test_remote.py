from django.test import TestCase
from support.serializers import AccountSerializer
from support.models import Account


# Create your tests here.

class SerializerTest(TestCase):
    def setUp(self):
        Account.objects.filter(oj_username='unit_test', oj_name='wust').delete()
        account = Account(oj_username='unit_test', oj_password='password', oj_name='wust')
        account.save()

    def tearDown(self):
        Account.objects.filter(oj_username='unit_test', oj_name='wust').delete()

    def test_account_1(self):
        request_data = {'remote_oj': '', 'username': '', 'password': ''}
        serializer = AccountSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_account_2(self):
        request_data = {'remote_oj1': '', 'username2': '', 'password': ''}
        serializer = AccountSerializer(data=request_data)
        self.assertFalse(serializer.is_valid())

    def test_account_3(self):
        request_data = {'remote_oj': '', 'username': '', 'password3': ''}
        serializer = AccountSerializer(data=request_data)
        self.assertFalse(serializer.is_valid())

    def test_account_4(self):
        request_data = {'remote_oj': 'HDU', 'username': 'username', 'password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertTrue(serializer.is_valid())

    def test_account_5(self):
        request_data = {'remote_oj': 'HDU1', 'username': 'username', 'password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertFalse(serializer.is_valid())

    def test_account_6(self):
        request_data = {'remote_oj': 'hdu', 'username': 'username', 'password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertTrue(serializer.is_valid())

    def test_account_7(self):
        request_data = {'remote_oj': 'wust', 'username': 'unit_test', 'password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertTrue(serializer.save())

    def test_account_8(self):
        Account.objects.filter(oj_username='unit_test', oj_name='wust').delete()
        request_data = {'remote_oj': 'wust', 'username': 'unit_test', 'password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertTrue(serializer.save())

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
        request_data = {'oj_name': '', 'oj_username': '', 'oj_password': ''}
        serializer = AccountSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_account_2(self):
        request_data = {'oj_name1': '', 'oj_username1': '', 'oj_password': ''}
        serializer = AccountSerializer(data=request_data)
        self.assertFalse(serializer.is_valid())

    def test_account_3(self):
        request_data = {'oj_name': '', 'oj_username': '', 'oj_password1': ''}
        serializer = AccountSerializer(data=request_data)
        self.assertFalse(serializer.is_valid())

    def test_account_4(self):
        request_data = {'oj_name': 'HDU', 'oj_username': 'username', 'oj_password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertTrue(serializer.is_valid())

    def test_account_5(self):
        request_data = {'oj_name': 'HDU1', 'oj_username': 'username', 'oj_password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertTrue(serializer.is_valid())

    def test_account_6(self):
        request_data = {'oj_name': 'hdu', 'oj_username': 'username', 'oj_password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertTrue(serializer.is_valid())

    def test_account_7(self):
        request_data = {'oj_name': 'wust', 'oj_username': 'unit_test', 'oj_password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertFalse(serializer.is_valid(), serializer.errors)

    def test_account_8(self):
        Account.objects.filter(oj_username='unit_test', oj_name='wust').delete()
        request_data = {'oj_name': 'wust', 'oj_username': 'unit_test', 'oj_password': 'password'}
        serializer = AccountSerializer(data=request_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertTrue(serializer.save())

import unittest
from account.bodys import LoginBody
from json import JSONEncoder


class TestLogin(unittest.TestCase):
    def test_login_body(self):
        json_str = JSONEncoder().encode({
            'username': 'root',
            'password': '123s456'
        })
        body = LoginBody(bytes(json_str, encoding='utf-8'))
        self.assertTrue(body.is_valid(), msg=body.errors)

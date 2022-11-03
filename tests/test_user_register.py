from flask import url_for
from test_auth_base import TestAuthBase

class TestUserRegister(TestAuthBase):

    """ Test Case for User Register API """

    def test_expect_return_code_200(self):

        response = self.client.post(url_for("auth.register"))
        expected = 200
        self.assertEqual(response.status_code, expected)
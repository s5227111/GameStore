from flask import url_for
from test_auth_base import TestAuthBase

class TestUserRegister(TestAuthBase):

    """ Test Case for User Register API """

    def test_user_register(self):
        """ Test User Register """
        response = self.client.get(url_for("auth.register"))
        self.assertEqual(response.status_code, 200)

    def test_email_null(self):
        """ Test Email NULL """
        response = self.client.post(
            url_for("auth.validate_email"))
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_email(self):
        """ Test Invalid Email """

        invalid_email = ("email": "testmail.com")

        response = self.client.post(
            url_for("auth.validate_email"))
        self.assertEqual(response.status_code, 400)
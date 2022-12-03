from unittest import TestCase
from app import create_app
from auth.models import User, PersonalData, Contact, Address, PasswordReset

# pep8 - jeito correto de dar nome p uma classe
class TestCatalogBase(TestCase):
    def setUp(self) -> None:
        # docstring:
        """Execute before all tests"""

        self.app = create_app(test_mode=True)
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.db.create_all()

        self.usertest_dict = {
            "username": "test",
            "email": "test@mail.com",
            "password": "1234",
        }

    def tearDown(self) -> None:
        """
        Execute after test
        """

        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def register_user(self, user_dict: dict) -> None:
        """
        Register a user
        """

        self.client.post("/auth/register", json=user_dict)
        user = User(**user_dict)
        user.hash_password()
        user.personal_data = PersonalData()
        user.contact = Contact()
        user.address = Address()
        user.password_reset = PasswordReset()

        user.personal_data = user_personal_data
        user.contact = user_contact
        user.address = user_address
        user.password_reset = user_password_reset

        self.app.db.session.add(user)
        self.app.db.session.add(user.personal_data)
        self.app.db.session.add(user.contact)
        self.app.db.session.add(user.address)
        self.app.db.session.add(user.password_reset)

        self.app.db.session.commit()

        return user

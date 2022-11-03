from unittest import TestCase
from app import create_app

# pep8 - jeito correto de dar nome p uma classe
class TestAuthBase(TestCase):
    def setUp(self) -> None:
        # docstring:
        """Execute before all tests"""

        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
    
    def tearDown(self) -> None:
        pass
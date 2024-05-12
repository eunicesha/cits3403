import unittest
from app import create_app, db
from app.models import User
from config import TestConfig


class BasicTests(unittest.TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User.query.get("susan")
        u.set_password("cat")
        self.assertTrue(u.check_password("cat"))
        self.assertFalse(u.check_password("dog"))

    





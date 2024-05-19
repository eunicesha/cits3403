import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
from flask import url_for
from app import app, db
from flask_login import login_user, logout_user
from app.models import Game, User

class UserModelCase(unittest.TestCase):
    # Set up the application context and initialize the database
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Remove the session and drop all tables to clean up after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        # Test that password hashing and checking work correctly
        u = User(username='mia', email='mia@example.com')
        u.set_password('mia@2024')
        self.assertFalse(u.check_password('mia123'))
        self.assertTrue(u.check_password('mia@2024'))

    def test_avatar(self):
        # Test that the avatar URL is generated correctly
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))
    
    def test_user_creation(self):
        # Test creating a new user and retrieving it from the database
        u = User(username='tashi', email='tashi@example.com', about_me="I'm Tashi")
        db.session.add(u)
        db.session.commit()
        queried_user = User.query.filter_by(username='tashi').first()
        self.assertIsNotNone(queried_user)
        self.assertEqual(queried_user.email, 'tashi@example.com')
        self.assertEqual(queried_user.about_me, "I'm Tashi")

    def test_game_creation(self):
        # Test creating a new game and retrieving it from the database
        u1 = User(username='davin', email='davin@example.com')
        u2 = User(username='eunice', email='eunie@example.com')
        db.session.add_all([u1, u2])
        db.session.commit()
        
        game = Game(user_id=u1.id, opponent_id=u2.id, user_move='rock', opponent_move='scissors', result='win', status='finished')
        db.session.add(game)
        db.session.commit()
        
        queried_game = Game.query.filter_by(user_id=u1.id).first()
        self.assertIsNotNone(queried_game) # Ensure the game was added
        self.assertEqual(queried_game.opponent_id, u2.id)
        self.assertEqual(queried_game.user_move, 'rock')
        self.assertEqual(queried_game.opponent_move, 'scissors')
        self.assertEqual(queried_game.result, 'win')
        self.assertEqual(queried_game.status, 'finished') 

    def test_leaderboard(self):
        # Test the GET request to /leaderboard
        user1 = User(username='user1', email='user1@example.com', points=2)
        user2 = User(username='user2', email='user2@example.com', points=5)
        db.session.add_all([user1, user2])
        db.session.commit()

        with self.client:
            response = self.client.get('/leaderboard')
            self.assertEqual(response.status_code, 200)  # Ensure the request was successful
            self.assertIn(b'user2', response.data)  # Ensure the leaderboard contains user2
            self.assertIn(b'user1', response.data)  # Ensure the leaderboard contains user1
            self.assertLess(response.data.index(b'user2'), response.data.index(b'user1'))  # Ensure user2 appears before user1

if __name__ == '__main__':
    unittest.main(verbosity=2) # Run the tests with verbose output
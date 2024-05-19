import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

#game logic
def play_game(user_move, opponent_move):
    if user_move == opponent_move:
        return "Draw"
    elif (user_move == "rock" and opponent_move == "scissors") or \
         (user_move == "scissors" and opponent_move == "paper") or \
         (user_move == "paper" and opponent_move == "rock"):
        return "Lost"
    else:
        return "Won"

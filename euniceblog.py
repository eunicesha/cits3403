from flask import flash
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}


# game logic 
def play_game(user_id, user_move, opponent_id, opponent_move):
    
    user = User.query.get(user_id) #get users from database
    opponent = User.query.get(opponent_id)
    
    
    if user_move == opponent_move:
        result = "Draw"
    elif (user_move == "rock" and opponent_move == "scissors") or \
         (user_move == "scissors" and opponent_move == "paper") or \
         (user_move == "paper" and opponent_move == "rock"):
        result = "Lost"
        add_points(user_id, 1)  # user gets one point
        add_points(opponent_id, -1)  # opp loses one point 
    else:
        result = "Won"
        add_points(user_id, -1)  # user loses one point 
        add_points(opponent_id, 1)  # opp gains one point

    db.session.commit()
    return result

def add_points(user_id, points):
    user = User.query.get(user_id)
    try:
        if user:
            if user.points is None:
                user.points = 0 
            user.points += points
    except Exception as e:
        # handle exception if points dont work
        print(f"Error updating points for user {user_id}: {str(e)}")
        flash("Failed to update points. Please contact support.", "error")

    

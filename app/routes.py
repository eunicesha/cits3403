from euniceblog import play_game
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, MoveForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import Game, User
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app.forms import EditProfileForm

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('page'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        # validate the next URL to ensure redirects remain internal
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('page')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#first page(after log in) view function
@app.route('/page')
@login_required
def page():
    open_challenges = Game.query.filter_by(status="Open").options(joinedload(Game.player)).all()
    return render_template('index.html', open_challenges=open_challenges, title='Home Page')

#game view function
@app.route('/game')
@login_required
def game():
    # Fetch all open challenges from the database
    open_challenges = Game.query.filter_by(status="Open").options(joinedload(Game.player)).all()
    return render_template('index.html', open_challenges=open_challenges)

@app.route("/fetch_challenges")
def fetch_challenges():
    # Fetch challenges from the database
    challenges = Post.query.all()
    challenges_data = []
    for challenge in challenges:
        challenge_data = {
            "name": challenge.move
            #"stake": challenge.stake
        }
        challenges_data.append(challenge_data)
    return jsonify(challenges_data)

@app.route("/create_challenge", methods=['GET', 'POST'])
def create_challenge():
    form = MoveForm()
    if form.validate_on_submit():
        # Save the user's move as an open challenge in the database
        game = Game(user_id=current_user.id, user_move=form.move.data, status="Open")
        db.session.add(game)
        db.session.commit()
        flash('Challenge created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create_challenge.html', form=form)

@app.route("/accept_challenge/<int:challenge_id>", methods=['GET', 'POST'])
def accept_challenge(challenge_id):
    # Fetch the challenge from the database
    challenge = Game.query.get(challenge_id)
    if challenge:
        # Check if the challenge is not created by the current user
        if challenge.user_id == current_user.id:
            flash('You cannot accept your own challenge!', 'danger')
            return redirect(url_for('index'))
        
        form = MoveForm()
        if form.validate_on_submit():
            # Update the challenge with the opponent's move and change status to "Closed"
            challenge.opponent_move = form.move.data
            challenge.status = "Closed"
            # Determine the result of the game
            result = play_game(challenge.user_move, challenge.opponent_move)
            challenge.result = result
            db.session.commit()
            flash(f'Challenge accepted! You {result}!', 'success')
            return redirect(url_for('index'))
        return render_template('accept_challenge.html', form=form)
    else:
        flash('Challenge not found!', 'danger')
        return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@login_required
def index():
    # logic needed
    return render_template('index.html', title='Home Page')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = Game.query.filter_by(status="Open", user_id=user.id).all()
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

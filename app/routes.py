from flask import jsonify, render_template, flash, redirect, url_for, request
from app import app
from app.determine_outcome import game_logic
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import Challenge, GameResults, User
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app.forms import EditProfileForm



@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
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
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
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
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
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

@app.route('/play', methods=['GET', 'POST'])
@login_required
def play_game():
    if request.method == 'POST':
        user_id = current_user.id
        opp_id = request.form.get("opp_id")
        user_choice = request.form.get("user_choice")
        opp_choice = request.form.get("opp_choice")

        if not all([opp_id, user_choice, opp_choice]):
            return "Error: Missing data", 400

        result = game_logic(user_choice, opp_choice)
        final_result = f"{current_user.username} {'wins against' if result == 'win' else 'loses to' if result == 'lose' else 'ties with'} opponent {opp_id}"
        
        new_game_result = GameResults(user_id=user_id, user_id2=opp_id,
                                      user_choice=user_choice, user_choice2=opp_choice,
                                      result=final_result)
        db.session.add(new_game_result)
        db.session.commit()

        return render_template('play.html', result=final_result)
    return render_template('play.html')



@app.route('/api/accept_challenge/<int:challenge_id>', methods=['GET','POST'])
def accept_challenge(challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if challenge:
        challenge.status = 'Accepted'  
        db.session.commit() 
        return jsonify({'success': True, 'message': 'Challenge accepted'})
    else:
        return jsonify({'success': False, 'message': 'Challenge not found'}), 404
    

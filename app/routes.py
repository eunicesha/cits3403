from flask import jsonify, make_response, render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Post, Game
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
    
    return render_template('/templates/login.html', title='Sign In', form=form)

@app.route("/create_game", methods=["POST"])
@login_required
def create_game():
    if request.method == "POST":
        data = request.json
        if not data:
            return jsonify({"message": "Validation error, please make sure javascript is enabled for this site"}), 400
        try:
            stake = data["stake"]
            move = data["move"]
        except KeyError:
            return jsonify({"message": "Invalid request data"}), 400
        if not stake:
            return jsonify({"message": "Stake is required"}), 400

        game = Post(move=move, stake=stake, user_id=current_user.id)
        db.session.add(game)
        db.session.commit()
        return jsonify({"message": "Game successfully created"}), 201  # HTTP 201 Created
    else:
        return render_template("new-challenge.html", title="Create a new game")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@login_required
def index1():
    # logic needed
    return render_template('indexx.html', title='Home Page')

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
    return render_template('signup.html', title='Register', form=form)

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
    
# Route for initiating a game /templates/front_end/1v1 page/new-challenge
#@app.route("/create_game", methods = ["GET", "POST"])
#@login_required
#def create_game():
    #if(request.method == "GET"):
        #have to have a html page called startgame.html. Was thiknking of having davins pop-up functionality?
        #return(render_template("new-challenge.html",title = "Create a new game"))
    #if(request.get_json()):
        #data = request.get_json()
        #if(not data):
            #response_dict = {"message" : "Validation error, please make sure javascript is enabled for this site"}
            #resp = make_response(response_dict)
            #resp.headers["status"] = 400
            #return(resp)
        #try:
            # startgame.html's form will have to have this data. will add js functionality to check if user actually has sufficient points
            #stake = data["stake"]
            #move = data["move"]
        #except KeyError as e:
        #    return(jsonify({"url" : False}), 400)
        #if (not stake):
        #    return(jsonify({"url" : False}), 400)
        #if (not data):
        #    return(jsonify({"url" : False}), 400)
        # need to fix timestamp + author?
        #game = Post(move = move, stake = stake, user_id = current_user.id)
        #db.session.add(game)
        #db.session.commit()
    #return(jsonify('Game successfully created'))
# Route for initiating a game

# Route for responding to a game
#/templates/front_end/new challenge/
@app.route("/play_game", methods = ["GET", "POST"])
@login_required
def play_game():
    if(request.get_json()):
        data = request.get_json()
        if (not data):
            response_dict = {"message" : "Validation error, please make sure javascript is enabled for this site"}
            resp = make_response(response_dict)
            resp.headers["status"] = 400
            return(resp)
        try:
            #game has to store its id?
            game_id = data["game_id"]
            move = data["move"]
        except KeyError as e:
            return(jsonify({"url" : False}), 400)
        if (not move):
            return(jsonify({"url" : False}), 400)
        request = Post.query.filter_by(id=game_id).first()
        initiator = User.query.filter_by(id=request.user_id).first()
        responder = User.query.filter_by(id=current_user.id).first()
        winner = initiator.username
        if request.move == move:
            winner = 'Draw'
        elif request.move == 'rock':
            if move == 'paper':
                winner = responder.username
        elif request.move == 'paper':
            if move == 'scissors':
                winner = responder.username
        elif request.move == 'scissors':
            if move == 'rock':
                winner = responder.username
        game = Game(game_id = game_id, move = move, user_id = current_user.id, winner = winner)
        db.session.add(game)
        db.session.commit()
    return(jsonify('The winner is' + winner))

@app.route("/fetch_challenges")
def fetch_challenges():
    # Fetch challenges from the database
    challenges = Post.query.all()
    # Convert challenges to a list of dictionaries
    challenges_data = []
    for challenge in challenges:
        challenge_data = {
            "id": challenge.id,
            "name": challenge.move  # Assuming 'move' is the name of the challenge
            # You can add more fields here as needed
        }
        challenges_data.append(challenge_data)
    # Return challenges as JSON response
    return jsonify(challenges_data)
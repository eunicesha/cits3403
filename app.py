from flask import Flask, render_template, request, jsonify, url_for, redirect, g
import sqlite3

app = Flask(__name__)

# Connects to the database
def get_db_connection():
    return sqlite3.connect('data/users.db')

# On teardown, close the database
@app.teardown_appcontext
def close_connection(exception):
    # checks if db connection exists, and closes it if it does
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(debug=True)

# Defines forum webpage for successful signup/login redirection
@app.route("/forum")
def forum():
    return render_template('forum.html')

# Root URL - users reach the signup/login page when they enter the website
@app.route('/')
def index():
    return render_template('signup.html')

#Sign up form used
@app.route('/signup', methods=['POST'])
def signup():
    # Gets user input from sign up form
    username = request.form['Susername']
    email = request.form['Semail']
    password = request.form['Spassword']
    confirm_password = request.form['Sconfirm_password']

    # Input validation
    if not (username and email and password and confirm_password):
        # Make sure all input fields weren't empty
        return jsonify({'error': 'All fields are required'})
    elif password != confirm_password:
        # Checks that passwords match
        return jsonify({'error': 'Passwords do not match'})
    
    with get_db_connection() as dbconnection:
        cursor = dbconnection.cursor()
        # Preventing injections into SQL with this format
        cursor.execute('SELECT * FROM userdata WHERE username = ?', (username,))
        if cursor.fetchone() is not None:
            # SQL query returned a line - there's already a user w/ that username
            return jsonify({'error': 'Username already exists'})
        else:
            # Insert new user into the database
            cursor.execute('INSERT INTO userdata VALUES (?, ?, ?, ?)', (username, email, password, 0))
            # Commit the changes to the databse
            dbconnection.commit()
            # New account was successfully made, return success
            return jsonify({'success': 'Signup successful'})

#log in
@app.route('/login', methods=['POST'])
def login():
    # Get user input from the form
    username = request.form['Lusername']
    password = request.form['Lpassword']

    # Input validation
    if not (username and password):
        return jsonify({'error': 'All fields are required'})
    # Check that username and password are correct
    with get_db_connection() as dbconnection:
        cursor = dbconnection.cursor()
        cursor.execute('SELECT password FROM userdata WHERE username = ?', (username,))
        # Returns first data point from SQL query - username is primary key so there's only one
        result = cursor.fetchone()
        if result is None:
            # Returned no password for the inputted username
            return jsonify({'error': 'Invalid username'})
        elif result[0] != password:
            # Input password was wrong
            return jsonify({'error': 'Incorrect password'})
        else:
            # Log in details were correct, return success
            return jsonify({'success': 'Login successful'})

@app.route('/play', methods = ['POST'])
def play():
    # Get user choice
    choice = request.form.get('choice')
    player1 = 'scissors'
    #check if there was actually a choice
    if not (choice):
        return jsonify({'error': 'Choose.'})
    if choice == player1:
        return jsonify({'success': 'Draw!'})
    # see if you won
    with get_db_connection() as dbconnection:
        cursor = dbconnection.cursor()
        cursor.execute('SELECT beats FROM psr WHERE option = ?', (choice,))
        result = cursor.fetchone()
        if result[0] == player1:
            return jsonify({'success': 'You won!!'})
        else:
            return jsonify({'success': 'You lost :('})






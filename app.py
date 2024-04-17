from flask import Flask, render_template, request, jsonify, url_for
import sqlite3

app = Flask(__name__)

db_path = 'data/users.db'

def get_db_connection():
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    return db

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    db = get_db_connection()
    c = db.cursor()
    results = c.execute('SELECT * FROM userdata WHERE username = "'+username+'";')
    # Input validation
    if not (username and email and password and confirm_password):
        return jsonify({'error': 'All fields are required'})
    elif password != confirm_password:
        return jsonify({'error': 'Passwords do not match'})
    elif results.fetchone() is not None:
        return jsonify({'error': 'Username already exists'})
    else:
        # Create new user
        c.execute('INSERT INTO userdata VALUES ("'+username+'","'+email+'","'+password+'",0);')
        db.commit()
        db.close()
        return jsonify({'success': 'User created successfully'})


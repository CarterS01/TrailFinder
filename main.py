import sqlite3
from flask import Flask, render_template
from login import *
from find import *
import bcrypt

con = sqlite3.connect("data.db")    #Create a connection to the database
app = Flask(__name__)               #Create a Flask object
app.config['SECRET_KEY'] = 'placeholder'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/find_a_trail', methods=["GET", "POST"])
def find_a_trail():
    form = findForm()
    if form.validate_on_submit():
        location = form.location.data
        terrain = form.terrain.data
        type = form.type.data
        jumps = form.jumps.data
        berms = form.berms.data
        drops = form.drops.data
        rolls = form.rolls.data
        skinnies = form.skinnies.data
        # Print statement for testing purposes
        print(f'Location: {location}\nTerrain: {terrain}\nType: {type}\nJumps: {jumps}\nBerms: {berms}\nDrops: {drops}\nRolls: {rolls}\nSkinnies: {skinnies}')
        return render_template('placeholder.html')
    return render_template('find.html', form=form)

@app.route('/recommend_a_trail')
def recommend_a_trail():
    return render_template('rec.html')

@app.route('/saved_trails')
def saved_trails():
    return render_template('saved.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form = loginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        with sqlite3.connect("data.db") as con:
            cur = con.cursor()

        cur.execute(''' SELECT username
                        FROM users
                        WHERE username=?''',
                        (username,))
            
        if cur.fetchone():     # Skips to else if no user matches, as cur.fethone() will return None

            newPass = password.encode('utf-8')                  # Convert password into format accepted by bcrypt (b'password')
            hashed = bcrypt.hashpw(newPass, bcrypt.gensalt())   # Hash the password using a generated salt

            # Open another cursor to fetch stored password hash
            with sqlite3.connect("data.db") as con:
                cur2 = con.cursor()

            # Search users table in database to retrieve hashed password corresponding with username
            cur2.execute('''SELECT pw_hash
                            FROM users
                            WHERE username=?''',
                            (username,))

            hashed = cur2.fetchall()               # Store the hashed password
            cur2.close()
            res = str(hashed).strip('[](),\'')     # Strip unnecessary characters off of password, otherwise it will not match in checkpw

            # If entered password is successfully matched to hash
            # Args need to be encoded for bcrypt format
            if bcrypt.checkpw(password.encode('utf-8'), res.encode('utf-8')):
                cur.close()
                return render_template('home.html')
            # If entered password does not match hash
            else:
                cur.close()
                form.username.data = ''
                form.password.data = ''
                return render_template('login.html', error="Incorrect password!", form=form)

        # If no record matching user is found  
        else:
            cur.close()
            form.username.data = ''
            form.password.data = ''
            return render_template('login.html', error="User not found!", form=form)
        
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
    # Uncomment line below to open up for outside connection for testing on other devices
    #app.run(host='0.0.0.0', port=5000)
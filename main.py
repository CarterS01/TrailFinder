#--- PYTHON MODULES ---
import sqlite3
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
#--- .py FILES ---
from login import *
from register import *
from find import *
from user import *

con = sqlite3.connect("data.db")    #Create a connection to the database
app = Flask(__name__)               #Create a Flask object
app.config['SECRET_KEY'] = 'placeholder'
login_manager = LoginManager()
login_manager.login_view = 'app.login'

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
        difficulty = form.difficulty.data
        jumps = form.jumps.data
        drops = form.drops.data
        berms = form.berms.data
        rolls = form.rolls.data
        skinnies = form.skinnies.data
        # Print statement for testing purposes
        #print(f'Location: {location}\nTerrain: {terrain}\nType: {type}\nJumps: {jumps}\nBerms: {berms}\nDrops: {drops}\nRolls: {rolls}\nSkinnies: {skinnies}')
        passedTrails = []    # List that will later store which trails passed the trailscore test

        with sqlite3.connect("data.db") as con:
            cur = con.cursor()

        cur.execute(''' SELECT *
                        FROM trails''')
        
        for row in cur:
            trailscore = 0
            differences = []    # List to keep track of which features vary from user's input.
            id1, name1, loc1, locname1, terrain1, type1, difficulty1, jumps1, drops1, berms1, rolls1, skinnies1 = row
            # Print statement for testing purposes
            #print(f'Name: {name1}\nTerrain: {terrain1}\nType: {type1}\nDifficulty: {difficulty1}\nJumps: {jumps1}\nBerms: {berms1}\nDrops: {drops1}\nRolls: {rolls1}\nSkinnies: {skinnies1}')
            
            # Check each condition, award a point to the trail if it matches
            if terrain == terrain1 or terrain == '*':
                trailscore += 1
            if type == type1 or type == '*':
                trailscore += 1
            if difficulty == difficulty1 or difficulty == '*':
                trailscore += 1
            if jumps == jumps1:
                trailscore += 1
            if drops == drops1:
                trailscore += 1
            if berms == berms1:
                trailscore += 1
            if rolls == rolls1:
                trailscore += 1
            if skinnies == skinnies1:
                trailscore += 1
            # Set image path based on trail difficulty
            if difficulty1 == 'green':
                difficulty1 = '/static/images/green.png'
            elif difficulty1 == 'blue':
                difficulty1 = '/static/images/blue.png'
            else:
                difficulty1 = '/static/images/black.png'
            # Adds trail to a list if its trailscore is 6 or more. 
            if trailscore > 5:
                trailData = (name1, locname1, trailscore, difficulty1, loc1)
                passedTrails.append(trailData)

        return render_template('results.html', trails=passedTrails)
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

@app.route('/register', methods=["GET", "POST"])
def register():
    form = regForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        password = password.encode('utf-8')                     # Convert to format for bcrypt
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())      # Hash password using generated salt

        with sqlite3.connect("data.db") as con:
            cur = con.cursor()

        cur.execute(''' SELECT username
                        FROM users
                        WHERE username=?''',
                        (username,))
        
        if cur.fetchone():      # If a user is found with that username
            form.username.data = ' '
            cur.close()
            return render_template('register.html', error="Username already taken!", form=form)
        
        # Insert the new user into the database 
        cur.execute(''' INSERT INTO users(username, pw_hash)
                        VALUES(?,?)''',
                        (username, hashed.decode('utf-8')))
        con.commit()

        cur.close()

        return redirect(url_for('login'))
        #return render_template('home.html', form=form)

    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
    # Uncomment line below to open up for outside connection for testing on other devices
    #app.run(host='0.0.0.0', port=5000)
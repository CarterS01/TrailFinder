#--- PYTHON MODULES ---
import sqlite3
from flask import Flask, render_template, redirect, url_for
import bcrypt
import pgeocode as pgeo
#--- .py FILES ---
from login import *
from register import *
from find import *
from user import *

con = sqlite3.connect("data.db")    # Create a connection to the database
app = Flask(__name__)               # Create a Flask object
app.config['SECRET_KEY'] = 'placeholder'
user = User(None, None)             # Create a blank user object

@app.route('/')
def home():
    return render_template('home.html', user=user)

@app.route('/find_a_trail', methods=["GET", "POST"])
def find_a_trail():
    form = findForm()
    if form.validate_on_submit():
        location = form.location.data
        radius = float(form.radius.data)
        terrain = form.terrain.data
        type = form.type.data
        difficulty = form.difficulty.data
        jumps = form.jumps.data
        drops = form.drops.data
        berms = form.berms.data
        rolls = form.rolls.data
        skinnies = form.skinnies.data
        passedTrails = []    # List that will later store which trails passed the trailscore test

        with sqlite3.connect("data.db") as con:
            cur = con.cursor()

        cur.execute(''' SELECT *
                        FROM trails''')
        
        for row in cur:
            trailscore = 0
            id1, name1, loc1, locname1, terrain1, type1, difficulty1, jumps1, drops1, berms1, rolls1, skinnies1 = row
            
            # Check each condition, award a point to the trail if it matches
            if terrain == terrain1 or terrain == 'terr_no':
                trailscore += 1
            if type == type1 or type == 'type_no':
                trailscore += 1
            if difficulty == difficulty1 or difficulty == 'diff_no':
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
                altText = 'Green difficulty icon'
            elif difficulty1 == 'blue':
                difficulty1 = '/static/images/blue.png'
                altText = 'Blue difficulty icon'
            else:
                difficulty1 = '/static/images/black.png'
                altText = 'Black difficulty icon'
            # Pass zip codes to calc_distance to determine how far they are from each other
            distance = calc_distance(location, loc1)
            # Adds trail to a list if its trailscore is 6 or more and the trail is within user's specified radius
            if trailscore > 5 and distance < radius:
                trailData = (name1, locname1, trailscore, difficulty1, loc1, altText)
                passedTrails.append(trailData)

        # If user is logged in, call function to update their preferences
        if user.auth == True:
            update_prefs(user, terrain, type, difficulty)

        return render_template('results.html', trails=passedTrails)
    return render_template('find.html', form=form)

# Function to update user preferences based on their Find A Trail searches
def update_prefs(user, terrain, type, difficulty):
    
    with sqlite3.connect('data.db') as con:
        cur = con.cursor()

    id = str(user.id).strip('(,)')   # Convert tuple to string and remove extra characters. I have no idea why this returns as a tuple in the first place

    # Update preference based on chosen terrain
    cur.execute(''' UPDATE preference
                    SET %s = %s + 1
                    WHERE user_id=?''' %
                    (terrain, terrain), (id,))
    con.commit()
    # Update preferences based on chosen trail type
    cur.execute(''' UPDATE preference
                    SET %s = %s + 1
                    WHERE user_id=?''' %
                    (type, type), (id,))
    con.commit()
    # Update preferences based on chosen difficulty
    cur.execute(''' UPDATE preference
                    SET %s = %s + 1
                    WHERE user_id=?''' %
                    (difficulty, difficulty), (id,))
    con.commit()

    cur.close()
    
# Function to calculate the distance between zip codes
def calc_distance(userCode, trailCode):
    search = pgeo.GeoDistance('US')
    distance = search.query_postal_code(userCode, trailCode)
    distance *= 0.6213712   # Convert km to mi
    return distance

@app.route('/login', methods=["GET", "POST"])
def login():
    form = loginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        with sqlite3.connect("data.db") as con:
            cur = con.cursor()

        # Search for matching username in the database
        cur.execute(''' SELECT username
                        FROM users
                        WHERE username=?''',
                        (username,))
            
        if cur.fetchone():     # Returns None if no matching username is found

            newPass = password.encode('utf-8')                  # Convert password into format accepted by bcrypt (b'password')
            hashed = bcrypt.hashpw(newPass, bcrypt.gensalt())   # Hash the password using a generated salt

            # Search users table in database to retrieve hashed password corresponding with username
            cur.execute('''SELECT pw_hash
                            FROM users
                            WHERE username=?''',
                            (username,))

            hashed = cur.fetchall()               # Store the hashed password
            res = str(hashed).strip('[](),\'')     # Strip unnecessary characters off of password, otherwise it will not match in checkpw

            # If entered password is successfully matched to hash
            # Args need to be encoded for bcrypt format
            if bcrypt.checkpw(password.encode('utf-8'), res.encode('utf-8')):
                cur.execute(''' SELECT id
                                FROM users
                                WHERE username=?''',
                                (username,))
                id = cur.fetchone()
                cur.close()
                login_user(id, username, user)
                return redirect(url_for('home'))
            # If entered password does not match hash
            else:
                cur.close()
                form.username.data = ''
                form.password.data = ''
                return render_template('login.html', error="ERROR: INCORRECT PASSWORD", form=form)

        # If no record matching user is found  
        else:
            cur.close()
            form.username.data = ''
            form.password.data = ''
            return render_template('login.html', error="ERROR: USER NOT FOUND", form=form)
        
    return render_template('login.html', form=form)

def login_user(id, username, user):
    user.id = id
    user.username = username
    user.auth = True

@app.route('/logout', methods=["GET", "POST"])
def logout():
    user.id = None
    user.username = None
    user.auth = False
    return redirect(url_for('home'))

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
            return render_template('register.html', error="ERROR: USERNAME ALREADY EXISTS", form=form)
        
        # Insert the new user into the database 
        cur.execute(''' INSERT INTO users(username, pw_hash)
                        VALUES(?,?)''',
                        (username, hashed.decode('utf-8')))
        con.commit()

        # Get the newly created user's ID to pass into login_user() and the preferences INSERT statement
        cur.execute(''' SELECT id
                        FROM users
                        WHERE username=?''',
                        (username,))
        
        id = ''.join(cur.fetchone())

        # Create a table in preferences for the user
        cur.execute(''' INSERT INTO preference (user_id)
                        VALUES (?)''',
                        (id))
        con.commit()

        login_user(id, username, user)     # Log the user in automatically upon registration

        cur.close()

        return render_template('home.html', user=user)

    return render_template('register.html', form=form)

@app.route('/recommend_a_trail')
def recommend_a_trail():
    if user.auth == True:

        id = user.id

        passedTrails = []   # Empty list to store trails that match criteria

        with sqlite3.connect('data.db') as con:
            cur = con.cursor()

        # Query for the user's row in the preference table. 
        cur.execute('''SELECT *
                        FROM preference
                        WHERE user_id=?''',
                        (id))
        
        for row in cur:
            user_id, flow, tech, terr_no, up, down, both, type_no, green, blue, black, diff_no = row

        # Compare statements for terrain
        if flow > tech:
            terrain = 'flow'
        else:
            terrain = 'tech'
        # Compare statements for type
        if up > down and up > both:
            type = 'up'
        elif down > up and down > both:
            type = 'down'
        else:
            type = 'both'
        # Compate statements for difficulty
        if green > blue and green > black:
            difficulty = 'green'
        elif blue > green and blue > black:
            difficulty = 'blue'
        else:
            difficulty = 'black'

        cur.execute(''' SELECT *
                        FROM trails''')
        
        # Query for trails based on results
        for row in cur:
            id1, name1, loc1, locname1, terrain1, type1, difficulty1, jumps1, drops1, berms1, rolls1, skinnies1 = row

            if terrain == terrain1 and type == type1 and difficulty == difficulty1:
                # Set image path based on trail difficulty
                if difficulty1 == 'green':
                    difficulty1 = '/static/images/green.png'
                    altText = 'Green difficulty icon'
                elif difficulty1 == 'blue':
                    difficulty1 = '/static/images/blue.png'
                    altText = 'Blue difficulty icon'
                else:
                    difficulty1 = '/static/images/black.png'
                    altText = 'Black difficulty icon'

                trailData = (name1, locname1, difficulty1, loc1, altText)
                passedTrails.append(trailData)

        return render_template('recs.html', trails=passedTrails)
    else:
        return render_template('not_logged.html')

@app.route('/saved_trails')
def saved_trails():
    if user.auth == True:
        return render_template('saved.html')
    else:
        return render_template('not_logged.html')

if __name__ == "__main__":
    app.run(debug=True)
    # Uncomment line below to open up for outside connection for testing on other devices
    #app.run(host='0.0.0.0', port=5000)
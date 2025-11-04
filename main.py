import sqlite3
from flask import Flask, render_template, request
from login import *

con = sqlite3.connect("data.db")    #Create a connection to the database
app = Flask(__name__)               #Create a Flask object
app.config['SECRET_KEY'] = 'placeholder'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/find_a_trail')
def find_a_trail():
    return render_template('find.html')

@app.route('/recommend_a_trail')
def recommend_a_trail():
    return render_template('rec.html')

@app.route('/saved_trails')
def saved_trails():
    return render_template('saved.html')

@app.route('/login', methods=["GET", "POST"])
def submit():
    form = loginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        #print(f'{username}\n{password}')
        #form.username.data = ''
        #form.password.data = ''

        with sqlite3.connect("data.db") as con:
            cur = con.cursor()

        cur.execute(''' SELECT username, pw_hash
                        FROM users
                        WHERE username=? and pw_hash=?''',
                        (username, password))
        
        if cur.fetchone():      # Returns None is nothing matches the query
            cur.close()
            return render_template('home.html')
        else:                   # If no record is found
            cur.close()
            form.username.data = ''
            form.password.data = ''
            return render_template('login.html', error="Incorrect username or password!", form=form)
        
    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
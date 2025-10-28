import sqlite3
from flask import Flask, render_template

con = sqlite3.connect("data.db")    #Create a connection to the database
app = Flask(__name__)               #Create a Flask object

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

@app.route('/login')
def login():
    with sqlite3.connect("data.db") as con:
        cur = con.cursor()
    return render_template('login.html')

@app.route('/placeholder')
def placeholder():
    return render_template('placeholder.html')

if __name__ == "__main__":
    app.run(debug=True)
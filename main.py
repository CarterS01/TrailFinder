from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
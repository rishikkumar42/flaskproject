#!/usr/bin/env python3
import requests
from flask import Flask, request
from models import db, Movie 
from fetch_data import fetch_data
from flask_migrate import Migrate 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Movies.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db object with the Flask app
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
        <label for="user_input">Enter your word below and hit submit:</label><br>
        <input type="text" id="user_input" name="user_input"><br>
        <input type="submit" value="Submit!">
    </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text

@app.route("/movies")
def display_movies():
    db.session.query(Movie).delete()
    db.session.commit()
    fetch_data()
    movies = Movie.query.all()
    print(movies)
    movie_list = "<h1>List of Movies1:</h1><ul>"
    for movie in movies:
        movie_list += f"<li>{movie.title} - Released on {movie.release_date}</li>"
    movie_list += "</ul>"

    return movie_list

if __name__ == "__main__":

    app.run(debug=True)
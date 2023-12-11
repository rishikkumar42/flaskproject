#!/usr/bin/env python3
from email import header
import requests
from flask import Flask, request, render_template
from backend.models import db, Movie 
from backend.fetch_data import fetch_data
from backend.searchPage import fetch_search_data
from backend.data_analyzer import randomizeMovieSelect
from flask_migrate import Migrate 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Movies.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the db object with the Flask app
db.init_app(app)
migrate = Migrate(app, db)

def headerdisplay():
    header = "<div style='border-bottom: 2px solid black; padding-bottom: 5px; margin-bottom: 10px;'><h1>Movie Buff Recs</h1></div>"
    buttons = "<button style='font-weight:bold; font-size:25px; margin-right: 30px;' onclick=\"window.location.href='/rand_gen_form'\">Random Movie Generator</button>"
    buttons += "<button style='font-weight:bold; font-size:18px; margin-right: 30px;' onclick=\"window.location.href='/'\">Home Page</button>"
    buttons += "<button style='font-weight:bold; font-size:18px; margin-right: 30px;' onclick=\"window.location.href='/action'\">View Top Action Movies</button>"
    buttons += "<button style='font-weight:bold; font-size:18px; margin-right: 30px;' onclick=\"window.location.href='/movies'\">Your Saved Movies</button>"
    buttons += "<button style='font-weight:bold; font-size:18px; margin-right: 30px;' onclick=\"window.location.href='/search'\">Search for a Movie</button>"

    return header, buttons

def movieTableDisplay(movies, title):
    
    movie_list = f"<h2>{title}</h2>"
    movie_list += "<table border='1'><tr><th>Poster</th><th>Title</th><th>Release Date</th><th>Overview</th><th>Vote Average</th></tr>"
    for movie in movies:
        movie_list += f"<tr><td><img src='https://image.tmdb.org/t/p/w500/{movie.poster_path}' alt='Poster' width='150'></td><td>{movie.title}</td><td>{movie.release_date}</td><td>{movie.overview}</td><td>{movie.vote_average}</td></tr>"
    movie_list += "</table>"

    return movie_list

@app.route("/")
def main():
    params = {
        'include_adult': 'false',
        'include_video': 'false',
        'language': 'en-US',  
        'sort_by': 'popularity.desc', 
        'primary_release_year': '2023' 
        
    } 
    db.session.query(Movie).delete()
    db.session.commit()
    
    fetch_data(params)
    movies = Movie.query.all()
    title = "List of Movies Popular Right Now"
    movie_list = movieTableDisplay(movies, title)
    header, buttons = headerdisplay()

    return f"{header}{buttons}{movie_list}"

#This code shows the main page of latest popular movies
@app.route("/action")
def display_movies():
    db.session.query(Movie).delete()
    db.session.commit()
   
    params = {
        'include_adult': 'false',
        'include_video': 'false',
        'language': 'en-US',  
        'sort_by': 'popularity.desc', 
        'primary_release_year': '2023',
        'with_genres': '28'
        
    }

    fetch_data(params)

    movies = Movie.query.all()
    title = "Top Action Movies"
    movie_list = movieTableDisplay(movies, title)
    header, buttons = headerdisplay()

    return f"{header}{buttons}{movie_list}"

@app.route("/search")
def takeSearchQuery():
    return render_template('search_form.html') 

@app.route("/search_display", methods=["POST"])
def display_search_movies():
    db.session.query(Movie).delete()
    db.session.commit()
    user_input= request.form.get("user_input", "")
    params = {
        'include_adult': 'false',
        'language': 'en-US',  
        'query': str(user_input)
        
    }
    fetch_search_data(params)
    movies = Movie.query.all()

    title = "Search results for " + user_input
    movie_list = movieTableDisplay(movies, title)
    header, buttons = headerdisplay()

    return f"{header}{buttons}{movie_list}"

@app.route("/rand_gen_form")
def randomGenForm():
    return render_template('user_input_form.html') 

@app.route("/random_gen_display", methods=["POST"])
def displayRandGenMovie():
    db.session.query(Movie).delete()
    db.session.commit()
    user_input_genres= request.form.getlist("preference")
    user_input_year = request.form['year']
    user_input_rating = request.form['rating']

    params = {
        'include_adult': 'false',
        'language': 'en-US',  
        'primary_release_year': str(user_input_year),
        'vote_average': str(user_input_rating)
        
    }
    movies_recc = randomizeMovieSelect(params, user_input_rating, user_input_genres)

    title = "Your Randomized Movie Reccomendation is..."
    header, buttons = headerdisplay()
    movie_list = f"<h2>Your Recommended Movie is ...</h2>"
    movie_list += "<table border='1'><tr><th>Poster</th><th>Title</th><th>Release Date</th><th>Overview</th><th>Vote Average</th></tr>"
    movie_list += f"<tr><td><img src='https://image.tmdb.org/t/p/w500/{movies_recc.poster_path}' alt='Poster' width='150'></td><td>{movies_recc.title}</td><td>{movies_recc.release_date}</td><td>{movies_recc.overview}</td><td>{movies_recc.vote_average}</td></tr>"
    
    return f"{header}{buttons}{movie_list}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Heroku-provided port or default to 5000
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
import requests
from backend.models import db, Movie
from backend.fetch_data import fetch_data
from sqlalchemy import desc

#this file contains code to analyze the data based on users input and output the results

def randomizeMovieSelect(params, rating, genrePref):
    #use api to get the keys to the genres to analyze later
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNjk0OWI3OTZkYmY4OGZjMDlmZGM0NjA5YmI2MGI5MCIsInN1YiI6IjY1NzU0YjFhODlkOTdmMDExZGNjYWJkMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7HEyAJ3TNcXvUAjt0vRHlYYHhivhPG1NIYNNTvtUlfk'
    base_url = 'https://api.themoviedb.org/3/genre/movie/list?language=en'
    
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(base_url, headers=headers)
    if response.status_code == 200:
        genres = response.json().get('genres', [])

    #take user preferences and use api to fetch appropriate data. 

    movies = fetch_data(params)
    recc_movie = Movie.query.order_by(desc(Movie.vote_average)).first()
    
    #in future, there will be more data analyzer to determine more optimized results using movie genres the user selected

    return recc_movie
import requests
from backend.models import db, Movie  
#this code is similar to fetch_data but it uses the api tto fetch data using the users entered query 

def fetch_search_data(query):
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNjk0OWI3OTZkYmY4OGZjMDlmZGM0NjA5YmI2MGI5MCIsInN1YiI6IjY1NzU0YjFhODlkOTdmMDExZGNjYWJkMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7HEyAJ3TNcXvUAjt0vRHlYYHhivhPG1NIYNNTvtUlfk'
    base_url = 'https://api.themoviedb.org/3/search/movie?'

    url = f"{base_url}{'&'.join([f'{key}={value}' for key, value in query.items()])}"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        movies_data = response.json().get('results', [])

        for movie in movies_data:
            new_movie = Movie(
                id=movie.get('id'),
                title=movie.get('title'),
                release_date=movie.get('release_date'),
                vote_average=movie.get('vote_average'),
                overview = movie.get('overview'),
                poster_path = movie.get('poster_path'),
            )
            db.session.add(new_movie)
        db.session.commit()
    else:
        print('Failed to fetch data from TMDB API')

if __name__ == "__main__":
    fetch_data()
import requests
from models import db, Movie  

def fetch_data():
    # Replace 'YOUR_TMDB_API_KEY' with your TMDB API key
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhNjk0OWI3OTZkYmY4OGZjMDlmZGM0NjA5YmI2MGI5MCIsInN1YiI6IjY1NzU0YjFhODlkOTdmMDExZGNjYWJkMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.7HEyAJ3TNcXvUAjt0vRHlYYHhivhPG1NIYNNTvtUlfk'
    base_url = 'https://api.themoviedb.org/3/discover/movie?'

    # Parameters for fetching movies (modify as needed)
    params = {
        'api_key': api_key,
        'sort_by': 'popularity.desc', 
        'include_adult': 'false',
        'include_video': 'false',
        'release_year': '2020',  
        'language': 'en-US'  
    }
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&primary_release_year=2020&sort_by=popularity.desc"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    print('hello')
    response = requests.get(url, headers=headers)
    print(response.json())
    if response.status_code == 200:
        movies_data = response.json().get('results', [])

        for movie in movies_data:
            new_movie = Movie(
                id=movie.get('id'),
                title=movie.get('title'),
                release_date=movie.get('release_date'),
                vote_average=movie.get('vote_average')
            )
            db.session.add(new_movie)
        db.session.commit()
    else:
        print('Failed to fetch data from TMDB API')

if __name__ == "__main__":
    fetch_data()
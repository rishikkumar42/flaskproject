import unittest
from unittest.mock import patch, MagicMock
from app import app, db, Movie
from backend.fetch_data import fetch_data


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    #this test checks if the main home page works and loads successfully 
    def test_main_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    #this test checks if the top action pages works successfully
    def test_action_route(self):
        response = self.app.get('/action')
        self.assertEqual(response.status_code, 200)
    
    #this test creates fake mock data to test the fetch_data function
    @patch('app.requests.get')
    def test_fetch_data(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'results': [
                {'id': 1, 'title': 'Movie 1', 'vote_average': 8.5},
                {'id': 2, 'title': 'Movie 2', 'vote_average': 7.9},
                
            ]
        }

        mock_get.return_value = mock_response

        #basic mock params setup 
        params = {
            'include_adult': 'false',
            'language': 'en-US',
        }
        with app.app_context():
            from backend.fetch_data import fetch_data
            fetch_data(params)

            movies = Movie.query.all()
            self.assertEqual(len(movies), 22) #assertion is for 22 because the db has 20 to start and the 2 mock ones get added


if __name__ == '__main__':
    unittest.main()
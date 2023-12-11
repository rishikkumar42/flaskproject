import unittest
from app import app, db, Movie  

class TestIntegration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True  
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  
        self.app = app.test_client()
        db.create_all()  

    def tearDown(self):
        db.session.remove()  
        db.drop_all()  

    #testing for main home page successfully working
    def test_main_route_integration(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    #tests is the top action movies page is working successfully 
    def test_action_route_integration(self):
        response = self.app.get('/action')
        self.assertEqual(response.status_code, 200)

    #tests is search page works with a mock search query (horror)
    def test_search_route_integration(self):
        response = self.app.post('/search_display', data={'user_input': 'horror'})
        self.assertEqual(response.status_code, 200)


    # Add more integration tests for other routes and interactions

if __name__ == '__main__':
    unittest.main()
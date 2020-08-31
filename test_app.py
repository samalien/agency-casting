import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Actor, Movie, Performance
from app import create_app
from config import *

# Create dict with Authorization key and Bearer token as values.
# Later used by test classes as Header

casting_assistant_auth_header = {
    'authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'authorization': bearer_tokens['casting_director']
}

casting_producer_auth_header = {
    'authorization': bearer_tokens['casting_producer']
}


class CastingAgencyTest(unittest.TestCase):
    """This class represents the casting agency test """

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agencydb"
        self.database_path = "postgresql://{}/{}".format('postgres:alien@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {
            'title': 'Gladiator?',
            'release_date': '20/8/9',
        }
        self.new_actor = {
            'name': 'Jennifer Lawrence',
            'age': '30',
            'gender': 'Female'
        }

    def tearDown(self):
        # Executed after reach test
        pass

    # ----------------------------------------------------------------------------------------------------------------
    # TESTS GET MOVIE
    # ----------------------------------------------------------------------------------------------------------------
    def test_get_movies(self):
        res = self.client().get('/movies', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_error_404_get_movies(self):
        # Error GET all movies
        res = self.client().get('/movies?page=100', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_error_401_get_all_movies(self):
        # GET all movies Authorization
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unauthorized')

    # ----------------------------------------------------------------------------------------------------------------
    # TESTS PATCH MOVIE
    # ----------------------------------------------------------------------------------------------------------------
    def test_update_movie(self):
        res = self.client().patch('/movies/2', json={"release_date": "2020/1/2"}, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_400_update_movie(self):
        res = self.client().patch('/movies/1', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_404_update_movie(self):
        res = self.client().patch('/movies/100', json={"release_date": "2020/5/4"},
                                  headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    # ----------------------------------------------------------------------------------------------------------------
    # TESTS POST MOVIE
    # ----------------------------------------------------------------------------------------------------------------
    def test_create_new_movie(self):
        new_movie = {
            'title': 'Abdelli',
            'release_date': "2020/5/4"
        }

        res = self.client().post('/movies/search', json=new_movie, headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_error_422_create_new_movie(self):
        # Test Error POST new movie

        movie_without_title = {
            "release_date": "2020/8/7"
        }

        res = self.client().post('/movies/search', json=movie_without_title, headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_error_403_create_movie(self):
        # Test create movie with wrong permissions
        new_movie = {
            "title": "abdelli",
            "release_date": "2020/8/7"
        }
        res = self.client().post('/movies/search', json=new_movie, headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

    def test_get_movie_search_with_results(self):
        res = self.client().post('/movies/search', json={'searchTerm': 'the'}, headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 2)
        self.assertTrue(data['total_movies'])

    def test_get_movie_search_without_results(self):
        res = self.client().post('/movies/search', json={'searchTerm': 'helloxgxgxgxgx'},
                                 headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 0)
        self.assertTrue(data['total_movies'])

    # ----------------------------------------------------------------------------------------------------------------
    # TESTS DELETE MOVIE
    # ----------------------------------------------------------------------------------------------------------------
    def test_delete_movie(self):
        res = self.client().delete('/movies/3', headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_error_404_delete_movie(self):
        # Test DELETE non existing movie
        res = self.client().delete('/movies/1254', headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_error_403_delete_movie(self):
        # Test DELETE movie with wrong permissions
        res = self.client().delete('/movies/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

    # ----------------------------------------------------------------------------------------------------------------
    # TESTS GET ACTOR
    # ----------------------------------------------------------------------------------------------------------------
    def test_get_actors(self):
        res = self.client().get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_error_404_get_actors(self):
        # Error GET all actors
        res = self.client().get('/actors?page=100', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_error_401_get_all_actors(self):
        # GET all actors Authorization
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unauthorized')

    # ----------------------------------------------------------------------------------------------------------------
    # TESTS PATCH ACTOR
    # ----------------------------------------------------------------------------------------------------------------
    def test_update_actor(self):
        res = self.client().patch('/actors/1', json={"age": "50"}, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['updated'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_400_update_actor(self):
        res = self.client().patch('/actors/1', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

    def test_404_update_actor(self):
        res = self.client().patch('/actors/100', json={"age": "50"}, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    # ----------------------------------------------------------------------------------------------------------------
    # TESTS POST ACTOR
    # ----------------------------------------------------------------------------------------------------------------
    def test_create_new_actor(self):
        new_actor = {
            'name': 'Abdelli',
            'age': '55',
            'gender': 'Male'
        }

        res = self.client().post('/actors/search', json=new_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_error_422_create_new_actor(self):
        # Test Error POST new actor

        actor_without_name = {
            'age': "55",
            'gender': 'Male'
        }

        res = self.client().post('/actors/search', json=actor_without_name, headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')

    def test_error_403_create_actor(self):
        # Test create actor with wrong permissions
        new_actor = {
            "name": "dalila",
            "age": "20",
            "gender": "Female"
        }
        res = self.client().post('/actors/search', json=new_actor, headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')

    def test_get_actor_search_with_results(self):
        res = self.client().post('/actors/search', json={'searchTerm': 'will'}, headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 2)
        self.assertTrue(data['total_actors'])

    def test_get_actor_search_without_results(self):
        res = self.client().post('/actors/search', json={'searchTerm': 'helloxgxgxgxgx'},
                                 headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['actors']), 0)
        self.assertTrue(data['total_actors'])

    # ----------------------------------------------------------------------------------------------------------------
    # TESTS DELETE ACTOR
    # ----------------------------------------------------------------------------------------------------------------
    def test_delete_actor(self):
        res = self.client().delete('/actors/3', headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_error_404_delete_actor(self):
        # Test DELETE non existing actor
        res = self.client().delete('/actors/1254', headers=casting_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Resource not found')

    def test_error_403_delete_movie(self):
        # Test DELETE actor with wrong permissions
        res = self.client().delete('/actors/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

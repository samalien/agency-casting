import os

from flask import Flask, request, abort, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import redirect

from models import setup_db, Movie, Actor, Performance, db
from flask_migrate import Migrate
from auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth


AUTH0_CALLBACK_URL = "https://agency-casting.herokuapp.com/login_result"
AUTH0_CLIENT_ID = "4bH07NXNIJ02BMCRkZsN85JYRDkB4sVI"
AUTH0_CLIENT_SECRET = "udacity"
AUTH0_DOMAIN = "dev-mrlzc2vg.us.auth0.com"
AUTH0_BASE_URL = 'https://dev-mrlzc2vg.us.auth0.com'
AUTH0_AUDIENCE = "casting"

MOVIES_PER_PAGE = 10
ACTORS_PER_PAGE = 10
db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    migrate = Migrate(app, db)
    app.secret_key = "udacity"

    # ------------------------------------------------------------------------
    # set Access-Control-allow, API Cofiguration
    # ------------------------------------------------------------------------
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PUT,PATCH,DELETE,OPTIONS')
        return response

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    # --------------------------------------------------------------------------
    # Custom Functions
    # --------------------------------------------------------------------------
    def paginate_movies(request, selection):
        page = request.args.get('page', 1, type=int)

        # determine the movies for each page
        start = (page - 1) * MOVIES_PER_PAGE
        end = start + MOVIES_PER_PAGE

        formatted_movies = [movie.format() for movie in selection]
        current_movies = formatted_movies[start:end]
        return current_movies

    def paginate_actors(request, selection):
        page = request.args.get('page', 1, type=int)

        # determine the actors for each page
        start = (page - 1) * ACTORS_PER_PAGE
        end = start + ACTORS_PER_PAGE

        formatted_actors = [actor.format() for actor in selection]
        current_actors = formatted_actors[start:end]
        return current_actors

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri="https://agency-casting.herokuapp.com/login_result",
                                        audience="casting")

    @app.route('/login_result')
    def login_result():
        # Handles response from token endpoint

        res = auth0.authorize_access_token()
        token = res.get('access_token')

        # Store the user information in flask session.
        session['jwt_token'] = token
        return redirect('/dashboard')

        # return render_template('dashboard.html',token=session['jwt_token'])

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html',
                               token=session['jwt_token']
                               )


    # ------------------------------------------------------------------------
    # API endpoints : movies GET/POST/DELETE/PATCH
    # ------------------------------------------------------------------------

    # GET MOVIES
    @app.route('/movies', methods=['GET'])
    @requires_auth('read:movie')
    def get_movies(payload):

        movies = Movie.query.all()
        current_movies = paginate_movies(request, movies)

        # if there are no movies abort 404
        if len(current_movies) == 0:
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(movies)
        })

    # CREATE / SEARCH MOVIES
    @app.route('/movies/search', methods=['POST'])
    @requires_auth('post:movie')
    def create_search_movie(payload):
        # Get request json
        body = request.get_json()

        if body is None:
            abort(400)

        # load data from body
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)
        search = body.get('searchTerm', None)
        if not search:
            # ensure all fields have data
            if not new_title:
                abort(422)
            if not new_release_date:
                abort(422)

        try:
            if search:
                selection = Movie.query.order_by(Movie.id) \
                    .filter(Movie.title.ilike('%{}%'.format(search)))
                current_movies = paginate_movies(request, selection)

                # return data to view
                return jsonify({
                    'success': True,
                    'movies': current_movies,
                    'total_movies': len(Movie.query.all())
                })
            else:

                # create and insert new movie
                movie = Movie(title=new_title, release_date=new_release_date)
                movie.insert()

                movies = Movie.query.all()
                formatted_movies = [movie.format() for movie in movies]

                # return data to view
                return jsonify({
                    'success': True,
                    'created': movie.id,
                    'movies': formatted_movies,
                    'total_movies': len(movies)
                })
        except:
            abort(401)

    # DELETE MOVIE
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        # Abort if no movie_id has been provided
        if not movie_id:
            abort(400)

        # get the movie should be deleted
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        # if no movie found abort 404
        if movie is None:
            abort(404)
        try:
            # delete the movie
            movie.delete()

            movies = Movie.query.all()
            formatted_movies = [movie.format() for movie in movies]

            # return success response
            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': formatted_movies,
                'total_movies': len(movies)
            })
        except:
            # if problem deleting
            abort(422)

    # UPDATE MOVIE
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(payload, movie_id):
        body = request.get_json()

        if not movie_id:
            abort(400)

        if not body:
            abort(400)

        # get the movie
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        # if no movie found abort 404
        if movie is None:
            abort(404)
        try:
            if 'title' in body:
                movie.title = body.get('title')
            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            # update the movie
            movie.update()

            movies = Movie.query.all()
            formatted_movies = [movie.format() for movie in movies]

            # return success response
            return jsonify({
                'success': True,
                'updated': movie_id,
                'movies': formatted_movies,
                'total_movies': len(movies)
            })
        except:
            # if problem updating
            abort(401)

    # GET MOVIES BY ACTOR
    @app.route('/actors/<actor_id>/movies', methods=['GET'])
    @requires_auth('read:movie')
    def get_movies_by_actor(payload, actor_id):
        performances = Performance.query.filter(Performance.actor_id == actor_id).all()

        if len(performances) == 0:
            abort(404)

        movies = {}
        for movie in performances:
            movie_actor = Movie.query.filter(Movie.id == movie.movie_id).first()
            movies[movie.id] = movie_actor.format()

        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies_by_actor': len(movies)
        })

    # ------------------------------------------------------------------------
    # API endpoints : actors GET/POST/DELETE/PATCH
    # ------------------------------------------------------------------------

    # GET ACTORS
    @app.route('/actors', methods=['GET'])
    @requires_auth('read:movie')
    def get_actors(payload):
        actors = Actor.query.all()
        current_actors = paginate_actors(request, actors)

        # if there are no actors abort 404
        if len(current_actors) == 0:
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(actors)
        })

    # CREATE / SEARCH BY NAME
    @app.route('/actors/search', methods=['POST'])
    @requires_auth('post:actor')
    def create_search_actor(payload):
        # Get request json
        body = request.get_json()

        if body is None:
            abort(400)

        # load data from body
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Actor.query.order_by(Actor.id) \
                    .filter(Actor.name.ilike('%{}%'.format(search)))
                current_actors = paginate_actors(request, selection)

                # return data to view
                return jsonify({
                    'success': True,
                    'actors': current_actors,
                    'total_actors': len(Actor.query.all())
                })
            else:
                # ensure all fields have data
                if not new_name or not new_age or not new_gender:
                    abort(422)

                # create and insert new movie
                actor = Actor(name=new_name, age=new_age, gender=new_gender)
                actor.insert()

                actors = Actor.query.all()
                formatted_actors = [actor.format() for actor in actors]

                # return data to view
                return jsonify({
                    'success': True,
                    'created': actor.id,
                    'actors': formatted_actors,
                    'total_actors': len(actors)
                })
        except:
            abort(422)

    # DELETE ACTOR
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        # get the actor
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        # if no actor found abort 404
        if actor is None:
            abort(404)
        try:
            # delete the actor
            actor.delete()

            actors = Actor.query.all()
            formatted_actors = [actor.format() for actor in actors]

            # return success response
            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': formatted_actors,
                'total_actors': len(actors)
            })
        except:
            # if problem deleting
            abort(422)

    # UPDATE ACTOR
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(payload, actor_id):
        body = request.get_json()

        if not actor_id:
            abort(400)

        if not body:
            abort(400)

        # get the actor
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        # if no actor found abort 404
        if actor is None:
            abort(404)
        try:
            if 'name' in body:
                actor.name = body.get('name')
            if 'age' in body:
                actor.age = int(body.get('age'))
            if 'gender' in body:
                actor.gender = body.get('gender')

            # update the actor
            actor.update()

            actors = Actor.query.all()
            formatted_actors = [actor.format() for actor in actors]

            # return success response
            return jsonify({
                'success': True,
                'updated': actor_id,
                'actors': formatted_actors,
                'total_actors': len(actors)
            }), 200
        except:
            # if problem updating
            abort(401)

    # GET ACTORS BY MOVIE
    @app.route('/movies/<movie_id>/actors', methods=['GET'])
    @requires_auth('read:actor')
    def get_actors_by_movie(payload, movie_id):
        performances = Performance.query.filter(Performance.movie_id == movie_id).all()

        if len(performances) == 0:
            abort(404)

        actors = {}
        for actor in performances:
            actor_movie = Actor.query.filter(Actor.id == actor.actor_id).first()
            actors[actor.id] = actor_movie.format()

        return jsonify({
            'success': True,
            'actors': actors,
            'total_actors_by_movie': len(actors)
        })

    # ------------------------------------------------------------------------------------
    # Error handler
    # ------------------------------------------------------------------------------------

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'unauthorized'
        }), 401

    @app.errorhandler(403)
    def unauthorized_error(error):
        return jsonify({
            'success': False,
            'error': 403,
            'message': 'Permission not found'
        }), 403

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

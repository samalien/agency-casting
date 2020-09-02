import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine

database_name = 'agencydb'
database_local_path = "postgres://{}@{}/{}".format('postgres:alien', 'localhost:5432', database_name)
database_path = os.environ.get('DATABASE_URL', database_local_path)
db = SQLAlchemy()


# binds a flask application and a SQLAlchemy services
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.drop_all()
    db.create_all()
    initialise_database()


def initialise_database():
    movie = Movie(title='The Grudge', release_date='2020/1/3')
    movie.insert()
    movie.insert()
    movie = Movie(title='Weathering with You', release_date='2016/5/4')
    movie.insert()

    actor = Actor(name='Will smith', age=25, gender='Male')
    actor.insert()
    actor = Actor(name='William powell', age=53, gender='Male')
    actor.insert()

    performance = Performance(movie_id=1, actor_id=1, actor_fee=600)
    performance.insert()
    performance = Performance(movie_id=2, actor_id=1, actor_fee=500)
    performance.insert()


# --------------------------------------------------------
# Movie
# --------------------------------------------------------
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    performances = db.relationship('Performance', backref='movies', lazy=True)

    def __repr__(self):
        return f'<Movie ID:{self.id}, Movie Title: {self.title}, Date:{self.release_date} >'

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


# -------------------------------------------------------------
# Actor
# -------------------------------------------------------------

class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<ID: {self.id}, NAME: {self.name}, AGE: {self.age}, GENDER: {self.gender}>'

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


# ----------------------------------------------------------------------
# Performane
# ----------------------------------------------------------------------

class Performance(db.Model):
    __tablename__ = 'performances'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'))
    actor_fee = db.Column(db.Float)

    def __repr__(self):
        return f'<ID: {self.id}, MOVIE_ID: {self.movie_id}, ACTOR_ID: {self.actor_id}, ACTOR_FEE: {self.actor_fee}>'

    def __init__(self, movie_id, actor_id, actor_fee):
        self.movie_id = movie_id
        self.actor_id = actor_id
        self.actor_fee = actor_fee

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.selete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'actor_id': self.actor_id,
            'actor_fee': self.actor_fee
        }

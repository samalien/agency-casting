
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine


database_name = 'agencydb'
# database_path = "postgres://{}@{}/{}". format('postgres:alien','localhost:5432', database_name)
database_path = "postgres://mzlssobwtfvevv:775b42b209c4c1a60d328af6a2579b1cf71e4dc3274d263732a31599a24b9913@ec2-52-200-111-186.compute-1.amazonaws.com:5432/d4m6kfhcpulj2t"
db=SQLAlchemy()

# binds a flask application and a SQLAlchemy service
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"]=database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app=app
    db.init_app(app)
    db.create_all()
#--------------------------------------------------------
# Movie
#--------------------------------------------------------
class Movie(db.Model):
    __tablename__='movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False )
    release_date = db.Column(db.DateTime, nullable=False)
    performances = db.relationship('Performance', backref='movies', lazy=True)

    def __repr__(self):
        return f'<Movie ID:{self.id}, Movie Title: {self.title}, Date:{self.release_date} >'

    def __init__(self,title,release_date):
        self.title=title
        self.release_date=release_date

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

    def __init__(self,name,age,gender):
        self.name= name
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

    def __init__(self,movie_id, actor_id, actor_fee):
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
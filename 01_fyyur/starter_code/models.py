from flask import Flask
from config import *
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

db = SQLAlchemy()


def db_setup(app):
    app.config.from_object('config')
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    return db

# app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
# app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
# app.config['SECRET_KEY']=SECRET_KEY

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120),nullable=False)
    address = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120),nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    artist_id =db.Column(db.Integer, db.ForeignKey('Artist.id'))


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(),nullable=False)
    city = db.Column(db.String(120),nullable=False)
    state = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    artists= db.relationship('Venue', backref='Artist', lazy=True)

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True )
  db.Column('venue.id', db.Integer, db.ForeignKey('venue.id'), primary_key=True)
  db.Column('artist.id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)

# db.init_app(app)
# db.create_all()
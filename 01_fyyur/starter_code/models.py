from flask import Flask
from config import *
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

db = SQLAlchemy()


def db_setup(app):
    app.config.from_object('config')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)
    return db


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship("Show", backref=db.backref("showss", lazy=True))
  
    def __repr__(self):
      return f'<Venue: { self.name }>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship("Show", backref=db.backref("shows", lazy=True))

    def __repr__(self):
      return f'<Artist: { self.name }>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__  = 'Shows'

  id = db.Column(db.Integer, primary_key=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.String, nullable=False)

  venue = db.relationship("Venue", backref=db.backref("shows_venue", lazy=True))
  artist = db.relationship("Artist", backref=db.backref("shows_artist", lazy=True))

  def __repr__(self):
      return f'<Show: { self.artist.name } at { self.venue.name }>'
      
# # db.init_app(app)
# # db.create_all()
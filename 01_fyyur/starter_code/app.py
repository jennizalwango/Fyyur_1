# # ----------------------------------------------------------------------------#
# # Imports
# # ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for)
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db_setup, Venue, Artist, Show
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment

# # ----------------------------------------------------------------------------#
# # App Config.
# # ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
db = db_setup(app)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = db.session.query(Venue).all()
  return render_template('pages/venues.html', areas=venues)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form['search_term']
  venues = db.session.query(Venue).with_entities(Venue.id, Venue.name).filter(Venue.name.contains(search_term)).all()
  data = []
  for venue in venues:
    upcoming = db.session.query(Show).filter_by(venue_id = venue.id).filter(
      Show.start_time > datetime.utcnow().isoformat()).all()
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(upcoming)
    })
  response={
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = db.session.query(Venue).filter_by(id = venue_id).first()
  data = {}

  if venue:
    data = venue.__dict__
    
    pastshows = db.session.query(Show).filter_by(venue_id = venue.id).filter(
      Show.start_time < datetime.utcnow().isoformat()).all()
    upcomingshows = db.session.query(Show).filter_by(venue_id = venue.id).filter(
      Show.start_time > datetime.utcnow().isoformat()).all()

    data["past_shows"] = pastshows
    data["upcoming_shows"] = upcomingshows
    data["past_shows_count"] = len(pastshows)
    data["upcoming_shows_count"] = len(upcomingshows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    venues = Venue(
      name=request.form.get("name"),
      city=request.form.get("city"),
      state=request.form.get("state"),
      address=request.form.get("address"),
      phone=request.form.get("phone"),
      facebook_link=request.form.get("facebook_link"),
      image_link=request.form.get("image_link")
    )
    
    db.session.add(venues)
    db.session.commit()
    
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(venue_id=id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = db.session.query(Artist).with_entities(Artist.id, Artist.name).all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form['search_term']
  venues = db.session.query(Venue).with_entities(Venue.id, Venue.name).filter(Venue.name.contains(search_term)).all()
  data = []
  for venue in venues:
    upcoming = db.session.query(Show).filter_by(venue_id = venue.id).filter(
      Show.start_time > datetime.utcnow().isoformat()).all()
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": len(upcoming)
    })
  response={
    "count": len(venues),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist = db.session.query(Artist).filter_by(id = artist_id).first()
  data = {}

  if artist:
    data = artist.__dict__
    
    pastshows = db.session.query(Show).filter_by(artist_id = artist.id).filter(
      Show.start_time < datetime.utcnow().isoformat()).all()
    upcomingshows = db.session.query(Show).filter_by(artist_id = artist.id).filter(
      Show.start_time > datetime.utcnow().isoformat()).all()

    data["past_shows"] = pastshows
    data["upcoming_shows"] = upcomingshows
    data["past_shows_count"] = len(pastshows)
    data["upcoming_shows_count"] = len(upcomingshows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    artists = Artist(
      name=request.form.get("name"),
      city=request.form.get("city"),
      state=request.form.get("state"),
      phone=request.form.get("phone"),
      genres=request.form.get("genres"),
      facebook_link=request.form.get("facebook_link"),
      image_link=request.form.get("image_link")
    )

    db.session.add(artists)
    db.session.commit()
    
  except:
    db.session.rollback()
  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Artist' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  show_list = []
  shows = db.session.query(Show).all()
  
  for s in shows:
    show = {}
    show["venue_id"] = s.venue_id
    show["venue_name"] = s.venue.name
    show["artist_id"] = s.artist_id
    show["artist_name"] = s.artist.name
    show["artist_image_link"] = s.artist.image_link
    show["start_time"] = s.start_time
    show_list.append(show)

  return render_template('pages/shows.html', shows=show_list)
  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    show = Show(artist_id=artist_id,
                venue_id=venue_id,
                start_time=start_time)

    db.session.add(show)
    db.session.commit()

  except:
    db.session.rollback()
    flash( 'An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
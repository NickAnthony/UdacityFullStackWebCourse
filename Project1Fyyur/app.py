#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from forms import *
from logging import Formatter, FileHandler
import babel
import datetime
import dateutil.parser
import json
import logging
import re

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False, default=[])
    website = db.Column(db.String(120), nullable=True, default=[])
    seeking_talent = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)

    def to_dict(self):
      return ({
        "id": self.id,
        "name": self.name,
        "genres": self.genres,
        "address": self.address,
        "city": self.city,
        "state": self.state,
        "phone": self.phone,
        "website": self.website,
        "facebook_link": self.facebook_link,
        "seeking_talent": self.seeking_talent,
        "seeking_description": self.seeking_description,
        "image_link": self.image_link
      })

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False, default=[])
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean(), nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)

    def to_dict(self):
      return ({
        "id": self.id,
        "name": self.name,
        "genres": self.genres,
        "city": self.city,
        "state": self.state,
        "phone": self.phone,
        "website": self.website,
        "facebook_link": self.facebook_link,
        "seeking_venue": self.seeking_venue,
        "seeking_description": self.seeking_description,
        "image_link": self.image_link
      })

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'),
                         nullable=False, default=1)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'),
                          nullable=False, default=1)

    def to_dict(self):
      return ({
        "id": self.id,
        "start_time": self.start_time.datetime('full'),
        "venue_id": self.venue_id,
        "artist_id": self.artist_id
      })

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
# Utils.
#----------------------------------------------------------------------------#

def get_upcoming_shows(artists_or_venue):
  return list(filter(
    lambda show: show.start_time >= datetime.now(), artists_or_venue.shows
  ))

def get_past_shows(artists_or_venue):
  return list(filter(
    lambda show: show.start_time < datetime.now(), artists_or_venue.shows
  ))

def get_num_upcoming_shows(artists_or_venue):
  return len(get_upcoming_shows(artists_or_venue))

def get_num_past_shows(artists_or_venue):
  return len(get_past_shows(artists_or_venue))

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
  # DONE: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.all()
  data = []
  for venue in venues:
      added_venue = False
      for location in data:
          # city and state already exist
          if (location["city"] == venue.city and
              location["state"] == venue.state):
              location["venues"].append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": get_num_upcoming_shows(venue),
              })
              added_venue = True
      if not added_venue:
          ## Add the location to the data and add the venue to the location
          data.append({
              "city": venue.city,
              "state": venue.state,
              "venues": [{
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": get_num_upcoming_shows(venue)
              }]
          })
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response = {
    "count": 0,
    "data": []
  }
  search_term = request.form.get('search_term', '')
  venues = Venue.query.all()
  for venue in venues:
    if re.search(search_term, venue.name, re.IGNORECASE):
      # Found a match
      response["data"].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": get_upcoming_shows(venue)
      })
      response["count"] = response["count"] + 1
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id
    chosen_venue = Venue.query.get(venue_id)
    upcoming_shows = get_upcoming_shows(chosen_venue)
    past_shows = get_past_shows(chosen_venue)
    upcoming_shows_count = len(upcoming_shows)
    past_shows_count = len(past_shows)
    response = chosen_venue.to_dict()
    response["upcoming_shows"] = upcoming_shows
    response["past_shows"] = past_shows
    response["upcoming_shows_count"] = upcoming_shows_count
    response["past_shows_count"] = past_shows_count
    return render_template('pages/show_venue.html', venue=response)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error_occured = False
  body = {
    'name': request.form.get('name', '')
  }
  try:
      new_venue = Venue(
        name = request.form.get('name', ''),
        city = request.form.get('city', None),
        state = request.form.get('state', None),
        address = request.form.get('address', None),
        phone = request.form.get('phone', None),
        image_link = request.form.get('image_link', None),
        genres = request.form.get('genres', []),
        facebook_link = request.form.get('facebook_link', None),
      )
      db.session.add(new_venue)
      db.session.commit()
      body['name'] = new_venue.name
      body['name'] = new_venue.name
      body['city'] = new_venue.city
      body['state'] = new_venue.state
      body['phone'] = new_venue.phone
      body['image_link'] = new_venue.image_link
      body['genres'] = new_venue.genres
      body['facebook_link'] = new_venue.facebook_link
  except:
      db.session.rollback()
      error_occured = True
      print(sys.exec_info())
  finally:
      db.session.close()
  if not error_occured:
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      return jsonify(body)
  else:
      # DONE: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. Venue ' + body['name'] + ' could not be listed.')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error_occured = False
    try:
        venue_to_delete = Venue.query.get(venue_id)
        if not venue_to_delete:
            error_occured = True
            raise Exception("Venue with id %s not found in the DB" % venue_to_delete)
        db.session.delete(venue_to_delete)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': (not error_occured) })

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  artists = Artist.query.all()
  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # Done: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response = {
    "count": 0,
    "data": []
  }
  search_term = request.form.get('search_term', '')
  artists = Artist.query.all()
  for artist in artists:
    if re.search(search_term, artist.name, re.IGNORECASE):
      # Found a match
      response["data"].append({
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": get_upcoming_shows(artist)
      })
      response["count"] = response["count"] + 1
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the Artist page with the given venue_id
  # DONE: replace with real artist data from the venues table, using artist_id
  artist = Artist.query.get(artist_id)
  response = artist.to_dict()
  upcoming_shows = get_upcoming_shows(artist)
  past_shows = get_past_shows(artist)
  upcoming_shows_count = len(upcoming_shows)
  past_shows_count = len(past_shows)
  response["upcoming_shows"] = upcoming_shows
  response["past_shows"] = past_shows
  response["upcoming_shows_count"] = upcoming_shows_count
  response["past_shows_count"] = past_shows_count
  return render_template('pages/show_artist.html', artist=response)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # DONE: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)
  form.name = artist.name
  form.city = artist.city
  form.state = artist.state
  form.phone = artist.phone
  form.image_link = artist.image_link
  form.genres = artist.genres
  form.facebook_link = artist.facebook_link
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  artist.name = request.form.get('name', '')
  artist.city = request.form.get('city', '')
  artist.state = request.form.get('state', '')
  artist.phone = request.form.get('phone', '')
  artist.image_link = request.form.get('image_link', None)
  artist.genres = request.form.get('genres', [])
  artist.facebook_link = request.form.get('facebook_link', None)
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  # DONE: populate form with values from venue with ID <venue_id>
  venue = Venue.query.get(venue_id)
  form.name = venue.name
  form.city = venue.city
  form.state = venue.state
  form.address = venue.address
  form.phone = venue.phone
  form.image_link = venue.image_link
  form.genres = venue.genres
  form.facebook_link = venue.facebook_link
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  venue.name = request.form.get('name', '')
  venue.city = request.form.get('city', '')
  venue.state = request.form.get('state', '')
  venue.address = request.form.get('address', '')
  venue.phone = request.form.get('phone', '')
  venue.image_link = request.form.get('image_link', None)
  venue.genres = request.form.get('genres', [])
  venue.facebook_link = request.form.get('facebook_link', None)
  db.session.commit()
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
  # DONE: insert form data as a new Artist record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  error_occured = False
  body = {
    'name': request.form.get('name', '')
  }
  try:
      new_artist = Artist(
        name = request.form.get('name', ''),
        city = request.form.get('city', None),
        state = request.form.get('state', None),
        phone = request.form.get('phone', None),
        image_link = request.form.get('image_link', None),
        genres = request.form.get('genres', []),
        facebook_link = request.form.get('facebook_link', None),
      )
      db.session.add(new_artist)
      db.session.commit()
      body['name'] = new_artist.name
      body['name'] = new_artist.name
      body['city'] = new_artist.city
      body['state'] = new_artist.state
      body['phone'] = new_artist.phone
      body['image_link'] = new_artist.image_link
      body['genres'] = new_artist.genres
      body['facebook_link'] = new_artist.facebook_link
  except:
      db.session.rollback()
      error_occured = True
      print(sys.exec_info())
  finally:
      db.session.close()
  if not error_occured:
      # on successful db insert, flash success
      flash('Artist ' + body['name'] + ' was successfully listed!')
      return jsonify(body)
  else:
      # DONE: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      flash('An error occurred. Artist ' + body['name'] + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  response = []
  for show in shows:
    show_data = show.to_dict()
    artist = Artist.query.get(show.artist_id)
    show_data["artist_name"] = artist.name
    show_data["artist_image_link"] = artist.image_link
    response.append(show_data)
  return render_template('pages/shows.html', shows=response)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  class ShowForm(Form):
      artist_id = StringField(
          'artist_id'
      )
      venue_id = StringField(
          'venue_id'
      )
      start_time = DateTimeField(
          'start_time',
          validators=[DataRequired()],
          default= datetime.today()
      )


  error_occured = False
  error_reason = ''
  body = {}
  try:
      new_show_start_time = request.form.get('start_time', None)
      new_show_artist_id = request.form.get('artist_id', None)
      new_show_venue_id = request.form.get('venue_id', None)
      if not new_show_start_time:
          error_occured = True
          error_reason = 'No start time specified'
      if not new_show_artist_id:
          error_occured = True
          error_reason = 'No artist specified for the show'
      if not new_show_venue_id:
          error_occured = True
          error_reason = 'No venue specified for the show'
      artist = Artist.query.get(new_show_artist_id)
      venue = Venue.query.get(new_show_venue_id)
      new_show = Show(
        start_time = new_show_start_time,
        artist = artist,
        venue = venue
      )
      db.session.add(new_show)
      db.session.commit()
      body['start_time'] = new_show.start_time
      body['artist_id'] = new_show.artist_id
      body['artist_name'] = artist.name
      body['venue_id'] = new_show.venue_id
      body['venue_name'] = venue.name
  except:
      db.session.rollback()
      error_occured = True
      print(sys.exec_info())
  finally:
      db.session.close()
  if not error_occured:
      # on successful db insert, flash success
      flash('Show was successfully listed!')
      return jsonify(body)
  else:
      # DONE: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. Show could not be listed.')
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

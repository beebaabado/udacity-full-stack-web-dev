#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')


# TODO: connect to a local postgresql database which has already been created
# using dbcreate (postgresql) and verified with psql

# Database connection info in config.py to keep specifics of database
# separate from model
# bind SQLAlchemy database object to this specific flask App
db = SQLAlchemy(app)

# Connect database and Model to migration object
# Run commands flask db init to create migrations folder
#              flask db migrations -m "SOME MESSAGE like Initial Migration"
#              Preview changes in the migration file for accuracy
#              flask db upgrade to actually  update the database with schema changes
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# 'Show' association or join table for artists and venues.  
show = db.Table('show',
       db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
       db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
       db.Column('start_time', db.DateTime, nullable=False)
)

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String, nullable=False)   #website URLs can be huge...
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String, nullable=False)
    
    # child relationship setup
    artists = db.relationship('Artist', secondary=show, backref='venue', lazy=True)  #Lazy be default 
    
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    def __repr__(self):
      return f'<Venue {self.id} {self.name}>'

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String, nullable=False) #website URSl can be long...
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String, nullable=False)
    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    def __repr__(self):
       return f'<Artist {self.id} {self.name}>'

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

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

# Default Route...index
@app.route('/')
def index():
  return render_template('pages/home.html')

#----------------------------------------------------------------------------#
#  VENUES
#----------------------------------------------------------------------------#

#~~~~~~~~List all Venues ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #
  #  
  # Returns list of dictionaries of areas and venues and number of upcoming shows per venue. 
  # data has format like:
  #data=[{
  #  "city": "San Francisco",
  #  "state": "CA",
  #  "venues": [{
  #    "id": 1,
  #    "name": "The Musical Hop",
  #    "num_upcoming_shows": 0,
  #  }, {
  #    "id": 3,
  #    "name": "Park Square Live Music & Coffee",
  #    "num_upcoming_shows": 1,
  #  }]
  #}, {
  #  "city": "New York",
  #  "state": "NY",
  #  "venues": [{
  #    "id": 2,
  #    "name": "The Dueling Pianos Bar",
  #    "num_upcoming_shows": 0,
  #  }]
  #}]
  #
  #

  # WHere the list of venues and areas will be stored to pass back to view
  data = []

  # Get list of cities and state -- areas   (returns list of tuples)
  result_areas = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()

  for area in result_areas:  
      venues=[]         #new venues list for this new area
      data_dict = {}    #create new temp dict for each area and venues list
      data_dict['city']=area[0]    
      data_dict['state']=area[1]

      #Get list of venues by city,state
      venues_for_one_city =\
        Venue.query.filter_by(city=area[0], state=area[1]).all()
          
      for v in venues_for_one_city:
         venue = {}
         venue["id"] = v.id
         venue["name"] = v.name   
         venue["num_upcoming_shows"] = 1   #TODO: calculate this value from shows table counts?
         venues.append(venue) 
         data_dict['venues']=venues
  
      # add area to data that will be passed to views
      data.append(data_dict)  

  return render_template('pages/venues.html', areas=data)

#~~~~~~~~Search for Venue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  #
  # return data looks like:
  #response={
  # "count": 1,
  # "data": [{
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "num_upcoming_shows": 0,
  # }]
  #}
  #
  response={}   #what to return to view
  # search_term =request.get_json()['search_term']
  search_term=request.form.get('search_term', '')
  venue_search_results = Venue.query.with_entities(Venue.id, Venue.name).filter(Venue.name.ilike('%' + search_term + '%')).all() # NOTE TO SELF:  returns an array of tuples (immutable)
  response['count'] = len(venue_search_results)
  response['data'] = []
   
  
  for item in venue_search_results:
    newdataitem = {}
    newdataitem['id'] = item.id
    newdataitem['name'] = item.name
    newdataitem['num_upcoming_shows'] = 0  # Need to do new query for this number against shows...sometype of aggregate JOIN ???
    response['data'].append(newdataitem)
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

#~~~~~~~~Get Venue by id ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  data =  Venue.query.get(venue_id)
   
  # filter filters out data from dta1, data2, data3 that is not associated with 
  # venue id passed in (venue_id)  But we won't  use this when we pass back data from
  # database query
  
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#~~~~CREATE: Create Venue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

#~~~~~~~~UPDATE:  Edit a Venue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


#~~~~~~~~DELETE: Delete a Venue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#---------------------------------------------------------------------------#
#  Artists
#---------------------------------------------------------------------------#

#~~~~~~~~list all Artists~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/artists')
def artists():
#
  #
  # TODO: replace with real data returned from querying the database
  data = Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  #
  # Using ilike query to do case insensitve search
  #
  # returned data looks like this:
  # response={
   # "count": 1,
   # "data": [{
    #  "id": 4,
    #  "name": "Guns N Petals",
     # "num_upcoming_shows": 0,
   # }]
  # }
 
  response={}   #what to return to view
 # search_term =request.get_json()['search_term']
  search_term=request.form.get('search_term', '')
  artist_search_results = Artist.query.with_entities(Artist.id, Artist.name).filter(Artist.name.ilike('%' + search_term + '%')).all() # NOTE TO SELF:  returns an array of tuples (immutable)
  response['count'] = len(artist_search_results)
  response['data'] = []
   
  for item in artist_search_results:
    newdataitem = {}
    newdataitem['id'] = item.id
    newdataitem['name'] = item.name
    newdataitem['num_upcoming_shows'] = 0  # Need to do new query for this number against shows...sometype of aggregate JOIN ???
    response['data'].append(newdataitem)

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

#~~~~~~~~ List Artist by id ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  data = Artist.query.get(artist_id) #NOTE TO SELF - .get returns object - app.Artist in this case so can add new properties 
  data.past_shows = []            #TODO need to do aggregate query to get these stats
  data.upcoming_shows = []
  data.past_shows_count = 1
  data.upcoming_shows_count = 0

  return render_template('pages/show_artist.html', artist=data)

#~~~~~~~~UPDATE:  Edit an Artist ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

#~~~~~~~~CREATE:  create an Artist ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')

#  ---------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

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

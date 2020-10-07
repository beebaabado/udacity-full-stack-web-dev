#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import datetime
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
import sys 
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__, static_url_path='/static')
moment = Moment(app)
app.config.from_object('config')


# COMPLETE: connect to a local postgresql database which has already been created
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

#'Show' association or join table for artists and venues.  
show = db.Table('show',
       db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
       db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
       db.Column('start_time', db.DateTime, primary_key=True, nullable=False)
)



#'Show' association or join table for artists and venues.  Created a 
# class Show(db.Model):
#      __tablename__= 'show'
#      venue_id =  db.Column( db.Integer, db.ForeignKey('venue.id'), primary_key=True),
#      artist_id = db.Column( db.Integer, db.ForeignKey('artist.id'), primary_key=True),
#      start_time = db.Column( db.DateTime, unique=True, nullable=False),
#      description = db.Column(db.String, nullable=False)
    
#      artist = db.relationship("Artist", back_populates="venues")
#      venue = db.relationship("Parent", back_populates="artists")

#      def __repr__(self):
#       return f'<Show {self.id} {self.description}>'


class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String, nullable=False)   #website URLs can be huge...
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String, nullable=False)
    
    # child relationship setup
    artists = db.relationship('Artist', secondary=show, backref='venue', lazy=True)  #Lazy be default 
    #artists = db.relationship('Show', back_populates="venue", lazy=True)
    # COMPLETE: implement any missing fields, as a database migration using Flask-Migrate

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
    website = db.Column(db.String, nullable=False) #website URLs can be long...
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String, nullable=False)
    # COMPLETE: implement any missing fields, as a database migration using Flask-Migrate
    
    #venues = db.relationship("Show", back_populates="artist")

    def __repr__(self):
       return f'<Artist {self.id} {self.name}>'

# COMPLETE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

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
  # COMPLETE: replace with real venues data.
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
         venue["upcoming_shows_count"] = db.session.query(show).filter(show.c.venue_id == v.id).count()
         venues.append(venue) 
         data_dict['venues']=venues
  
      # add area to data that will be passed to views
      data.append(data_dict)  

  return render_template('pages/venues.html', areas=data)

#~~~~~~~~Search for Venue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # COMPLETE: implement search on artists with partial string search. Ensure it is case-insensitive.
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
  venue_search_results = Venue.query.with_entities(Venue.id, Venue.name).\
    filter(Venue.name.ilike('%' + search_term + '%')).all() # NOTE TO SELF:  returns an array of tuples (immutable)
  response['count'] = len(venue_search_results)
  response['data'] = []
  
  for item in venue_search_results:
    newdataitem = {
      "id": item.id,
      "name": item.name,
      "num_upcoming_shows": 0  # Need to do new query for this number against shows...sometype of aggregate JOIN ???
    } 
    response['data'].append(newdataitem)
    
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

#~~~~~~~~Get Venue by id ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # COMPLETE: replace with real venue data from the venues table, using venue_id

  # filter filters out data from dta1, data2, data3 that is not associated with 
  # venue id passed in (venue_id)  But we won't  use this when we pass back data from
  # database query
  # 
  # #data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,

  # get time so we can determine if show is future or past
  current_time = datetime.utcnow()

  #get one venue by input venue id
  data =  Venue.query.get(venue_id)
  data.genres = data.genres.split(", ")
  data.past_shows_count = db.session.query(show).filter(show.c.venue_id == venue_id, show.c.start_time < current_time).count()
  data.past_shows = []
  past_shows = db.session.query(show, Artist.name, Artist.image_link).\
    join(Artist, show.c.artist_id == Artist.id).filter(show.c.venue_id == venue_id, show.c.start_time < current_time).all() 
  
  for s in past_shows:
      s = {
        "artist_id": s.artist_id,
        "artist_name": s.name,
        "artist_image_link": s.image_link,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      data.past_shows.append(s)
    
  data.upcoming_shows_count = db.session.query(show).filter(show.c.venue_id == 1, show.c.start_time > current_time).count()
  data.upcoming_shows = []
  upcoming_shows = db.session.query(show, Artist.name, Artist.image_link).\
    join(Artist, show.c.artist_id == Artist.id).filter(show.c.venue_id == venue_id, show.c.start_time > current_time).all()

  for s in upcoming_shows:
      s = {
        "artist_id": s.artist_id,
        "artist_name": s.name,
        "artist_image_link": s.image_link,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      data.upcoming_shows.append(s)

  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#~~~~CREATE: Create Venue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Render Venue form 
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()   
  return render_template('forms/new_venue.html', form=form)

# Create new Venue / add to database
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

    error = False 
    try:
       # print ( "data:  " ,request.form)
        
        form = request.form
        # translate to boolean
        seeking_talent = False
        if form['seeking_talent']=='y': 
          seeking_talent = True
      
        #do something with user input data
        if (form):
           newVenue = Venue(name=form['name'])
           newVenue.city = form['city']
           newVenue.state = form['state']
           newVenue.phone = form['phone']
           newVenue.address = form['address']
           newVenue.genres = ", ".join(form.getlist('genres'))  #note:  that space has to be there after the comma! genres stored in form as ('genres', 'Jazz'), ('genres', 'R&B')
           newVenue.website = form['website']
           newVenue.image_link = form['image_link']
           newVenue.facebook_link = form['facebook_link']
           newVenue.seeking_talent = seeking_talent
           newVenue.seeking_description = form['seeking_description']
           db.session.add(newVenue)
           db.session.commit()
           
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    if error:
        # TODO: on unsuccessful db insert, flash an error instead.   
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        #for field, errors in form.errors.items():
         #   for error, lines in errors.items():  TODO....want error messages from Form to print out  could be ugly for end user???
          #      description = "\n".join(lines)
           #     flash(u"Error in the %s field - %s" % (
            #    
             #       form[field][error].label.text,
              #      description
               # ))
        return redirect(url_for('create_venue_form'))
    else: 
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        #refresh
        return render_template('pages/home.html')

#~~~~~~~~UPDATE:  Edit a Venue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  #create venue form
  data = Venue.query.get(venue_id)
  venueForm = VenueForm()
  
  # TODO: populate form with values from venue with ID <venue_id>
  #data = Venue.query.get(venue_id)   # NOTE to self get gives you mutable object

  venueForm.name.data = data.name 
  venueForm.city.data = data.city 
  venueForm.state.data = data.state 
  venueForm.address.data = data.address
  venueForm.phone.data = data.phone 
  venueForm.genres.data = data.genres
  venueForm.website.data = data.website
  venueForm.image_link.data = data.image_link
  venueForm.facebook_link.data = data.facebook_link
  venueForm.seeking_talent.data = data.seeking_talent
  venueForm.seeking_description.data = data.seeking_description

  #show pre populated form  
  return render_template('forms/edit_venue.html', form=venueForm,  venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):


  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    error = False 
    try:
        existingVenue = Venue.query.get(venue_id) 
        form = request.form
        # translate to boolean
        seeking_talent = False
        if form['seeking_talent']=='y': 
          seeking_talent = True
      
        #update existing Venue data
        if (form):
           existingVenue.name = form['name']
           existingVenue.city = form['city']
           existingVenue.state = form['state']
           existingVenue.phone = form['phone']
           existingVenue.address = form['address']
           existingVenue.genres = ", ".join(form.getlist('genres'))  #note:  that space has to be there after the comma! genres stored in form as ('genres', 'Jazz'), ('genres', 'R&B')
           existingVenue.website = form['website']
           existingVenue.image_link = form['image_link']
           existingVenue.facebook_link = form['facebook_link']
           existingVenue.seeking_talent = seeking_talent
           existingVenue.seeking_description = form['seeking_description']
           db.session.commit() 
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    if error:
        # TODO: on unsuccessful db insert, flash an error instead.   
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
        return redirect(url_for('edit_venue', venue_id=venue_id))
    else: 
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
        #refresh, show updated info 
        return redirect(url_for('show_venue', venue_id=venue_id))
  
#~~~~~~~~DELETE: Delete a Venue ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  print("Delete Venue:  ", venue_id)
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepageerror = False
  error = False
  try:
    print("Delete Venue:  BEGIN TRY")
    venue=Venue.query.get(venue_id)
    name =venue.name
    #delete shows
    db.session.query(show).filter(show.c.venue_id==venue_id).delete()
    #delete venues
    db.session.delete(venue)
    #can also write as ... I think maybe allows for deleting more than one row...avoid builtin.list error?
    #Venues.query.filter_by(id=venue_id).delete()
    db.session.commit()
    print("Delete Venue:  committed")
  except:  
     print("Delete Venue:  error...rollback")  
     error = True
     db.session.rollback()
     print(sys.exc_info())
  finally:
     print("Delete Venue:  FINALLY")
     db.session.close()
   
  if error:
     # TODO: on unsuccessful db delete, flash an error instead.   
     flash('An error occurred. Venue ' + name + ' could not be deleted.')
     return redirect(url_for('show_venue', venue_id=venue_id))
  else: 
     # on successful db delete, flash success
     flash('Venue ' + name + ' was successfully deleted!')
     #refresh, show updated info 
     return render_template('pages/home.html')

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
  search_term=request.form.get('search_term', '')
  artist_search_results = Artist.query.with_entities(Artist.id, Artist.name). \
    filter(Artist.name.ilike('%' + search_term + '%')).all() # NOTE TO SELF:  returns an array of tuples (immutable)
  response['count'] = len(artist_search_results)
  response['data'] = []
   
  for item in artist_search_results:
    newdataitem = {
     "id": item.id,
     "name": item.name,
     "num_upcoming_shows": db.session.query(show).join(Artist, show.c.artist_id == item.id).distinct().count()
    }
    response['data'].append(newdataitem)
   
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

#~~~~~~~~ List Artist by id ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artists page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  # get time so we can determine if show is future or past
  current_time = datetime.utcnow()
  #get one artist by input artist id
  data = Artist.query.get(artist_id) #NOTE TO SELF - .get returns object - app.Artist in this case so can add new properties 
  data.genres = data.genres.split(", ")
 
  # Get past shows for this artist
  data.past_shows = []  
  data.past_shows_count = db.session.query(show).filter(show.c.artist_id == artist_id, show.c.start_time < current_time).count()         
  past_shows = db.session.query(show, Artist.name, Artist.image_link).\
    join(Artist, show.c.artist_id == Artist.id).filter(show.c.artist_id == artist_id, show.c.start_time < current_time).order_by(show.c.start_time).all() 
 
  for s in past_shows:
      s = {
        "venue_id": s.venue_id,
        "venue_name": s.name,
        "venue_image_link": s.image_link,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      data.past_shows.append(s)
  
  # Get upcoming shows for this artist
  data.upcoming_shows = []
  data.upcoming_shows_count = db.session.query(show).filter(show.c.artist_id == artist_id, show.c.start_time > current_time).count()
  past_shows = db.session.query(show, Artist.name, Artist.image_link).\
    join(Artist, show.c.artist_id == Artist.id).filter(show.c.artist_id == artist_id, show.c.start_time > current_time).order_by(show.c.start_time).all()
 
  for s in past_shows:
      s = {
        "venue_id": s.venue_id,
        "venue_name": s.name,
        "venue_image_link": s.image_link,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      data.upcoming_shows.append(s)
  
  return render_template('pages/show_artist.html', artist=data)

#~~~~~~~~UPDATE:  Edit an Artist ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artistForm = ArtistForm()
  #create artist form
  data = Artist.query.get(artist_id)
  
  artistForm.name.data = data.name 
  artistForm.city.data = data.city 
  artistForm.state.data = data.state 
  artistForm.phone.data = data.phone 
  artistForm.genres.data = data.genres
  artistForm.website.data = data.website
  artistForm.image_link.data = data.image_link
  artistForm.facebook_link.data = data.facebook_link
  artistForm.seeking_venue.data = data.seeking_venue
  artistForm.seeking_description.data = data.seeking_description
  
  #show pre populated form 
  return render_template('forms/edit_artist.html', form=artistForm, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    error = False 
    try:
        existingArtist = Artist.query.get(artist_id) 
        form = request.form
        
        # translate to boolean
        seeking_venue = False
        if form['seeking_venue']=='y': 
          seeking_venue = True
      
        #update existing Venue data
        if (form):
           existingArtist.name = form['name']
           existingArtist.city = form['city']
           existingArtist.state = form['state']
           existingArtist.phone = form['phone']
           existingArtist.genres = ", ".join(form.getlist('genres'))  #note:  that space has to be there after the comma! genres stored in form as ('genres', 'Jazz'), ('genres', 'R&B')
           existingArtist.website = form['website']
           existingArtist.image_link = form['image_link']
           existingArtist.facebook_link = form['facebook_link']
           existingArtist.seeking_venue = seeking_venue
           existingArtist.seeking_description = form['seeking_description']
           db.session.commit() 
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    if error:
        # TODO: on unsuccessful db insert, flash an error instead.   
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
        return redirect(url_for('edit_artist', artist_id=artist_id))
    else: 
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
        #refresh, show updated info 
        return redirect(url_for('show_artist', artist_id=artist_id))

    #show updated info  
    return redirect(url_for('show_artist', artist_id=artist_id))

#~~~~~~~~CREATE:  create an Artist ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  # I think this only works if merge two routes create form and submission and methods= GET and POST
  # if form.validate_on_submit():  # detects valid and POST request
  #       return render_template('forms/new_artist.html', form=form)
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new artist record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

    error = False
    try:
        form = request.form       
        
        # translate to boolean
        seeking_venue = False
        if (form['seeking_venue']):
           if (form['seeking_venue']) =='y': 
             seeking_venue = True

        #do something with user input data
        if (form):
           newArtist = Artist(name=form['name'])
           newArtist.city = form['city']
           newArtist.state = form['state']
           newArtist.phone = form['phone']
           newArtist.genres = ", ".join(form.getlist('genres'))  #note:  that space has to be there after the comma!
           newArtist.website = form['website']
           newArtist.image_link = form['image_link']
           newArtist.facebook_link = form['facebook_link']
           newArtist.seeking_venue = seeking_venue
           newArtist.seeking_description = form['seeking_description']
           db.session.add(newArtist)
           db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    if error:
        # TODO: on unsuccessful db insert, flash an error instead.   
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        #for field, errors in form.errors.items():
         #   for error, lines in errors.items():  TODO....want error messages from Form to print out  could be ugly for end user???
          #      description = "\n".join(lines)
           #     flash(u"Error in the %s field - %s" % (
            #    
             #       form[field][error].label.text,
              #      description
               # ))
        return redirect(url_for('create_artist_form'))
    else: 
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        #refresh
        return render_template('pages/home.html')


#  ---------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #
  # Gives shows for artist
  # shows = db.session.query(show).all()
  # shows with venue name and artist name
  # shows = db.session.query(show, Artist.name, Artist.image_link, Venue.name).join(Artist, \
  #    db.session.query(show, Artist.name.label("artist_name"), Artist.image_link, Venue.name.label("venue_name")).join(Artist, show.c.artist_id == Artist.id).join(Venue, show.c.venue_id == Venue.id).distinct().\
  #    group_by(Venue.name, show.c.artist_id, Artist.name, Artist.image_link, show.c.start_time, show.c.venue_id)
  # SQL = SELECT DISTINCT show.venue_id AS show_venue_id, show.artist_id AS show_artist_id, show.start_time AS show_start_time, artist.name AS artist_name, artist.image_link AS artist_image_link, venue.name AS venue_name 
  # FROM show 
  # JOIN artist ON show.artist_id = artist.id 
  # JOIN venue ON show.venue_id = venue.id 
  # GROUP BY show.venue_id, venue.name, show.artist_id, artist.name, artist.image_link, show.start_time
  
  data=[]
  shows = db.session.query(show, Artist.name.label("artist_name"), Artist.image_link, Venue.name.label("venue_name")).\
    join(Artist, show.c.artist_id == Artist.id).join(Venue, show.c.venue_id == Venue.id).distinct().\
    group_by(Venue.name, show.c.artist_id, Artist.name, Artist.image_link, show.c.start_time, show.c.venue_id).order_by(show.c.start_time)
       
  for s in shows:
      s = {
        "venue_name": s.venue_name,
        "artist_id": s.artist_id,
        "artist_name": s.artist_name,
        "artist_image_link": s.image_link,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      data.append(s)

  return render_template('pages/shows.html', shows=data)

#~~~~~~~~CREATE:  create a Show ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

#~~~~~~~~Error handler~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

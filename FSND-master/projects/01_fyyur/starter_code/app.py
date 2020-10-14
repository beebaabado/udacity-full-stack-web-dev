#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import datetime
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, make_response, jsonify
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


# 'Show' association or join table for artists and venues.  Prior version implemented
#  table.  Decided to use the alternate method of a Many to many relationship with
#  artitsts and Venues using Show as a class (association table).  This made it easier
#  to query for shows and delete shows when a venue is deleted by using objects via 
#  SQLAlchemy ORM  
#  
class Show(db.Model):
     __tablename__= 'show'
     venue_id =  db.Column( db.Integer, db.ForeignKey('venue.id'), primary_key=True)
     artist_id = db.Column( db.Integer, db.ForeignKey('artist.id'), primary_key=True)
     start_time = db.Column( db.DateTime, primary_key=True, nullable=False)
     description = db.Column(db.String, nullable=False)
    
     # Create relationships to artist and venue
     artist = db.relationship("Artist", back_populates="venues")
     venue = db.relationship("Venue", back_populates="artists")

     def __repr__(self):
       return f'<Show {self.description} {self.venue_id} {self.artist_id} {self.start_time}>'


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
    artists = db.relationship('Show', back_populates="venue", lazy=True)
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
    time_available_start = db.Column(db.DateTime, nullable=False)
    time_available_stop = db.Column(db.DateTime, nullable=False)
    
    # COMPLETE: implement any missing fields, as a database migration using Flask-Migrate
    
    venues = db.relationship("Show", back_populates="artist")

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
  # Get first 10 recently listed artists and venues
  artists = Artist.query.with_entities(Artist.id, Artist.name).order_by(Artist.id.desc()).limit(10)
  venues = Venue.query.with_entities(Venue.id, Venue.name).order_by(Venue.id.desc()).limit(10)
  return render_template('pages/home.html', artists=artists, venues=venues)

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
  # WHere the list of venues and areas will be stored to pass back to view
  data = []

  # Get list of cities and state -- areas   (returns list of tuples)
  result_areas = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()

  for a in result_areas:  
      venues=[]     #new venues list for this new area
      area = {}    #create new temp dict for each area and venues list
      area['city']=a[0]    
      area['state']=a[1]

      #Get list of venues by city,state
      venues_for_one_city =\
        Venue.query.filter_by(city=a[0], state=a[1]).all()
          
      for v in venues_for_one_city:
         venue = {}
         venue["id"] = v.id
         venue["name"] = v.name   
         venue["upcoming_shows_count"] = Show.query.filter(Show.venue_id == v.id).count()
         venues.append(venue) 
         area['venues']=venues
  
      # add area to data that will be passed to views
      data.append(area)  

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
  # see if user is searching by city and state
  # not so elegant but look for comma then split 
  # in to city and state.  Query for venue filter on city and state
  venue_search_results = []
  if (search_term.find(",")) != -1:
     parts = search_term.split(",")
     city = parts[0].strip()
     state = parts[1].strip()
     print(city, state)
     venue_search_results = Venue.query.with_entities(Venue.id, Venue.name).filter(Venue.city==city, Venue.state==state).order_by(Venue.name).all() 

  # if no results try a query on venue name.
  if len(venue_search_results) == 0:
     venue_search_results = Venue.query.with_entities(Venue.id, Venue.name).\
      filter(Venue.name.ilike('%' + search_term + '%')).order_by(Venue.name).all() # NOTE TO SELF:  returns an array of tuples (immutable)
  response['count'] = len(venue_search_results)
  response['data'] = []
 
  for venue in venue_search_results:
    newdataitem = {
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": Show.query.filter(Show.venue_id == venue.id, Show.start_time > datetime.utcnow()).count()
    } 
    response['data'].append(newdataitem)
    
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

#~~~~~~~~Get Venue by id ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # COMPLETE: replace with real venue data from the venues table, using venue_id
  # get time so we can determine if show is future or past
  current_time = datetime.utcnow()

  #get one venue by input venue id
  data =  Venue.query.get(venue_id)
  data.genres = data.genres.split(", ")

  data.past_shows = []  
  data.past_shows_count = Show.query.filter(Show.venue_id == venue_id, Show.start_time < current_time).count()
  past_shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time < current_time).order_by(Show.start_time).all()
  
  for s in past_shows:
      s = {
        "artist_id": s.artist_id,
        "artist_name": s.artist.name,
        "artist_image_link": s.artist.image_link,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      data.past_shows.append(s)
    
  data.upcoming_shows_count = Show.query.filter(Show.venue_id == venue_id, Show.start_time > current_time).count()
  data.upcoming_shows = []
  upcoming_shows = Show.query.filter(Show.venue_id == venue_id, Show.start_time > current_time).order_by(Show.start_time).all()

  for s in upcoming_shows:
      s = {
        "artist_id": s.artist_id,
        "artist_name": s.artist.name,
        "artist_image_link": s.artist.image_link,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      data.upcoming_shows.append(s)

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
        if ('seeking_talent' in form):
           if (form['seeking_talent']) =='y': 
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
        if ('seeking_talent' in form):
           if (form['seeking_talent']) =='y': 
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
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    print("Begin Try Delete Venue id: ", venue_id)
    venue=Venue.query.get(venue_id)
    name =venue.name
    #delete shows
    Show.query.filter(Show.venue_id==venue_id).delete()
    #delete venues
    db.session.delete(venue)
    #can also write as ... I think maybe allows for deleting more than one row...avoid builtin.list error?
    #Venues.query.filter_by(id=venue_id).delete()
    db.session.commit()
    print("Delete Venue id:  committed", venue_id)
  except:  
     #print("Delete Venue:  error...rollback")  
     error = True
     db.session.rollback()
     #print(sys.exc_info())
  finally:
     #print("Delete Venue:  FINALLY")
     db.session.close()
   
  if error:
     # TODO: on unsuccessful db delete, flash an error instead.  
     #print("YES ERROR in deleting venue ...show venue again.") 
     flash('An error occurred. Venue ' + name + ' could not be deleted.')
     return redirect(url_for('delete_venue', venue_id=venue_id))
  else: 
     # on successful db delete, flash success
     # print("NO ERROR in deleting venue ...go home.") 
     #NOTE to self: Server side redirects in delete handlers are not recommended
     flash('Venue ' + name + ' was successfully deleted!')
     return jsonify({ 'success': True })
  
  return render_template('/') #Does this ever get called????

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
  data.past_shows_count = Show.query.filter(Show.artist_id == artist_id, Show.start_time < current_time).count()
  past_shows = Show.query.filter(Show.artist_id == artist_id, Show.start_time < current_time).order_by(Show.start_time).all()
  for s in past_shows:
      s = {
        "venue_id": s.venue_id,
        "venue_name": s.venue.name,
        "venue_image_link": s.venue.image_link,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      data.past_shows.append(s)
  
  # Get upcoming shows for this artist
  data.upcoming_shows = []
  data.upcoming_shows_count = Show.query.filter(Show.artist_id == artist_id, Show.start_time > current_time).count()
  upcoming_shows = Show.query.filter(Show.artist_id == artist_id, Show.start_time > current_time).order_by(Show.start_time).all()
 
  for s in upcoming_shows:
      s = {
        "venue_id": s.venue_id,
        "venue_name": s.venue.name,
        "venue_image_link": s.venue.image_link,
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
  artistForm.available_start_time.data = data.time_available_start
  artistForm.available_stop_time.data = data.time_available_stop

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
        print(form)
        # translate to boolean
        seeking_venue = False
        if ('seeking_venue' in form):
           if (form['seeking_venue']) =='y': 
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
           existingArtist.time_available_start = form['available_start_time']
           existingArtist.time_available_stop = form['available_stop_time']
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
        if ('seeking_venue' in form):
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
           newArtist.time_available_start = form['available_start_time']
           newArtist.time_available_stop = form['available_stop_time']
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
        return redirect(url_for('create_artist_form'))
    else: 
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        #refresh
        return render_template('pages/home.html')

#~~~~~~~~DELETE: Delete a Artist ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
@app.route('/artists/<artist_id>/delete', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  error = False
  try:
    print("Begin Try Delete artist id: ", artist_id)
    artist=Artist.query.get(artist_id)
    name =artist.name
    #delete shows
    Show.query.filter(Show.artist_id==artist_id).delete()
    #delete artist
    db.session.delete(artist)
    #can also write as ... I think maybe allows for deleting more than one row...avoid builtin.list error?
    #Venues.query.filter_by(id=artist_id).delete()
    db.session.commit()
    print("Delete Artist id:  committed", artist_id)
  except:  
     #print("Delete Artist:  error...rollback")  
     error = True
     db.session.rollback()
     #print(sys.exc_info())
  finally:
     #print("Delete Artist:  FINALLY")
     db.session.close()
   
  if error:
     # TODO: on unsuccessful db delete, flash an error instead.  
     #print("YES ERROR in deleting artist ...show artist again.") 
     flash('An error occurred. Artist ' + name + ' could not be deleted.')
     return redirect(url_for('delete_artist', artist_id=artist_id))
  else: 
     # on successful db delete, flash success
     # print("Successful in deleting artist ...go home.") 
     #NOTE to self: Server side redirects in delete handlers are not recommended
     flash('Artist ' + name + ' was successfully deleted!')
     return jsonify({ 'success': True })
  
  return render_template('/') #Does this ever get called????


#  ---------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  
  data=[]
  # shows = Show.query(Artist.name.label("artist_name"), Artist.image_link, Venue.name.label("venue_name")).\
  #   join(Artist, Show.artist_id == Artist.id).join(Venue, Show.venue_id == Venue.id).distinct().\
  #   group_by(Venue.name, Show.artist_id, Artist.name, Artist.image_link, Show.start_time, Show.venue_id).order_by(Show.start_time).all()       
  
  shows = Show.query.order_by(Show.start_time).all()

  for s in shows:
      s = {
        "venue_id": s.venue.id,
        "venue_name": s.venue.name,
        "artist_id": s.artist.id,
        "artist_name": s.artist.name,
        "artist_image_link": s.artist.image_link,
        "artist_time_available_start": s.artist.time_available_start.isoformat(),
        "artist_time_available_stop": s.artist.time_available_stop.isoformat(),
        "description":s.description,
        "start_time": s.start_time.isoformat() #returned as datetime...converted to iso datetime
      }  
      print(s)
      data.append(s)

  return render_template('pages/shows.html', shows=data)

#~~~~~~~~CREATE:  create a Show ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route('/shows/<int:artist_d>/verifytime')
def verify_artist_time():


  return None

@app.route('/shows/create')
def create_show_form():
  # renders form. do not touch.
  form = ShowForm()
  artist = Artist.query.with_entities(Artist.id, Artist.name, Artist.time_available_start, Artist.time_available_stop).order_by(Artist.name).all()
  form.artist_id.choices = [(a.id, a.name + " (ID: " + str(a.id) + ")") for a in artist]
  form.venue_id.choices = [(v.id, v.name + " (ID: " + str(v.id) + ")") for v in Venue.query.with_entities(Venue.id, Venue.name).order_by(Venue.name).all()]
  return render_template('forms/new_show.html', form=form, artist=artist)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  
  try:
    error = False
    form=request.form
    newShow=Show()
    
    if (form):
      newShow.venue_id = form['venue_id']
      newShow.artist_id = form['artist_id']
      newShow.start_time = form['datepicker'] + ' ' + form['timepicker'] 
      newShow.description = form['description']
    db.session.add(newShow)
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
        flash('An error occurred. Show for Artist ' + request.form['artist_id'] +  ' and Venue ' \
          + request.form['venue_id'] + ' could not be listed.')
        return redirect(url_for('create_show_form'))
    else: 
        # on successful db insert, flash success
        flash('Show for Artist ' + request.form['artist_id'] +  ' and Venue ' \
          + request.form['venue_id'] +  ' was successfully listed!')
        #refresh
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

from datetime import datetime
from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField, SelectMultipleField, BooleanField, TextField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL, Length
from wtforms.fields.html5 import DateField, TimeField

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM

class ShowForm(FlaskForm):
    # Create/Edit show form
    artist_id = SelectField(
        'Artist', validators=[DataRequired()] 
    )
    venue_id = SelectField(
        'Venue', validators=[DataRequired()]
    )
    description = TextField(
        'Description', 
        validators=[DataRequired()],
        default="Show description"
    )
    datepicker = DateField (
        'Date', validators=[DataRequired()],
        format='%Y-%m-%d'
    )
    timepicker = TimeField (
        "Time", validators=[DataRequired()],
        format='%H:%M'
    )

class VenueForm(FlaskForm):
    # Create/Edit Venue form
    name = StringField(
        'Name', validators=[DataRequired()]
    )
    city = StringField(
        'City', validators=[DataRequired()]
    )
    state = SelectField(
        'State', validators=[DataRequired(), Length(2)],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'Address', validators=[DataRequired()]
    )
    phone = StringField(
        'Phone', validators=[DataRequired(), Length(12)]
    )
    image_link = StringField(
        'Image', validators=[URL()],
         default="/static/img/DefaultArtistImage.jpeg"
    )
    facebook_link = StringField(
        'Facebook', validators=[URL()],
        default="http://"
    )
    website = StringField(
        'Website', validators=[DataRequired(), URL()]   
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'Genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    seeking_talent = BooleanField(
        'Seeking new talent', 
        default=True
    )
    seeking_description = TextField(
        'Description', validators=[DataRequired()]
    )



class ArtistForm(FlaskForm):
    # Create/Edit Artist form
    name = StringField(
        'Name', validators=[DataRequired()]
    )
    city = StringField(
        'City', validators=[DataRequired()]
    )
    state = SelectField(
        'State', validators=[DataRequired(), Length(2)],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for phone
        'Phone', validators=[DataRequired(), Length(12)]
    )
    website = StringField(
       'Website', validators=[DataRequired(), URL()]
    )

    image_link = StringField(
        'Image', validators=[URL()],
        default="/static/img/DefaultArtistImage.jpeg"
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'Facebook', validators=[URL()],
        default="http://"
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'Genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    available_start_time = DateTimeField(
        'Available time start',
        validators=[DataRequired()],
        default=datetime.now()
    )
    available_stop_time = DateTimeField(
        'Available time end',
         validators=[DataRequired()],
        default=datetime.now()
    )
    seeking_venue = BooleanField(
        'Seeking Venue',
        default=True
    )
    seeking_description = TextField(
        'Description', validators=[DataRequired()]
    )


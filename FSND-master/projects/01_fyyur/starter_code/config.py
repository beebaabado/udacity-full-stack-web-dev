import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# TODO IMPLEMENT DATABASE URL and set other options for SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/fyyurdb_alt_schema_many_to_many'
# Prevent warning concerning use of Flask-SQLAlchemy event system causing overhead in memory usage
SQLALCHEMY_TRACK_MODIFICATIONS = False


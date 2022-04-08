import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI =\
    'postgresql://username:password@domain:port/database_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CSRF time to expire
WTF_CSRF_TIME_LIMIT = 3600
import os


DATABASE_URL = os.getenv('DATABASE_URL') if 'DATABASE_URL' in os.environ else 'sqlite://'
SQLALCHEMY_TRACK_MODIFICATIONS = False

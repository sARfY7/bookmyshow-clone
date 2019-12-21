from os import environ

# "postgres+psycopg2://postgres:password@localhost/bookmyshow"
class Config:
  SQLALCHEMY_DATABASE_URI = environ.get('DB_URI')
  SECRET_KEY = environ.get('SECRET_KEY')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

from os import environ

class Config:
  SQLALCHEMY_DATABASE_URI = environ.get('DB_URI')
  SECRET_KEY = environ.get('SECRET_KEY')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  TMDB_API_KEY = environ.get("TMDB_API_KEY")

import requests, os
from flask import session
from bookmyshow import db
from bookmyshow.config import Config
from bookmyshow.models import MovieScreening, Movie

def get_poster_base_url():
  config_url = f"https://api.themoviedb.org/3/configuration?api_key={Config.TMDB_API_KEY}"
  api_config = requests.get(config_url)
  config = None
  poster_base_url = None
  poster_size = None
  if (api_config.status_code == 200):
    config = api_config.json()
    poster_base_url = config["images"]["secure_base_url"]
    poster_size = config["images"]["poster_sizes"][3]
    return f"{poster_base_url}{poster_size}"
  return None

def get_now_playing_movies(page):
  url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={Config.TMDB_API_KEY}&language=en-US&page=" + page
  now_playing_movies_request = requests.get(url)
  if (now_playing_movies_request.status_code == 200):
    now_playing_movies = now_playing_movies_request.json()["results"]
    total_pages = now_playing_movies_request.json()["total_pages"]
    return (now_playing_movies, total_pages)
  return (None, None)

def get_screened_movies(page, offset):
  total_movie_screenings = MovieScreening.query.filter_by(
      theatre_id=session['user_id']).count()
  total_movie_screenings = (total_movie_screenings // 12) + \
      1 if total_movie_screenings % 12 != 0 else (total_movie_screenings // 12)
  movie_screenings = MovieScreening.query.filter_by(
      theatre_id=session['user_id']).limit(12).offset(offset)
  movies = []
  for movie_screening in movie_screenings:
    movies.append(movie_screening.movie)
  return (movies, total_movie_screenings)

def get_movie_data(movie_id):
  url = f"https://api.themoviedb.org/3/movie/{str(movie_id)}?api_key={Config.TMDB_API_KEY}&language=en-US"
  movie_request = requests.get(url)
  if (movie_request.status_code == 200):
    return movie_request.json()
  return None

def is_movie_screened(movie_title):
  existing_movie = Movie.query.filter_by(title=movie_title).first()
  if existing_movie is None:
    return False
  return existing_movie

def save_movie_poster(poster_path):
  poster_url = f"{get_poster_base_url()}{poster_path}"
  poster = requests.get(poster_url)
  open(os.path.abspath("bookmyshow/static/img/posters") +
       poster_path, "wb").write(poster.content)


def screen_new_movie(movie_data, screening_time):
  new_movie = Movie(title=movie_data['title'], overview=movie_data['overview'],
                    poster_path=movie_data['poster_path'], runtime=movie_data['runtime'], release_date=movie_data['release_date'])
  new_movie_screening = MovieScreening(
      screening_time=screening_time, theatre_id=session['user_id'])
  new_movie.screenings = [new_movie_screening]
  db.session.add(new_movie)
  db.session.commit()

def is_movie_screened_by_current_theatre(existing_movie):
  existing_movie_screening = existing_movie.screenings
  if len(existing_movie_screening) != 0:
     for movie_screening in existing_movie_screening:
       if (movie_screening.theatre_id == session['user_id']):
         return True
  return False

def screen_existing_movie(existing_movie, screening_time):
  new_movie_screening = MovieScreening(
      screening_time=screening_time, movie_id=existing_movie.id, theatre_id=session['user_id'])
  db.session.add(new_movie_screening)
  db.session.commit()

def delete_screened_movie(movie_id):
  movie = Movie.query.get(movie_id)
  if (len(movie.screenings) == 1):
    movie_screening = MovieScreening.query.filter_by(movie_id=movie_id, theatre_id=session["user_id"]).first()
    db.session.delete(movie_screening)
    db.session.delete(movie)
  else:
    movie_screening = MovieScreening.query.filter_by(movie_id=movie_id, theatre_id=session["user_id"]).first()
    db.session.delete(movie_screening)
  db.session.commit()

from flask import Blueprint, render_template, url_for, flash, redirect, session, request
from .forms import LoginForm, SignupForm, MovieScreeningForm
from bookmyshow import db, bcrypt, theatre_login_required
from bookmyshow.models import Theatre, Movie, MovieScreening
from bookmyshow.config import Config
import requests, json, os

theatre = Blueprint("theatre", __name__)

config_url = f"https://api.themoviedb.org/3/configuration?api_key={Config.TMDB_API_KEY}"
api_config = requests.get(config_url)
config = None
poster_base_url  = None
poster_size = None
if (api_config.status_code == 200):
  config = api_config.json()
  poster_base_url = config["images"]["secure_base_url"]
  poster_size = config["images"]["poster_sizes"][3]


@theatre.route("/theatre")
@theatre_login_required
def home():
  return render_template("theatre/home.html")

# Now Playing Movies
@theatre.route("/theatre/movies/nowplaying")
@theatre_login_required
def now_playing():
  page = request.args.get('page')
  if not page:
    page = str(1)
  url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={Config.TMDB_API_KEY}&language=en-US&page=" + page
  now_playing_movies_request = requests.get(url)
  if ((now_playing_movies_request.status_code == 200) and (api_config.status_code == 200)):
    now_playing_movies = now_playing_movies_request.json()["results"]
    total_pages = now_playing_movies_request.json()["total_pages"]
    return render_template("theatre/now-playing.html", poster_base_url=poster_base_url, poster_size=poster_size, movies=now_playing_movies, total_pages=total_pages)
  return "Error Fetching Now Playing Movies"

# List all theatre screened movies
@theatre.route("/theatre/movies")
@theatre_login_required
def movies():
  movie_screenings = MovieScreening.query.filter_by(theatre_id = session['user_id']).all()
  movies = []
  for movie_screening in movie_screenings:
    movies.append(movie_screening.movie)
  return render_template("theatre/view-movies.html", movies=movies)

# Screen Movie
@theatre.route("/theatre/movies/<int:movie_id>/screen", methods=["GET", "POST"])
@theatre_login_required
def screen_movie(movie_id):
  url = f"https://api.themoviedb.org/3/movie/{str(movie_id)}?api_key={Config.TMDB_API_KEY}&language=en-US"
  movie_request = requests.get(url)
  movie_screening_form = MovieScreeningForm()
  if (movie_request.status_code == 200):
    movie = movie_request.json()
    if movie_screening_form.validate_on_submit():
      # Check if movie already screened
      existing_movie = Movie.query.filter_by(title=movie['title']).first()
      if existing_movie is None:
        poster_url = poster_base_url + poster_size + "/" + movie["poster_path"]
        poster = requests.get(poster_url)
        open(os.path.abspath("bookmyshow/static/img/posters") +
            movie["poster_path"], "wb").write(poster.content)
        new_movie = Movie(title=movie['title'], overview=movie['overview'], poster_path=movie['poster_path'], runtime=movie['runtime'], release_date=movie['release_date'])
        db.session.add(new_movie)
        db.session.commit()
        new_movie_screening = MovieScreening(screening_time=movie_screening_form.screening_time.data, movie_id=new_movie.id, theatre_id=session['user_id'])
        db.session.add(new_movie_screening)
        db.session.commit()
        flash(f"Movie Screening added", "success")
      else:
        existing_movie_screening = existing_movie.screenings
        movie_already_screened = False
        if len(existing_movie_screening) != 0:
          for movie_screening in existing_movie_screening:
            if (movie_screening.theatre_id == session['user_id']):
              movie_already_screened = True
        if (not movie_already_screened):
          new_movie_screening = MovieScreening(
              screening_time=movie_screening_form.screening_time.data, movie_id=existing_movie.id, theatre_id=session['user_id'])
          db.session.add(new_movie_screening)
          db.session.commit()
          flash(f"Movie Screening added", "success")
        else:
          flash(f"Movie Screening already exists", "danger")
    return render_template("theatre/screen-movie.html", poster_base_url=poster_base_url, poster_size=poster_size, movie=movie, form=movie_screening_form)
  return "Error Fetching Movie Details"

# Update a movie screening time
@theatre.route("/theatre/movies/<int:movie_id>/update")
def update_movie_screening():
  pass

# Delete a movie
@theatre.route("/theatre/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie_screening(movie_id):
  return redirect(url_for('theatre.movies'))

@theatre.route("/theatre/login", methods=["GET", "POST"])
def login():
  if 'user_id' not in session:
    login_form = LoginForm()
    if login_form.validate_on_submit():
      theatre = Theatre.query.filter_by(email=login_form.email.data).first()
      if theatre and bcrypt.check_password_hash(theatre.password, login_form.password.data):
        session["user_id"] = theatre.id
        session["logged_in_as"] = "theatre"
        return redirect(url_for("theatre.home"))
      else:
        flash(f"Invalid login credentials", "danger")
    return render_template("login.html", form=login_form , user_type="Theatre Admin")
  return redirect(url_for("theatre.home"))


@theatre.route("/theatre/signup", methods=["GET", "POST"])
def signup():
  if 'user_id' not in session:
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(signup_form.password.data).decode("utf-8")
      new_theatre = Theatre(name=signup_form.name.data, location=signup_form.location.data, rows=signup_form.rows.data, columns=signup_form.columns.data, seat_price=signup_form.seat_price.data, email=signup_form.email.data, password=hashed_password)
      db.session.add(new_theatre)
      db.session.commit()
      flash(f"Your account has been created successfully. You can login now.", "success")
      return redirect(url_for("theatre.login"))
    return render_template("theatre/signup.html", form=signup_form, user_type="Theatre Admin")
  return redirect(url_for("theatre.home"))

@theatre.route("/logout")
def logout():
  session.pop('user_id')
  session.pop('logged_in_as')
  return redirect(url_for("theatre.login"))

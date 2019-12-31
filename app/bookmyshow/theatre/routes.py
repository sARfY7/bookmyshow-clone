from flask import Blueprint, render_template, url_for, flash, redirect, session, request
from .forms import LoginForm, SignupForm, MovieScreeningForm
from bookmyshow.auth import theatre_login_required
from .services import get_poster_base_url,get_now_playing_movies, get_screened_movies, get_movie_data, is_movie_screened, screen_new_movie, is_movie_screened_by_current_theatre, screen_existing_movie, delete_screened_movie
from .auth import is_valid_credentials, register_new_theatre
from bookmyshow.auth import logout_user

theatre = Blueprint("theatre", __name__)

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
  poster_base_url = get_poster_base_url()
  movies, total_pages = get_now_playing_movies(page)
  if (movies):
    return render_template("theatre/now-playing.html", poster_base_url=poster_base_url, movies=movies, total_pages=total_pages)
  return render_template("errors/500.html")

# List all movies screened by the theatre
@theatre.route("/theatre/movies")
@theatre_login_required
def movies():
  page = request.args.get('page')
  offset = None
  if not page:
    page = 1
    offset = 0
  else:
    page = int(page)
    offset = (page - 1) * 12
  screened_movies, total_screened_movies = get_screened_movies(page, offset)
  return render_template("theatre/view-movies.html", movies=screened_movies, total_pages=total_screened_movies)

# Screen Movie
@theatre.route("/theatre/movies/<int:movie_id>/screen", methods=["GET", "POST"])
@theatre_login_required
def screen_movie(movie_id):
  poster_base_url = get_poster_base_url()
  movie_data = get_movie_data(movie_id)
  movie_screening_form = MovieScreeningForm()
  if movie_screening_form.validate_on_submit():
    already_screened_movie = is_movie_screened(movie_data["title"])
    if (already_screened_movie):
      if is_movie_screened_by_current_theatre(already_screened_movie):
        flash(f"Movie Screening already exists", "danger")
      else:
        screen_existing_movie(already_screened_movie, movie_screening_form.screening_time.data)
        flash(f"Movie Screening added", "success")
    else:
      screen_new_movie(movie_data, movie_screening_form.screening_time.data)
      flash(f"Movie Screening added", "success")    
  return render_template("theatre/screen-movie.html", poster_base_url=poster_base_url, movie=movie_data, form=movie_screening_form)

# Update a movie screening time
# @theatre.route("/theatre/movies/<int:movie_id>/update")
# def update_movie_screening():
#   pass

# Delete a movie
@theatre.route("/theatre/movies/<int:movie_id>/delete", methods=["GET"])
def delete_movie(movie_id):
  delete_screened_movie(movie_id)
  return redirect(url_for('theatre.movies'))

@theatre.route("/theatre/login", methods=["GET", "POST"])
def login():
  if 'user_id' not in session:
    login_form = LoginForm()
    if login_form.validate_on_submit():
      if is_valid_credentials(login_form.email.data, login_form.password.data):
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
      theatre_data = {"name": signup_form.name.data, "location": signup_form.location.data, "rows": signup_form.rows.data, "columns": signup_form.columns.data, "seat_price": signup_form.seat_price.data, "email": signup_form.email.data, "password": signup_form.password.data}
      register_new_theatre(theatre_data)
      flash(f"Your account has been created successfully. You can login now.", "success")
      return redirect(url_for("theatre.login"))
    return render_template("theatre/signup.html", form=signup_form, user_type="Theatre Admin")
  return redirect(url_for("theatre.home"))

@theatre.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("theatre.login"))

from flask import Blueprint, render_template, url_for, request, json, session, redirect
from bookmyshow.models import MovieScreening, Movie, Theatre, Booking, Seat
from bookmyshow import db
import requests
from bookmyshow.auth import user_login_required
from .services import get_in_theatre_movies, get_movie_screenings, get_unavailable_seats, get_booking_summary, get_booking_confirmation, get_search_query_result

main = Blueprint("main", __name__)

@main.route("/")
def home():
    page = request.args.get('page')
    offset = None
    if not page:
      page = 1
      offset = 0
    else:
      page = int(page)
      offset = (page - 1) * 12
    movies, total_movies = get_in_theatre_movies(offset)
    return render_template("home.html", movies=movies, total_pages=total_movies)

@main.route("/movies/<int:movie_id>/book")
def book_movie(movie_id):
    movie, screening_theates = get_movie_screenings(movie_id)
    return render_template("booking.html", movie=movie, theatres=screening_theates)

@main.route("/movies/<int:movie_id>/theatres/<int:theatre_id>/booking")
def select_seat(movie_id, theatre_id):
  movie, theatre, unavailable_seats = get_unavailable_seats(movie_id, theatre_id)
  return render_template("select-seat.html", movie=movie, theatre=theatre, unavailable_seats=unavailable_seats)

@main.route("/movies/<int:movie_id>/theatres/<int:theatre_id>/summary", methods=["POST"])
def summary(movie_id, theatre_id):
  movie, theatre, selected_seats, total_amount = get_booking_summary(movie_id, theatre_id, request.form["seats"])
  return render_template("summary.html", movie=movie, theatre=theatre, seats=selected_seats, total_amount=total_amount)


@main.route("/movies/<int:movie_id>/theatres/<int:theatre_id>/confirmation", methods=["POST"])
@user_login_required
def confirmation(movie_id, theatre_id):
  movie, theatre, new_booking, booked_seats = get_booking_confirmation(movie_id, theatre_id, request.form["seats"].replace("'", '"'), request.form["amount"])
  return render_template("user/confirmation.html", movie=movie, theatre=theatre, booking=new_booking, seats=booked_seats)

@main.route("/movies/search")
def search():
  query = request.args.get("q")
  search_result = get_search_query_result(query)
  print(search_result)
  return render_template("search-result.html", result=search_result)
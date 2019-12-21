from flask import Blueprint, render_template, url_for, request, json, session, redirect
from bookmyshow.models import MovieScreening, Movie, Theatre, Booking, Seat
from bookmyshow import db, user_login_required

main = Blueprint("main", __name__)

@main.route("/")
def home():
    movies = Movie.query.all()
    return render_template("home.html", movies=movies)

@main.route("/movie/<int:movie_id>/book")
def book_movie(movie_id):
    movie = Movie.query.get(movie_id)
    movie_screenings = movie.screenings
    theatres = []
    for movie_screening in movie_screenings:
      theatres.append((movie_screening.theatre.id, movie_screening.theatre.name,
                       movie_screening.theatre.location, movie_screening.screening_time))
    return render_template("booking.html", movie=movie, theatres=theatres)

@main.route("/movie/<int:movie_id>/theatre/<int:theatre_id>/booking")
def select_seat(movie_id, theatre_id):
  movie = Movie.query.get(movie_id)
  theatre = Theatre.query.get(theatre_id)
  bookings = Booking.query.filter_by(movie_id=movie_id, theatre_id=theatre_id).all()
  unavailable_seats = []
  if (len(bookings) != 0):
    for booking in bookings:
      for seat in booking.seats:
        unavailable_seats.append({"row": seat.row, "column": seat.number})
  return render_template("select-seat.html", movie=movie, theatre=theatre, unavailable_seats=unavailable_seats)

@main.route("/movie/<int:movie_id>/theatre/<int:theatre_id>/summary", methods=["GET", "POST"])
def summary(movie_id, theatre_id):
  movie = Movie.query.get(movie_id)
  theatre = Theatre.query.get(theatre_id)
  if request.method == "POST":
    selected_seats = json.loads(request.form["seats"])
    total_amount = theatre.seat_price * len(selected_seats)
  return render_template("summary.html", movie=movie, theatre=theatre, seats=selected_seats, total_amount=total_amount)


@main.route("/movie/<int:movie_id>/theatre/<int:theatre_id>/confirmation", methods=["POST"])
@user_login_required
def confirmation(movie_id, theatre_id):
  movie = Movie.query.get(movie_id)
  theatre = Theatre.query.get(theatre_id)
  booked_seats = json.loads(request.form["seats"].replace("'", '"'))
  total_amount = request.form["amount"]
  new_booking = Booking(booking_amount=total_amount, movie_id=movie_id,
                        theatre_id=theatre_id, user_id=session['user_id'])
  db.session.add(new_booking)
  db.session.commit()
  for seat in booked_seats:
    new_booked_seat = Seat(
        row=seat['row'], number=seat['column'], booking_id=new_booking.id)
    db.session.add(new_booked_seat)
  db.session.commit()
  return render_template("user/confirmation.html", movie=movie, theatre=theatre, booking=new_booking, seats=booked_seats)

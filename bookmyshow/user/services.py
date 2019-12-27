from flask import session, json
from bookmyshow.models import Booking, Theatre, Movie,User

def get_user_bookings():
  bookings = Booking.query.filter_by(user_id=session['user_id']).join(
      Movie, Movie.id == Booking.movie_id).join(Theatre, Theatre.id == Booking.theatre_id).all()
  return bookings

def get_user_data(user_id):
  user = User.query.get(user_id)
  serialized_user_data = {"name": user.name, "bookings": []}
  for booking in user.bookings:
    movie = {"title": booking.movie.title,
             "overview": booking.movie.overview,
             "poster_path": booking.movie.poster_path,
             "runtime": booking.movie.runtime,
             "release_date": booking.movie.release_date}
    theatre = {"name": booking.theatre.name,
               "location": booking.theatre.location}
    seats = []
    for seat in booking.seats:
      seats.append({"row": seat.row, "number": seat.number})
    serialized_user_data["bookings"].append({"id": booking.id, "booked_at": booking.booked_at, "booking_amount": booking.booking_amount, "movie": movie, "theatre": theatre, "seats": seats})
  return json.dumps(serialized_user_data)

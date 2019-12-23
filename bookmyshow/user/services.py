from flask import session
from bookmyshow.models import Booking, Theatre, Movie

def get_user_bookings():
  bookings = Booking.query.filter_by(user_id=session['user_id']).join(
      Movie, Movie.id == Booking.movie_id).join(Theatre, Theatre.id == Booking.theatre_id).all()
  return bookings
from bookmyshow.models import Movie, Booking, Theatre, Seat
from flask import json, session
from bookmyshow import db

def get_in_theatre_movies(offset):
  total_movies = Movie.query.count()
  total_movies = (total_movies // 12) + \
      1 if total_movies % 12 != 0 else total_movies // 12
  movies = Movie.query.offset(offset).limit(12)
  return (movies, total_movies)

def get_movie_screenings(movie_id):
  movie = Movie.query.get(movie_id)
  movie_screenings = movie.screenings
  theatres = []
  for movie_screening in movie_screenings:
      theatres.append((movie_screening.theatre.id, movie_screening.theatre.name,
                       movie_screening.theatre.location, movie_screening.screening_time))
  return (movie, theatres)

def get_unavailable_seats(movie_id, theatre_id):
  movie = Movie.query.get(movie_id)
  theatre = Theatre.query.get(theatre_id)
  bookings = Booking.query.filter_by(
      movie_id=movie_id, theatre_id=theatre_id).all()
  unavailable_seats = []
  if (len(bookings) != 0):
    for booking in bookings:
      for seat in booking.seats:
        unavailable_seats.append({"row": seat.row, "column": seat.number})
  return (movie, theatre, unavailable_seats)

def get_booking_summary(movie_id, theatre_id, seats):
  movie = Movie.query.get(movie_id)
  theatre = Theatre.query.get(theatre_id)
  selected_seats = json.loads(seats)
  total_amount = theatre.seat_price * len(selected_seats)
  return (movie, theatre, selected_seats, total_amount)

def get_booking_confirmation(movie_id, theatre_id, seats, amount):
  movie = Movie.query.get(movie_id)
  theatre = Theatre.query.get(theatre_id)
  seats = json.loads(seats)
  total_amount = amount
  new_booking = Booking(booking_amount=total_amount, movie_id=movie_id, theatre_id=theatre_id, user_id=session['user_id'])
  booked_seats = []
  for seat in seats:
    booked_seats.append(Seat(row=seat['row'], number=seat['column']))
  new_booking.seats = booked_seats
  db.session.add(new_booking)
  db.session.commit()
  return (movie, theatre, new_booking, new_booking.seats)
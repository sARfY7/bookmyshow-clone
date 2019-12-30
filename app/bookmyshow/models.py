from bookmyshow import db

# Common DB Classes
Model = db.Model
Table = db.Table
Column = db.Column
ForeignKey = db.ForeignKey

# Common DB Functions
relationship = db.relationship

# DB Column Data Types
Integer = db.Integer
Float = db.Float
String = db.String
Text = db.Text
Boolean = db.Boolean
Date = db.Date
DateTime = db.DateTime
Time = db.Time

class Movie(Model):
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    overview = Column(Text)
    poster_path = Column(Text, nullable=False, default="/placeholder.png")
    runtime = Column(Integer)
    release_date = Column(Date)
    bookings = relationship('Booking', cascade="all, delete-orphan", backref='movie', lazy=True)
    screenings = relationship('MovieScreening', cascade="save-update, delete", backref='movie', lazy=True)

class MovieScreening(Model):
    id = Column(Integer, primary_key=True)
    screening_time = Column(Time, nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    theatre_id = Column(Integer, ForeignKey('theatre.id'), nullable=False)


class Theatre(Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Integer, nullable=False)
    seat_price = Column(Integer, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    bookings = relationship('Booking', backref='theatre', lazy=True)
    screenings = relationship('MovieScreening', backref='theatre', lazy=True)


class User(Model):
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    bookings = relationship('Booking', backref='user', lazy=True)


class Booking(Model):
    id = Column(Integer, primary_key=True)
    booked_at = Column(DateTime)
    booking_amount = Column(Integer, nullable=False)
    movie_id = Column(Integer, ForeignKey('movie.id'), nullable=False)
    theatre_id = Column(Integer, ForeignKey('theatre.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    seats = relationship('Seat', cascade="save-update, delete", backref='booking', lazy=True)


class Seat(Model):
    id = Column(Integer, primary_key=True)
    row = Column(Integer)
    number = Column(Integer)
    booking_id = Column(Integer, ForeignKey('booking.id'))

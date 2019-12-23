from bookmyshow import bcrypt, db
from bookmyshow.models import Theatre
from flask import session

def is_valid_credentials(email, password):
  theatre = Theatre.query.filter_by(email=email).first()
  if theatre and bcrypt.check_password_hash(theatre.password, password):
        session["user_id"] = theatre.id
        session["logged_in_as"] = "theatre"
        return True
  return False

def register_new_theatre(theatre):
  hashed_password = bcrypt.generate_password_hash(
      theatre['password']).decode("utf-8")
  new_theatre = Theatre(name=theatre['name'], location=theatre['location'], rows=theatre['rows'],
                        columns=theatre['columns'], seat_price=theatre['seat_price'], email=theatre['email'], password=hashed_password)
  db.session.add(new_theatre)
  db.session.commit()

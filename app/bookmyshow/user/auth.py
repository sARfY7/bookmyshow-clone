from flask import session
from bookmyshow import bcrypt, db
from bookmyshow.models import User

def is_valid_credentials(email, password):
  user = User.query.filter_by(email=email).first()
  if user and bcrypt.check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["logged_in_as"] = "user"
        return True
  return False

def register_new_user(user):
  hashed_password = bcrypt.generate_password_hash(
      user['password']).decode("utf-8")
  new_user = User(name=user['name'], email=user['email'], password=hashed_password)
  db.session.add(new_user)
  db.session.commit()

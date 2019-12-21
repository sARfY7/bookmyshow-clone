from bookmyshow.config import Config
from flask import Flask, request, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


def theatre_login_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if ('user_id' in session):
      return func(*args, **kwargs)
    else:
      return redirect(url_for('theatre.login'))
  return wrapper


def user_login_required(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    if ('user_id' in session):
      return func(*args, **kwargs)
    else:
      return redirect(url_for('user.login'))
  return wrapper

# Models Import
import bookmyshow.models as Models

# Route Imports
from bookmyshow.main.routes import main
from bookmyshow.theatre.routes import theatre
from bookmyshow.user.routes import user

# Blueprint Registerations
app.register_blueprint(main)
app.register_blueprint(theatre)
app.register_blueprint(user)

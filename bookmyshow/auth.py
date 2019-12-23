from flask import session, redirect, url_for
from functools import wraps

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

def logout_user():
  session.pop('user_id')
  session.pop('logged_in_as')
from flask import Blueprint, render_template, url_for, redirect, flash, session
from .forms import LoginForm, SignupForm
from bookmyshow import db, bcrypt, user_login_required
from bookmyshow.models import User, Booking, Movie, Theatre

user = Blueprint("user", __name__)


@user.route("/user/bookings")
@user_login_required
def bookings():
  bookings = Booking.query.filter_by(user_id=session['user_id']).join(
      Movie, Movie.id == Booking.movie_id).join(Theatre, Theatre.id == Booking.theatre_id).all()
  print(bookings)
  return render_template("user/user-bookings.html", bookings=bookings)

@user.route("/user/login", methods=["GET", "POST"])
def login():
  if 'user_id' not in session:
    login_form = LoginForm()
    if login_form.validate_on_submit():
      user = User.query.filter_by(email=login_form.email.data).first()
      if user and bcrypt.check_password_hash(user.password, login_form.password.data):
        session["user_id"] = user.id
        session["logged_in_as"] = "user"
        return redirect(url_for("main.home"))
      else:
        flash(f"Invalid login credentials", "danger")
    return render_template("login.html", form=login_form, user_type="User")
  return redirect(url_for('main.home'))


@user.route("/user/signup", methods=["GET", "POST"])
def signup():
  if 'user_id' not in session:
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(
          signup_form.password.data).decode("utf-8")
      new_user = User(name=signup_form.name.data,
                      email=signup_form.email.data, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
      flash(f"Your account has been created successfully. You can login now.", "success")
      return redirect(url_for("user.login"))
    return render_template("signup.html", form=signup_form, user_type="User")
  return redirect(url_for('main.home'))


@user.route("/logout")
def logout():
  session.pop('user_id')
  session.pop('logged_in_as')
  return redirect(url_for("user.login"))

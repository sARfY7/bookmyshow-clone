from flask import Blueprint, render_template, url_for, redirect, flash, session
from .forms import LoginForm, SignupForm
from bookmyshow.auth import user_login_required, logout_user
from .auth import is_valid_credentials, register_new_user
from .services import get_user_bookings

user = Blueprint("user", __name__)

# Get User Bookings
@user.route("/user/bookings")
@user_login_required
def bookings():
  user_bookings = get_user_bookings()
  return render_template("user/user-bookings.html", bookings=user_bookings)

@user.route("/user/login", methods=["GET", "POST"])
def login():
  if 'user_id' not in session:
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if is_valid_credentials(login_form.email.data, login_form.password.data):
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
      user_data = {"name": signup_form.name.data, "email": signup_form.email.data, "password": signup_form.password.data}
      register_new_user(user_data)
      flash(f"Your account has been created successfully. You can login now.", "success")
      return redirect(url_for("user.login"))
    return render_template("signup.html", form=signup_form, user_type="User")
  return redirect(url_for('main.home'))


@user.route("/logout")
def logout():
  logout_user()
  return redirect(url_for("user.login"))

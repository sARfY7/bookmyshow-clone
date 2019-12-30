from flask import Blueprint, render_template, url_for, redirect, flash, session, json, request, send_from_directory, make_response
from .forms import LoginForm, SignupForm
from bookmyshow.auth import user_login_required, logout_user
from .auth import is_valid_credentials, register_new_user
from .services import get_user_bookings
from .tasks import fetch_user_data
import os

user = Blueprint("user", __name__)

# Get User Bookings
@user.route("/user/bookings")
@user_login_required
def bookings():
  user_bookings = get_user_bookings()
  return render_template("user/user-bookings.html", bookings=user_bookings)

@user.route("/user/data/download")
@user_login_required
def download_user_data():
  #return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__name__)), "bookmyshow/data"), f"{session['user_id']}_user_data.json")
  user_data_file = open(f"bookmyshow/data/{session['user_id']}_user_data.json")
  user_data = user_data_file.read()
  user_data_file.close()
  response = make_response(user_data)
  response.headers["Content-Type"] = "application/text"
  response.headers["Content-Disposition"] = "inline; filename=user_data.json"
  return response

@user.route("/user/data", methods=["GET", "POST"])
@user_login_required
def get_user_data():
  if request.method == "POST":
    task = fetch_user_data.apply_async(args=[session["user_id"]])
    return json.jsonify({'location': url_for('user.task_status', task_id=task.id)}), 202
  return render_template("user/user-data.html")

@user.route("/task/<task_id>")
@user_login_required
def task_status(task_id):
  task = fetch_user_data.AsyncResult(task_id)
  if task.ready():
    with open(f"bookmyshow/data/{session['user_id']}_user_data.json", "w") as user_data_file:
      user_data_file.write(task.get())
    return json.dumps({"status": task.status})
  return json.dumps({"status": task.status})

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

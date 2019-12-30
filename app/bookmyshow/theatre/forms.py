from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FileField, SubmitField, PasswordField, TextAreaField, TimeField
from wtforms.validators import Email, Regexp, InputRequired, ValidationError
from bookmyshow.models import Theatre

# class MovieForm(FlaskForm):
#   name = StringField("Movie Name", validators=[InputRequired()])
#   description = TextAreaField("Movie Description")
#   poster = FileField("Movie Poster")
#   runtime = IntegerField("Movie Runtime")
#   cast = StringField("Cast")
#   directors = StringField("Directors")
#   release_date = DateField("Release Date")
#   submit = SubmitField("Add Movie")

class MovieScreeningForm(FlaskForm):
  screening_time = TimeField("Movie Screening Time (24H Format)", validators=[InputRequired()])
  submit = SubmitField("Add Movie Screening")


class SignupForm(FlaskForm):
  name = StringField("Theatre Name", validators=[InputRequired()])
  location = StringField("Theatre Location", validators=[InputRequired()])
  rows = IntegerField("Num of Seat Rows", validators=[InputRequired()])
  columns = IntegerField("Num of Seat Columns", validators=[InputRequired()])
  seat_price = IntegerField("Price per Seat", validators=[InputRequired()])
  email = StringField("Email", validators=[InputRequired(), Email()])
  password = PasswordField("Password", validators=[InputRequired()])
  submit = SubmitField("Signup")

  def validate_email(self, email):
    theatre = Theatre.query.filter_by(email = email.data).first()
    if theatre:
      raise ValidationError("This email is already registered.")


class LoginForm(FlaskForm):
  email = StringField("Email", validators=[InputRequired(), Email()])
  password = PasswordField("Password", validators=[InputRequired()])
  submit = SubmitField("Login")

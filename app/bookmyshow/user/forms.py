from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, ValidationError
from bookmyshow.models import User

class SignupForm(FlaskForm):
  name = StringField("Name", validators=[InputRequired()])
  email = StringField("Email", validators=[InputRequired(), Email()])
  password = PasswordField("Password", validators=[InputRequired()])
  submit = SubmitField("Signup")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("This email is already registered.")


class LoginForm(FlaskForm):
  email = StringField("Email", validators=[InputRequired(), Email()])
  password = PasswordField("Password", validators=[InputRequired()])
  submit = SubmitField("Login")
